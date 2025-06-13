# WorkConnect - Modern Job Board Platform

A modern, full-stack job board application built with Django 5.x and Bootstrap 5, featuring role-based authentication, job search, and application management.

## Features

- 🔐 Role-based authentication (Admin, Employer, Job Seeker)
- 🔑 Social Authentication (Google)
- 💼 Job posting and management
- 🔍 Advanced job search and filtering
- 📝 Resume upload and management
- 📊 User dashboards
- 🎨 Modern, responsive UI
- 📱 Mobile-friendly design

## Tech Stack

- Django 5.x
- Bootstrap 5
- SQLite3
- Python Social Auth
- Font Awesome
- LottieFiles

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/workconnect.git
cd workconnect
```

2. Create and activate virtual environment:
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
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
workconnect/
├── applications/    # Job applications management
├── employers/       # Employer features and dashboard
├── jobs/           # Job listings and search
├── users/          # User authentication and profiles
├── static/         # Static files (CSS, JS, images)
├── templates/      # HTML templates
└── workconnect/    # Project settings
```

## Key Features

### For Job Seekers
- Create and manage professional profile
- Upload and manage resumes
- Search and filter job listings
- Easy job application process
- Track application status
- Save favorite jobs

### For Employers
- Company profile management
- Post and manage job listings
- Review applications
- Search candidate database
- Dashboard with analytics

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
