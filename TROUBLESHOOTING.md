# Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the Energy Tracker Django application.

## Table of Contents
- [Installation Issues](#installation-issues)
- [Database Problems](#database-problems)
- [Development Server Issues](#development-server-issues)
- [Chart/Visualization Problems](#chartvisualization-problems)
- [Form and Data Entry Issues](#form-and-data-entry-issues)
- [Template and Static Files](#template-and-static-files)
- [Production Deployment Issues](#production-deployment-issues)
- [Performance Issues](#performance-issues)

## Installation Issues

### Python Version Compatibility

**Problem:** Application doesn't work with older Python versions
```
SyntaxError: invalid syntax
```

**Solution:**
- Ensure you're using Python 3.13+ as specified in requirements
- Check your Python version: `python --version`
- Use the correct Python command: `python3` instead of `python` on some systems

### Virtual Environment Issues

**Problem:** Packages not found or import errors
```
ModuleNotFoundError: No module named 'django'
```

**Solution:**
1. Ensure virtual environment is activated:
   ```bash
   source env/bin/activate  # Linux/Mac
   env\Scripts\activate     # Windows
   ```
2. Verify you're in the correct environment:
   ```bash
   which python
   pip list
   ```
3. Reinstall requirements:
   ```bash
   pip install -r requirments.txt
   ```

### Requirements Installation Fails

**Problem:** Package installation errors
```
ERROR: Could not install packages due to an EnvironmentError
```

**Solutions:**
1. **Update pip:**
   ```bash
   pip install --upgrade pip
   ```

2. **Install with user flag:**
   ```bash
   pip install --user -r requirments.txt
   ```

3. **Install packages individually:**
   ```bash
   pip install django==5.1.7
   pip install matplotlib
   pip install pandas
   ```

4. **Clear pip cache:**
   ```bash
   pip cache purge
   ```

## Database Problems

### Migration Issues

**Problem:** Migration fails or conflicts
```
django.db.utils.OperationalError: no such table: meter_meterreading
```

**Solutions:**
1. **Reset migrations (development only):**
   ```bash
   rm meter/migrations/0*.py
   python manage.py makemigrations meter
   python manage.py migrate
   ```

2. **Check migration status:**
   ```bash
   python manage.py showmigrations
   ```

3. **Apply specific migration:**
   ```bash
   python manage.py migrate meter 0001 --fake
   python manage.py migrate meter
   ```

### Database Locked Error

**Problem:** SQLite database is locked
```
django.db.utils.OperationalError: database is locked
```

**Solutions:**
1. **Stop all Django processes:**
   ```bash
   ps aux | grep python
   kill -9 <process_id>
   ```

2. **Remove lock files:**
   ```bash
   rm db.sqlite3-journal  # If exists
   ```

3. **Restart development server:**
   ```bash
   python manage.py runserver
   ```

### Data Loss or Corruption

**Problem:** Database appears empty or corrupted

**Solutions:**
1. **Check database file:**
   ```bash
   ls -la db.sqlite3
   file db.sqlite3
   ```

2. **Backup and restore:**
   ```bash
   cp db.sqlite3 db.sqlite3.backup
   python manage.py dumpdata > data.json
   rm db.sqlite3
   python manage.py migrate
   python manage.py loaddata data.json
   ```

## Development Server Issues

### Port Already in Use

**Problem:** Development server won't start
```
Error: That port is already in use.
```

**Solutions:**
1. **Use different port:**
   ```bash
   python manage.py runserver 8001
   ```

2. **Kill process using port 8000:**
   ```bash
   lsof -ti:8000 | xargs kill -9
   ```

3. **Find and stop process:**
   ```bash
   ps aux | grep runserver
   kill <process_id>
   ```

### Server Crashes on Startup

**Problem:** Server immediately crashes
```
SystemCheckError: System check identified some issues
```

**Solutions:**
1. **Run system check:**
   ```bash
   python manage.py check
   ```

2. **Check settings:**
   ```bash
   python manage.py diffsettings
   ```

3. **Verify database connection:**
   ```bash
   python manage.py dbshell
   ```

## Chart/Visualization Problems

### Matplotlib Backend Issues

**Problem:** Charts don't display or cause crashes
```
UserWarning: Matplotlib is currently using agg, which is a non-GUI backend
```

**Solutions:**
1. **Ensure correct backend (already set in code):**
   ```python
   import matplotlib
   matplotlib.use('Agg')  # Non-GUI backend
   ```

2. **Install additional dependencies:**
   ```bash
   pip install pillow  # Usually included
   ```

3. **Clear matplotlib cache:**
   ```bash
   rm -rf ~/.matplotlib  # Linux/Mac
   ```

### Charts Not Displaying

**Problem:** Dashboard shows no chart or broken image

**Solutions:**
1. **Check if data exists:**
   - Ensure you have both meter readings and tariff data
   - Go to input page and add some data

2. **Debug chart generation:**
   ```python
   # Add to dashboard view for debugging
   import logging
   logging.basicConfig(level=logging.DEBUG)
   logger = logging.getLogger(__name__)
   logger.debug(f"Readings: {readings.count()}")
   logger.debug(f"Tariff: {tariff}")
   ```

3. **Verify image encoding:**
   - Check if `encoded` variable contains base64 data
   - Ensure `buf.close()` and `plt.close()` are called

### Chart Display Errors

**Problem:** Chart shows but with incorrect data
```
ValueError: x and y must have same first dimension
```

**Solutions:**
1. **Check data consistency:**
   ```python
   print(f"Dates length: {len(dates)}")
   print(f"Costs length: {len(costs)}")
   ```

2. **Filter invalid data:**
   ```python
   # Add validation before plotting
   valid_readings = readings.filter(kwh_used__gt=0)
   ```

## Form and Data Entry Issues

### Form Validation Errors

**Problem:** Forms don't submit or show validation errors

**Solutions:**
1. **Check form errors in template:**
   ```html
   {% if meter_form.errors %}
       {{ meter_form.errors }}
   {% endif %}
   ```

2. **Debug form in view:**
   ```python
   if not meter_form.is_valid():
       print(meter_form.errors)
   ```

3. **Verify field requirements:**
   - Ensure date is in correct format (YYYY-MM-DD)
   - Check that kwh_used is a valid float
   - Verify price_per_kwh is a positive integer

### Data Not Saving

**Problem:** Form appears to submit but data doesn't save

**Solutions:**
1. **Check form processing logic:**
   ```python
   # Ensure both validation and save are correct
   if meter_form.is_valid():
       meter_reading = meter_form.save()
       print(f"Saved reading: {meter_reading.id}")
   ```

2. **Verify database write permissions:**
   ```bash
   ls -la db.sqlite3
   ```

3. **Check for transaction issues:**
   ```python
   from django.db import transaction
   with transaction.atomic():
       meter_form.save()
   ```

### Date Format Issues

**Problem:** Date input not working correctly

**Solutions:**
1. **Check browser compatibility:**
   - HTML5 date input requires modern browser
   - Fallback to text input if needed

2. **Verify date format in view:**
   ```python
   from datetime import datetime
   try:
       date_obj = datetime.strptime(date_string, '%Y-%m-%d')
   except ValueError:
       # Handle invalid date
   ```

## Template and Static Files

### CSS Styles Not Loading

**Problem:** Page appears unstyled

**Solutions:**
1. **Check static file configuration:**
   ```python
   # In settings.py
   STATIC_URL = '/static/'
   STATICFILES_DIRS = [
       BASE_DIR / "energy_tracker" / "static",
   ]
   ```

2. **Verify file paths:**
   ```bash
   ls -la energy_tracker/static/styles.css
   ```

3. **Collect static files (production):**
   ```bash
   python manage.py collectstatic
   ```

### Template Not Found

**Problem:** TemplateDoesNotExist error
```
TemplateDoesNotExist at /dashboard/
dashboard.html
```

**Solutions:**
1. **Check template directory setting:**
   ```python
   TEMPLATES = [{
       'DIRS': [BASE_DIR / 'templates'],
   }]
   ```

2. **Verify template files exist:**
   ```bash
   ls -la templates/
   ```

3. **Check template names in views:**
   ```python
   return render(request, 'dashboard.html', context)
   ```

## Production Deployment Issues

### Static Files Not Served

**Problem:** CSS/JS files return 404 in production

**Solutions:**
1. **Configure web server:**
   ```nginx
   location /static/ {
       alias /path/to/static/files/;
   }
   ```

2. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Check STATIC_ROOT setting:**
   ```python
   STATIC_ROOT = '/var/www/mysite/static/'
   ```

### Database Connection Errors

**Problem:** Can't connect to production database
```
OperationalError: FATAL: password authentication failed
```

**Solutions:**
1. **Verify connection settings:**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

2. **Test database connection:**
   ```bash
   psql -h localhost -U your_user -d your_database
   ```

3. **Check firewall/security groups:**
   - Ensure database port is accessible
   - Verify network connectivity

### Permission Denied Errors

**Problem:** File permission errors in production
```
PermissionError: [Errno 13] Permission denied
```

**Solutions:**
1. **Fix file ownership:**
   ```bash
   sudo chown -R www-data:www-data /path/to/app/
   ```

2. **Set correct permissions:**
   ```bash
   chmod 755 /path/to/app/
   chmod 644 /path/to/app/files/
   ```

3. **Check SELinux (if applicable):**
   ```bash
   sudo setsebool -P httpd_can_network_connect 1
   ```

## Performance Issues

### Slow Page Loading

**Problem:** Dashboard takes long time to load

**Solutions:**
1. **Optimize database queries:**
   ```python
   # Use select_related for foreign keys
   readings = MeterReading.objects.select_related().all()
   ```

2. **Limit data for charts:**
   ```python
   # Show only last 100 readings
   readings = MeterReading.objects.all().order_by('-date')[:100]
   ```

3. **Cache chart generation:**
   ```python
   from django.core.cache import cache
   
   chart_key = f"chart_{readings.count()}_{tariff.id}"
   chart = cache.get(chart_key)
   if not chart:
       # Generate chart
       cache.set(chart_key, encoded, 3600)  # 1 hour
   ```

### High Memory Usage

**Problem:** Application uses too much memory

**Solutions:**
1. **Optimize matplotlib usage:**
   ```python
   plt.figure(figsize=(8, 5))
   # ... plotting code ...
   plt.close()  # Important: always close figures
   ```

2. **Limit data processing:**
   ```python
   # Process data in chunks for large datasets
   from django.core.paginator import Paginator
   paginator = Paginator(readings, 1000)
   ```

## Debug Mode

### Enable Debug Information

For development troubleshooting, temporarily enable debug mode:

```python
# In settings.py (NEVER in production)
DEBUG = True

# Add debug toolbar for detailed information
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
```

### Logging Configuration

Add detailed logging for troubleshooting:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'meter': {  # Your app
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## Getting Help

If you're still experiencing issues:

1. **Check Django documentation:** https://docs.djangoproject.com/
2. **Search GitHub issues:** Look for similar problems in the repository
3. **Create a new issue:** Include error messages, system info, and steps to reproduce
4. **Django community:** Stack Overflow, Django Discord, Reddit r/django

## Quick Diagnostic Commands

```bash
# Check Python version
python --version

# Verify Django installation
python -c "import django; print(django.get_version())"

# Check database connectivity
python manage.py dbshell

# Validate Django project
python manage.py check

# Show migration status
python manage.py showmigrations

# Test development server
python manage.py runserver --verbosity=2

# Check installed packages
pip list

# Show Django settings
python manage.py diffsettings
```

Remember to always backup your database before attempting fixes, especially in production environments!