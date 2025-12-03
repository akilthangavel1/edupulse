# Quick Start Guide - Attendance Notifications

## Setup Complete! ✓

The attendance notification system is now installed and active. Here's what you need to know:

## What's Been Installed

1. **Automatic Email Notifications** - Parents receive emails when their child is marked absent
2. **Signal-Based System** - Notifications trigger automatically when attendance is saved
3. **Email Templates** - Professional HTML email template included
4. **Testing Tools** - Management command for testing the system
5. **Documentation** - Complete documentation in `ATTENDANCE_NOTIFICATION_README.md`

## Quick Test (Development Mode)

### 1. Start the Development Server
```bash
python manage.py runserver
```

### 2. Test via Web Interface
1. Go to the attendance marking page
2. Mark a student as "absent"
3. Save the record
4. Check the terminal where Django is running - you'll see the email printed there

### 3. Test via Management Command
```bash
# List available students
python manage.py test_absence_notification

# Create test absence for a specific student
python manage.py test_absence_notification --student-id 1
```

## For Production Use

### Enable Real Email Sending

Edit `edupulse/settings.py` and update these lines:

#### For Gmail:
```python
# Comment out the console backend
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Uncomment and configure SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Generate at https://myaccount.google.com/apppasswords
```

#### For Office 365:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@outlook.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

## How to Use

### Individual Attendance
1. Navigate to: Attendance → Mark Attendance
2. Select student, date, and status
3. If status is "absent", parents will automatically receive email
4. You'll see a confirmation message: "Absence notification email sent to parents"

### Bulk Attendance
1. Navigate to: Attendance → Bulk Mark Attendance
2. Select date and filters (grade, program)
3. Mark students as present/absent
4. Submit the form
5. You'll see: "Absence notifications sent to parents of X student(s)"

## What Parents Receive

**Email Subject:** `Absence Notification - [Student Name] - [Date]`

**Email Content:**
- Student name, grade, and program
- Date of absence
- Who recorded the attendance
- Any additional notes
- Contact information for the school

**Recipients:**
- Father's email address
- Mother's email address
(Both emails from student's profile)

## Important Notes

✅ **Works Automatically** - No manual action needed after marking attendance

✅ **Dual Notification** - Both parents receive the email

✅ **Safe Failure** - If email fails, attendance is still recorded

⚠️ **Email Addresses Required** - Ensure all students have valid parent emails

⚠️ **Development Mode** - By default, emails print to console, not sent

## Troubleshooting

### "No parent email addresses found"
- Update the student's profile to include father_email_id and mother_email_id

### "Emails not appearing in console"
- Check the terminal where `runserver` is running
- Emails appear after marking student as absent

### "Emails not being sent in production"
- Verify SMTP settings in settings.py
- Test with: `python manage.py test_absence_notification --student-id 1`
- Check email provider settings (allow less secure apps, app passwords, etc.)

## Files Created

1. `xstudent/signals.py` - Notification logic
2. `xstudent/templates/xstudent/emails/absence_notification.html` - Email template
3. `xstudent/management/commands/test_absence_notification.py` - Testing command
4. `ATTENDANCE_NOTIFICATION_README.md` - Full documentation
5. `QUICK_START_NOTIFICATIONS.md` - This file

## Need More Help?

📖 Read the full documentation: `ATTENDANCE_NOTIFICATION_README.md`

🔧 Test the system: `python manage.py test_absence_notification`

📧 Check email configuration in `edupulse/settings.py`

## Next Steps

1. ✅ Test in development mode
2. ✅ Verify parent email addresses in student records
3. ✅ Configure SMTP settings for production
4. ✅ Test with real email addresses
5. ✅ Monitor email delivery logs

---

**System Status:** ✓ Active and Ready

The notification system is now monitoring all attendance records. When a student is marked absent, parents will be notified automatically.

