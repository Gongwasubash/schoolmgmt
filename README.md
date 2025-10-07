# School Management System

A comprehensive Django-based school management system for managing students, teachers, fees, academics, and administrative tasks.

## Features

- **Student Management**: Registration, profiles, academic records
- **Teacher Management**: Staff profiles, subject assignments
- **Fee Management**: Fee structure, payment tracking, receipts
- **Academic Management**: Marksheets, grades, calendar events
- **Website Content**: Hero sliders, blog posts, announcements
- **Administrative Tools**: User management, reports, notifications

## Models

- Student, Teacher, Staff profiles
- FeeStructure, FeePayment with payment tracking
- Marksheet, Subject, Grade management
- CalendarEvent, HeroSlider, Blog content
- User authentication and permissions

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd schoolmgmt
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

## Deployment

Use the provided build scripts for deployment:

- `build.sh` - Standard deployment script
- `build_deploy.py` - Comprehensive deployment with error handling
- `fix_database.py` - Database migration fix script

## Database Fix

If you encounter "no such table" errors during deployment, run:
```bash
python fix_database.py
```

See `DATABASE_FIX.md` for detailed troubleshooting.

## Project Structure

```
schoolmgmt/
├── schoolmgmt/          # Main Django app
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── urls.py          # URL routing
│   └── templates/       # HTML templates
├── static/              # Static files (CSS, JS, images)
├── media/               # User uploaded files
├── build.sh             # Deployment script
├── fix_database.py      # Database fix utility
└── manage.py            # Django management script
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.