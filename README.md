# Energy Tracker

A Django web application for tracking energy usage and calculating costs over time.

## Features
- Input meter readings and energy tariff information
- Visualize energy cost trends with charts
- View recent readings and calculated costs
- Simple, user-friendly dashboard

## Requirements
- Python 3.13+
- Django 5.1.7
- Matplotlib
- SQLite (default)

## Setup
1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd Energy-Tracker
   ```
2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv env
   source env/bin/activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirments.txt
   ```
4. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```
5. **Run the development server:**
   ```sh
   python manage.py runserver
   ```
6. **Access the app:**
   Open your browser and go to `http://localhost:8000/`

## Usage
- Add new meter readings and tariff data via the input form
- View the dashboard for cost trends and recent readings

## File Structure
- `energy_tracker/` - Django project settings and static files
- `meter/` - Main app: models, views, forms, migrations
- `templates/` - HTML templates for dashboard and input
- `db.sqlite3` - Default database
- `requirments.txt` - Python dependencies

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License.

---

## Developer Information

- **Author:** Robbie FaLL
- **Contact:** [robbiefall@robbiefallcycles.cc]
- **GitHub:** [https://github.com/RobbieFaLL](https://github.com/RobbieFaLL)

## Educational Use

This project was created for an educational assignment and is intended for learning and demonstration purposes only. It is not intended for production use.

Feel free to use, modify, and share for educational activities!
