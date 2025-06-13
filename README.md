# WorkConnect - Modern Job Board Platform

A modern, full-stack job board application built with Django 5.x and Bootstrap 5, featuring role-based authentication, job search, and application management.

## Features

- 🔐 Role-based authentication (Admin, Employer, Job Seeker)
- 🔑 Social Authentication (Google, LinkedIn)
- 💼 Job posting and management
- 🔍 Advanced job search and filtering
- 📝 Resume upload and management
- 📊 User dashboards with analytics
- 🎨 Modern, responsive UI
- 📱 Mobile-friendly design
- 🚀 Performance optimized
- 🛡️ Enhanced security features
- 🔄 Real-time browser reload in development
- 🐞 Advanced error handling and debugging

## Tech Stack

### Backend
- Django 5.x
- Python 3.12+
- SQLite3 (Development)
- Redis (Caching)
- Gunicorn (Production server)

### Frontend
- Bootstrap 5
- JavaScript
- SCSS
- Custom SVG illustrations

### Development Tools
- Django Debug Toolbar
- Django Extensions
- Browser Reload
- Coverage Testing
- Python Dotenv
- VS Code configuration

### Additional Features
- WhiteNoise for static files
- Django Cleanup for file management
- Crispy Forms with Bootstrap 5
- Social Auth integration
- Enhanced security middleware

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/workconnect.git
   cd workconnect
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Development

### VS Code Setup
The project includes VS Code configuration for:
- Python linting and formatting
- Debugging configuration
- Recommended extensions
- Editor settings

### Debug Toolbar
Access the Django Debug Toolbar by:
1. Ensuring `DEBUG=True` in your `.env`
2. Looking for the toolbar on the right side of your browser

### Browser Reload
Changes to templates, static files, and Python code will automatically trigger a browser reload in development.

### Shell Plus
Use Django Extensions' enhanced shell:
```bash
python manage.py shell_plus
```

## Testing

Run tests with coverage:
```bash
coverage run manage.py test
coverage report
coverage html  # For detailed HTML report
```

## Deployment

1. Set up your production environment:
   - Set `DEBUG=False`
   - Configure a proper database (e.g., PostgreSQL)
   - Set up proper email backend
   - Configure Redis for caching
   - Set up static files serving

2. Install production requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the Gunicorn server:
   ```bash
   gunicorn workconnect.wsgi:application
   ```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django community
- Bootstrap team
- Contributors and users
