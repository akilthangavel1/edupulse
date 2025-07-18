# EduPulse Authentication System

This document describes the authentication system implemented for the EduPulse project.

## Overview

A complete authentication system has been added as a separate Django app called `accounts`. This system provides user registration, login, logout, and dashboard functionality with a modern, responsive UI.

## Features

### 🔐 User Authentication
- **User Registration**: Create new accounts with username, email, first name, last name, and password
- **User Login**: Secure login with username and password
- **User Logout**: Secure logout functionality
- **Dashboard**: User dashboard with account information and quick actions

### 🎨 Modern UI Design
- Responsive Bootstrap 5 design
- Gradient color scheme with modern card layouts
- Icon integration using Bootstrap Icons
- Mobile-friendly responsive design
- Form validation and error handling

## URL Structure

The authentication system is available at the following URLs:

- `/accounts/register/` - User registration
- `/accounts/login/` - User login
- `/accounts/logout/` - User logout
- `/accounts/dashboard/` - User dashboard (requires login)

## Files Structure

```
accounts/
├── __init__.py
├── admin.py
├── apps.py
├── forms.py              # Custom registration and login forms
├── models.py
├── tests.py
├── urls.py               # URL patterns for authentication
├── views.py              # Authentication views
├── migrations/
└── templates/
    └── accounts/
        ├── base.html     # Base template for auth pages
        ├── login.html    # Login form template
        ├── register.html # Registration form template
        └── dashboard.html # User dashboard template
```

## Key Components

### Forms (`forms.py`)
- `CustomUserCreationForm`: Enhanced registration form with additional fields
- `CustomAuthenticationForm`: Styled login form

### Views (`views.py`)
- `register_view`: Handles user registration
- `login_view`: Handles user authentication
- `logout_view`: Handles user logout
- `dashboard_view`: Protected dashboard view

### Templates
- **Base Template**: Consistent styling and layout
- **Login Template**: Clean login form with validation
- **Registration Template**: Comprehensive registration form
- **Dashboard Template**: User information and quick actions

## Usage

### For Users

1. **Register**: Visit `/accounts/register/` to create a new account
2. **Login**: Visit `/accounts/login/` to access your account
3. **Dashboard**: After login, access your dashboard at `/accounts/dashboard/`
4. **Logout**: Use the logout link in the dashboard navigation

### For Developers

The authentication system is fully integrated with Django's built-in authentication framework:

- Uses Django's `User` model
- Implements `@login_required` decorators for protected views
- Includes proper form validation and error handling
- Follows Django best practices for security

## Security Features

- CSRF protection on all forms
- Password validation using Django's built-in validators
- Secure session management
- Login required decorators for protected views
- Proper redirect handling after login/logout

## Configuration

The following settings have been added to `settings.py`:

```python
# Authentication settings
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
```

## Integration

The accounts app has been:
- Added to `INSTALLED_APPS` in settings.py
- URL patterns included in the main project URLs
- Designed to work seamlessly with the existing student management system

## Next Steps

You can extend this authentication system by:
- Adding user profile management
- Implementing password reset functionality
- Adding role-based permissions
- Integrating with the student management system for access control

## Testing

To test the authentication system:

1. Start the development server: `python manage.py runserver`
2. Visit `http://127.0.0.1:8000/accounts/register/` to create a test account
3. Login at `http://127.0.0.1:8000/accounts/login/`
4. Access the dashboard to see user information and navigation

The system is now ready for use! 