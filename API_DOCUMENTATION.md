# API Documentation

This document provides technical documentation for the Energy Tracker Django application, including models, views, URLs, and forms.

## Table of Contents
- [Models](#models)
- [Views](#views)
- [URLs](#urls)
- [Forms](#forms)
- [Database Schema](#database-schema)
- [Template Context](#template-context)

## Models

### MeterReading

Located in `meter/models.py`

Stores individual meter readings with energy usage data.

```python
class MeterReading(models.Model):
    date = models.DateField()
    kwh_used = models.FloatField()
```

**Fields:**
- `id` (AutoField): Primary key, auto-generated
- `date` (DateField): Date when the meter reading was taken
- `kwh_used` (FloatField): Energy consumption in kilowatt-hours

**Database Table:** `meter_meterreading`

**Example Usage:**
```python
from meter.models import MeterReading
from datetime import date

# Create a new reading
reading = MeterReading.objects.create(
    date=date.today(),
    kwh_used=125.5
)

# Query readings
recent_readings = MeterReading.objects.all().order_by('-date')[:10]
```

### Tariff

Located in `meter/models.py`

Stores energy pricing information.

```python
class Tariff(models.Model):
    price_per_kwh = models.IntegerField(help_text="Enter price in pence (e.g., 15 for £0.15)")
```

**Fields:**
- `id` (AutoField): Primary key, auto-generated
- `price_per_kwh` (IntegerField): Price per kWh in pence (e.g., 15 = £0.15)

**Database Table:** `meter_tariff`

**Example Usage:**
```python
from meter.models import Tariff

# Create a tariff
tariff = Tariff.objects.create(price_per_kwh=15)  # 15 pence per kWh

# Get current tariff (assumes latest is current)
current_tariff = Tariff.objects.last()
```

## Views

### input_data

Located in `meter/views.py`

Handles both GET and POST requests for the data input page.

**URL:** `/` (root)
**Template:** `input.html`
**Methods:** GET, POST

**Functionality:**
- GET: Displays empty forms for meter reading and tariff input
- POST: Processes form submissions and saves valid data

**Form Handling:**
```python
def input_data(request):
    if request.method == "POST":
        meter_form = MeterReadingForm(request.POST)
        tariff_form = TariffForm(request.POST)

        if meter_form.is_valid():
            meter_form.save()

        if tariff_form.is_valid():
            tariff_form.save()

        return redirect('dashboard')

    meter_form = MeterReadingForm()
    tariff_form = TariffForm()
    return render(request, 'input.html', {
        'meter_form': meter_form, 
        'tariff_form': tariff_form
    })
```

**Context Variables:**
- `meter_form`: MeterReadingForm instance
- `tariff_form`: TariffForm instance

### dashboard

Located in `meter/views.py`

Displays energy usage dashboard with charts and recent readings.

**URL:** `/dashboard/`
**Template:** `dashboard.html`
**Methods:** GET

**Functionality:**
- Retrieves all meter readings and latest tariff
- Calculates costs for each reading
- Generates matplotlib chart as base64 encoded image
- Handles cases where no data is available

**Chart Generation:**
```python
# Matplotlib Plot
plt.figure(figsize=(8, 5))
plt.plot(dates, costs, marker='o', linestyle='-')
plt.xlabel("Date")
plt.ylabel("Cost (£)")
plt.title("Energy Cost Over Time")
plt.grid(True)

# Convert to base64 for web display
buf = io.BytesIO()
plt.savefig(buf, format="png")
buf.seek(0)
encoded = base64.b64encode(buf.read()).decode('utf-8')
```

**Context Variables:**
- `chart`: Base64 encoded PNG image string
- `readings`: List of readings with calculated costs
- `tariff`: Current tariff object
- `error`: Error message if no data available

**Cost Calculation:**
```python
cost = reading.kwh_used * tariff.price_per_kwh  # Result in pence
```

## URLs

### Project URLs (`energy_tracker/urls.py`)
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('meter.urls')),
]
```

### App URLs (`meter/urls.py`)
```python
urlpatterns = [
    path('', input_data, name='input_data'),
    path('dashboard/', dashboard, name='dashboard'),
]
```

**Available Routes:**
- `/` → Input data page
- `/dashboard/` → Dashboard with charts and readings
- `/admin/` → Django admin interface

## Forms

### MeterReadingForm

Located in `meter/forms.py`

Form for inputting meter readings.

```python
class MeterReadingForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = MeterReading
        fields = ['date', 'kwh_used']
```

**Fields:**
- `date`: HTML5 date input with form-control CSS class
- `kwh_used`: Float input for energy usage

### TariffForm

Located in `meter/forms.py`

Form for inputting tariff information.

```python
class TariffForm(forms.ModelForm):
    class Meta:
        model = Tariff
        fields = ['price_per_kwh']
        widgets = {
            'price_per_kwh': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 0, 
                'step': 1
            }),
        }
```

**Fields:**
- `price_per_kwh`: Number input with minimum value 0 and step 1

## Database Schema

### Tables

**meter_meterreading:**
```sql
CREATE TABLE meter_meterreading (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    kwh_used REAL NOT NULL
);
```

**meter_tariff:**
```sql
CREATE TABLE meter_tariff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    price_per_kwh INTEGER NOT NULL
);
```

### Migrations

Current migrations:
- `0001_initial.py`: Initial models creation
- `0002_alter_tariff_price_per_kwh.py`: Tariff field modification

## Template Context

### input.html Context
```python
{
    'meter_form': MeterReadingForm(),
    'tariff_form': TariffForm()
}
```

### dashboard.html Context
```python
{
    'chart': 'base64_encoded_image_string',
    'readings': [
        {
            'date': datetime.date,
            'kwh_used': float,
            'cost': float  # in pence
        }
    ],
    'tariff': Tariff(),
    'error': 'Error message'  # Only if no data
}
```

## Error Handling

### No Data Available
When no readings or tariff data exists:
```python
if not readings.exists() or not tariff:
    return render(request, 'dashboard.html', {'error': "No data available."})
```

### Form Validation
Forms use Django's built-in validation:
- Date fields validate proper date format
- Float fields validate numeric input
- Integer fields validate whole numbers
- Minimum values enforced via widget attributes

## Security Considerations

- Forms use Django's CSRF protection
- No user authentication implemented (suitable for single-user/demo)
- SQLite database for development (not recommended for production)
- No input sanitization beyond Django defaults

## Performance Notes

- Matplotlib plots generated on each dashboard request
- No caching implemented
- Database queries are simple but could benefit from optimization for large datasets
- All readings loaded into memory for chart generation