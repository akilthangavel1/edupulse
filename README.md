# EduPulse - School Management System

A comprehensive school management system built with Django for managing students, courses, fees, attendance, marks, faculty, and more.

## 📚 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [URL Reference Guides](#url-reference-guides)
- [Module Overview](#module-overview)
- [Key Features](#key-features)
- [Documentation](#documentation)
- [Support](#support)

---

## ✨ Features

### 🎓 Student Management
- Complete student registration and profile management
- Student drafts for incomplete registrations
- Old student records (completed 10th level)
- Student photo uploads
- Data export to CSV
- Advanced search and filtering

### 📋 Attendance Management
- Individual attendance marking
- Bulk attendance for multiple students
- Attendance dashboard with statistics
- Daily, weekly, and monthly reports
- **Automatic email notifications to parents when student is absent**
- Attendance history tracking

### 💰 Course Fee Management
- Course creation and management
- Student enrollment in courses
- Fee structure management (multiple fee types)
- Invoice generation
- Payment recording and tracking
- Receipt generation (Print, PDF, Excel)
- Discount management
- Kit fee tracking
- Financial reports

### 📊 Marks Management
- Subject management
- Assessment type configuration
- Grade scale setup
- Mark entry (individual and bulk)
- Student performance reports
- Grade summaries

### 👨‍🏫 Faculty Management
- Faculty profiles
- Onboarding process
- Leave request management
- Faculty payments
- Backup schedule management
- Exam request handling
- Attendance reporting

### 🎓 Batch Management
- Batch creation and management
- Student assignments to batches
- Batch transfers
- Faculty changes
- WhatsApp group integration

### 🚌 Transport Management
- Vendor management
- Vendor request approval
- Student transport assignments
- Monthly payment generation
- Vendor ratings
- Transport reports

### 📦 Kit Materials Management
- Material inventory
- Category and supplier management
- Kit assembly
- Stock movements
- Low stock alerts
- Integration with course fee kits

### 📢 Broadcast & Lead Management
- Message templates
- Broadcast management (general and specific)
- Lead tracking
- Lead scoring
- Communication logs
- Performance analytics

### 🔐 System Administration
- User and role management
- Audit logs
- Security monitoring
- Backup and restore
- System health monitoring
- Configuration management

---

## 🛠 Technology Stack

- **Backend:** Django 5.2.1 (Python)
- **Database:** SQLite3 (Development)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Authentication:** Django Auth System
- **Email:** Django Email Backend (Console for development, SMTP for production)
- **File Storage:** Django File Storage
- **PDF Generation:** ReportLab
- **Excel Export:** OpenPyXL

---

## 📥 Installation

### Prerequisites
- Python 3.13+
- pip
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd edupulse
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create superuser**
```bash
python manage.py createsuperuser
```

6. **Run development server**
```bash
python manage.py runserver
```

7. **Access the application**
- Main application: http://localhost:8000/
- Admin panel: http://localhost:8000/admin/

---

## 🔗 URL Reference Guides

We have created comprehensive URL reference documentation:

### 📖 [Complete URL Reference Guide](URL_REFERENCE.md)
- Detailed listing of all URLs organized by module
- Full descriptions of each endpoint
- URL naming conventions
- Parameter explanations

### ⚡ [Quick Reference Cheat Sheet](URL_QUICK_REFERENCE.md)
- Most commonly used URLs
- Quick access patterns
- Template tag examples
- Common URL patterns

**Quick Access to Main URLs:**

| Function | URL | Status |
|----------|-----|--------|
| **Dashboard** | http://localhost:8000/ | ✅ Working |
| **Login** | http://localhost:8000/accounts/login/ | ✅ Working |
| **Django Admin** | http://localhost:8000/admin/ | ✅ Working |
| **Students** | http://localhost:8000/students/ | ✅ Working |
| **Attendance** | http://localhost:8000/attendance/ | ✅ Working |
| **Course Fees** | http://localhost:8000/coursefee/ | ✅ Working |
| **Marks** | http://localhost:8000/marks/ | ✅ Working |
| **Faculty** | http://localhost:8000/faculty/ | ✅ Working |

**Django Admin URLs (Superuser/Staff Access):**

| Function | URL | Access Level |
|----------|-----|--------------|
| **Admin Home** | http://localhost:8000/admin/ | Superuser/Staff |
| **User Management** | http://localhost:8000/admin/auth/user/ | Superuser |
| **Groups/Roles** | http://localhost:8000/admin/auth/group/ | Superuser |
| **Students (Admin)** | http://localhost:8000/admin/xstudent/newstudent/ | Staff+ |
| **Courses (Admin)** | http://localhost:8000/admin/xcoursefee/course/ | Staff+ |
| **Payments (Admin)** | http://localhost:8000/admin/xcoursefee/payment/ | Staff+ |
| **Marks (Admin)** | http://localhost:8000/admin/xmark/mark/ | Staff+ |

---

## 📦 Module Overview

### Core Modules

| Module | Prefix | Description |
|--------|--------|-------------|
| **accounts** | `/accounts/` | User authentication and authorization |
| **xstudent** | `/` | Student management and attendance |
| **xcoursefee** | `/coursefee/` | Course fees, enrollment, and payments |
| **xmark** | `/marks/` | Marks and grade management |
| **xtrainer** | `/faculty/` | Faculty management |
| **xbatch** | `/batches/` | Batch and class management |
| **xtransport** | `/transport/` | Transport vendor management |
| **xkit** | `/kits/` | Kit materials and inventory |
| **xbroadcast** | `/broadcast/` | Communication and lead management |
| **xadmin** | `/system/` | System administration |

---

## 🎯 Key Features

### ✅ Automated Processes
- **Absence Notifications:** Automatic email to parents when student marked absent
- **Invoice Number Generation:** Auto-generated invoice numbers
- **Receipt Numbers:** Auto-generated receipt numbers on payment completion
- **Grade Calculation:** Automatic grade percentage calculations

### 📊 Reporting
- Student attendance reports (daily, weekly, monthly)
- Financial reports (revenue, payments, outstanding)
- Student performance reports
- Faculty attendance reports
- Transport reports
- Kit inventory reports

### 🔒 Security
- Role-based access control
- Audit logging for all actions
- Security event monitoring
- Password reset functionality
- Session management

### 📱 User Experience
- Responsive design (mobile-friendly)
- Intuitive navigation
- Search and filter functionality
- Pagination for large datasets
- Export to CSV, PDF, Excel
- Bulk operations support

---

## 📚 Documentation

### Available Documentation Files

1. **[MODULE_STATUS.md](MODULE_STATUS.md)** - ⚠️ **READ THIS FIRST** - Shows which modules are fully functional vs under development
2. **[URL_REFERENCE.md](URL_REFERENCE.md)** - Complete URL documentation
3. **[URL_QUICK_REFERENCE.md](URL_QUICK_REFERENCE.md)** - Quick URL cheat sheet
4. **[QUICK_FIX_ADMIN_CSS.md](QUICK_FIX_ADMIN_CSS.md)** - 🚨 **FIX:** Admin CSS not loading on server
5. **[STATIC_FILES_FIX.md](STATIC_FILES_FIX.md)** - Complete guide to fixing static files in production
6. **[ATTENDANCE_NOTIFICATION_README.md](ATTENDANCE_NOTIFICATION_README.md)** - Attendance notification system guide
7. **[AUTHENTICATION_README.md](AUTHENTICATION_README.md)** - Authentication system documentation
8. **[LOGIN_PROTECTION_README.md](LOGIN_PROTECTION_README.md)** - Login protection guide
9. **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Recent implementation summary
10. **[QUICK_START_NOTIFICATIONS.md](QUICK_START_NOTIFICATIONS.md)** - Quick start for notifications

### ⚠️ Important Notice

**Not all modules are fully implemented!** Some modules have URL routes defined but show "under development" messages. Please check [MODULE_STATUS.md](MODULE_STATUS.md) to see which features are currently functional.

---

## 🚀 Getting Started

### For Administrators
1. Login at `/accounts/login/`
2. Access Django admin panel at `/admin/`
3. Create user accounts at `/admin/auth/user/add/`
4. Assign roles/permissions at `/admin/auth/group/`
5. Manage all system data through admin interface

### For Staff
1. Login with provided credentials
2. Access dashboard at `/`
3. Navigate to required module from menu
4. Use search and filters for quick access

### For Teachers/Faculty
1. Login to faculty portal at `/faculty/`
2. Mark attendance
3. Submit leave requests
4. View payment history

---

## 🔧 Configuration

### Email Configuration (for Absence Notifications)

**Development (Default):**
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**Production:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

See [ATTENDANCE_NOTIFICATION_README.md](ATTENDANCE_NOTIFICATION_README.md) for detailed configuration.

---

## 🧪 Testing

### Test Attendance Notifications
```bash
python manage.py test_absence_notification --student-id 1
```

### Run Django Tests
```bash
python manage.py test
```

---

## 📝 Management Commands

### Custom Management Commands

```bash
# Test absence notification
python manage.py test_absence_notification --student-id <id>

# Create dummy course fee data
python manage.py create_dummy_coursefee_data

# Create sample kits
python manage.py create_sample_kits

# Create sample marks data
python manage.py create_sample_marks_data
```

---

## 🔍 Common Tasks

### Add a New Student
1. Navigate to `/students/create/`
2. Fill in student information
3. Save as draft or submit directly

### Mark Attendance
1. Go to `/attendance/create/` for individual
2. Or `/attendance/bulk/` for multiple students
3. Select date and mark status
4. Parents receive email if marked absent

### Enroll Student in Course
1. Navigate to `/coursefee/enrollments/create/`
2. Select student and course
3. System will check capacity and requirements
4. Submit to complete enrollment

### Record Payment
1. Go to `/coursefee/payments/create/`
2. Select enrollment
3. Enter amount and payment details
4. Receipt generated automatically

### Generate Reports
- Attendance: `/attendance/report/`
- Financial: `/coursefee/reports/financial/`
- Student Performance: `/marks/reports/student/`

---

## 🐛 Troubleshooting

### Common Issues

**Issue: Admin CSS not loading (admin page has no styling)** 🚨
- **Solution:** See [QUICK_FIX_ADMIN_CSS.md](QUICK_FIX_ADMIN_CSS.md) for immediate fix
- Quick fix: Install WhiteNoise, run `collectstatic`, update MIDDLEWARE
- Detailed guide: [STATIC_FILES_FIX.md](STATIC_FILES_FIX.md)

**Issue: Cannot access admin panel**
- Solution: Create superuser with `python manage.py createsuperuser`

**Issue: Emails not sending**
- Solution: Check email configuration in `settings.py`
- For development, emails print to console

**Issue: Missing templates**
- Solution: Ensure all template files exist in respective app's template folders

**Issue: Static files not loading**
- Solution: Run `python manage.py collectstatic`
- For production: Install WhiteNoise or configure nginx/Apache

---

## 📞 Support

### Getting Help
- Check documentation files in the project root
- Review URL reference guides
- Check audit logs for error tracking
- Contact system administrator

### Reporting Issues
1. Navigate to `/system/security/` for security issues
2. Check `/system/audit/` for action logs
3. Use `/system/monitoring/errors/` for error monitoring

---

## 🔄 Version History

### Version 1.0 (December 2025)
- Initial release
- Complete student management system
- Attendance tracking with parent notifications
- Course fee management
- Marks management
- Faculty management
- Batch management
- Transport management
- Kit materials management
- Broadcast and lead management
- System administration

---

## 📋 Project Structure

```
edupulse/
├── accounts/              # Authentication module
├── xstudent/              # Student & attendance management
├── xcoursefee/            # Course fees & payments
├── xmark/                 # Marks & grades
├── xtrainer/              # Faculty management
├── xbatch/                # Batch management
├── xtransport/            # Transport management
├── xkit/                  # Kit materials
├── xbroadcast/            # Communication
├── xadmin/                # System administration
├── edupulse/              # Main project settings
├── media/                 # Uploaded files
├── staticfiles/           # Static files
├── templates/             # Shared templates
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

---

## 🤝 Contributing

This is a private school management system. For contribution guidelines, contact the development team.

---

## 📄 License

Proprietary - All rights reserved.

---

## 👥 Credits

Developed for EduPulse School Management  
December 2025

---

## 📞 Contact

For support or inquiries:
- System Administrator
- Development Team

---

**EduPulse** - Empowering Education Through Technology 🎓

---

*Last Updated: December 3, 2025*

