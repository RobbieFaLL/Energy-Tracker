# Contributing to Energy Tracker

Thank you for your interest in contributing to Energy Tracker! This document provides guidelines for contributing to this Django-based energy usage tracking application.

## Getting Started

### Prerequisites
- Python 3.13+
- Git
- Basic knowledge of Django framework
- Familiarity with SQLite databases

### Setting Up Development Environment

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Energy-Tracker.git
   cd Energy-Tracker
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirments.txt
   ```

4. **Set up the database:**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## How to Contribute

### Reporting Issues
- Use the GitHub issue tracker to report bugs
- Include detailed information about the issue
- Provide steps to reproduce the problem
- Include your Python and Django versions

### Suggesting Features
- Open an issue with the "enhancement" label
- Clearly describe the feature and its benefits
- Discuss implementation approaches if you have ideas

### Code Contributions

#### Code Style Guidelines
- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep line length under 88 characters
- Use type hints where appropriate

#### Django-Specific Guidelines
- Follow Django coding conventions
- Use Django's built-in features when possible
- Write database queries efficiently
- Handle form validation properly
- Use Django's template system effectively

#### Example Code Style:
```python
from django.db import models
from typing import Optional

class MeterReading(models.Model):
    """Model for storing meter readings with energy usage data."""
    
    date = models.DateField(help_text="Date of the meter reading")
    kwh_used = models.FloatField(help_text="Energy used in kWh")
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self) -> str:
        return f"Reading on {self.date}: {self.kwh_used} kWh"
```

### Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation if needed

3. **Test your changes:**
   ```bash
   python manage.py test
   python manage.py runserver  # Manual testing
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```

5. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request:**
   - Use a clear, descriptive title
   - Describe what your changes do
   - Reference any related issues
   - Include screenshots for UI changes

### Commit Message Guidelines
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 50 characters
- Reference issues when applicable

Examples:
- `Fix: Resolve tariff calculation bug`
- `Add: Energy usage chart visualization`
- `Update: Improve form validation`
- `Docs: Add installation instructions`

## Project Structure

```
Energy-Tracker/
├── energy_tracker/          # Django project settings
│   ├── settings.py         # Main configuration
│   ├── urls.py            # URL routing
│   └── static/            # Static files (CSS, JS)
├── meter/                 # Main application
│   ├── models.py         # Database models
│   ├── views.py          # Request handlers
│   ├── forms.py          # Form definitions
│   ├── urls.py           # App-specific URLs
│   └── migrations/       # Database migrations
├── templates/            # HTML templates
└── manage.py            # Django management script
```

## Testing

### Running Tests
```bash
python manage.py test
```

### Writing Tests
- Add tests for new models, views, and forms
- Use Django's TestCase class
- Test both positive and negative scenarios
- Include edge cases

Example test:
```python
from django.test import TestCase
from .models import MeterReading

class MeterReadingTestCase(TestCase):
    def test_meter_reading_creation(self):
        """Test that meter readings are created correctly."""
        reading = MeterReading.objects.create(
            date='2025-01-01',
            kwh_used=100.5
        )
        self.assertEqual(reading.kwh_used, 100.5)
```

## Documentation

- Update README.md for significant changes
- Add docstrings to new functions and classes
- Update this CONTRIBUTING.md if the process changes
- Include inline comments for complex logic

## Getting Help

- Open an issue for questions about contributing
- Check existing issues and pull requests first
- Be patient and respectful in all interactions

## Recognition

Contributors will be acknowledged in the project documentation. Thank you for helping make Energy Tracker better!

## License

By contributing to Energy Tracker, you agree that your contributions will be licensed under the MIT License.