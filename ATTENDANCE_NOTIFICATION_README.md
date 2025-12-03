# Attendance Notification System

## Overview
The EduPulse system automatically sends email notifications to parents when their child is marked as **absent** during attendance marking. This feature ensures that parents are immediately informed about their child's absence from school.

## How It Works

### Automatic Notifications
When a teacher or administrator marks a student as "absent" in the attendance system, an email notification is automatically sent to both parents (father and mother) using the email addresses stored in the student's profile.

### Trigger Points
Absence notifications are triggered in the following scenarios:
1. **Individual Attendance Marking** - When marking attendance for a single student
2. **Bulk Attendance Marking** - When marking attendance for multiple students at once
3. **Attendance Update** - When updating an existing attendance record from any status to "absent"

### Email Recipients
Notifications are sent to:
- **Father's Email**: `student.father_email_id`
- **Mother's Email**: `student.mother_email_id`

Both parents receive the notification simultaneously. If either email is missing, the notification is still sent to the available email address(es).

## Email Content

### Information Included
Each absence notification email contains:
- Student's full name
- Grade and program
- Date of absence
- Name of the person who recorded the attendance
- Any additional notes entered by the teacher/administrator

### Email Format
- **Subject**: `Absence Notification - [Student Name] - [Date]`
- **Format**: Both HTML (styled) and plain text versions
- **From**: EduPulse School Management (`noreply@edupulse.com`)

### Sample Email
```
Dear [Father Name] and [Mother Name],

This is to inform you that your child, [Student Name], was marked absent on [Date].

Student Details:
- Name: [Student Name]
- Grade: [Grade]
- Program: [Program]
- Date of Absence: [Date]

Additional Notes:
[Any notes entered by the teacher]

If this absence was unexpected or if you have any questions, please contact 
the school administration immediately.

Best regards,
EduPulse School Management
```

## Configuration

### Email Backend Setup

#### Development Mode (Default)
By default, the system uses console email backend, which prints emails to the terminal instead of sending them. This is useful for testing.

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

#### Production Mode (Real Email Sending)
To enable actual email sending, update the following settings in `edupulse/settings.py`:

##### For Gmail:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use App Password, not regular password
```

**Note**: For Gmail, you need to generate an [App Password](https://support.google.com/accounts/answer/185833) instead of using your regular password.

##### For Office 365/Outlook:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@outlook.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

##### For SendGrid:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
```

## Testing the Notification System

### Method 1: Using Management Command
Test the notification system without affecting real attendance data:

```bash
# Test with a specific student ID
python manage.py test_absence_notification --student-id 1

# Resend notification for an existing absence record
python manage.py test_absence_notification --attendance-id 5

# View available students
python manage.py test_absence_notification
```

### Method 2: Through the Web Interface
1. Navigate to the attendance marking page
2. Mark a student as "absent"
3. Save the attendance record
4. Check the console (development) or email inbox (production) for the notification

### Method 3: Using Django Shell
```python
python manage.py shell

from xstudent.models import NewStudent, Attendance
from datetime import date

# Get a student
student = NewStudent.objects.first()

# Create absence record
attendance = Attendance.objects.create(
    student=student,
    date=date.today(),
    status='absent',
    notes='Test notification'
)

# The notification will be sent automatically
```

## Technical Implementation

### Signal-Based Architecture
The notification system uses Django signals for automatic triggering:

```python
# xstudent/signals.py
@receiver(post_save, sender=Attendance)
def send_absence_notification(sender, instance, created, **kwargs):
    if instance.status == 'absent':
        # Send email to parents
        ...
```

### Files Involved
1. **`xstudent/signals.py`** - Signal handlers for automatic notification
2. **`xstudent/apps.py`** - Registers signals when app is ready
3. **`xstudent/templates/xstudent/emails/absence_notification.html`** - HTML email template
4. **`xstudent/management/commands/test_absence_notification.py`** - Testing command
5. **`edupulse/settings.py`** - Email configuration

## Troubleshooting

### Notifications Not Sending

#### Issue: No emails appearing in console (development mode)
**Solution**: Check that you're running the development server and looking at the terminal output where `python manage.py runserver` is running.

#### Issue: No emails being sent (production mode)
**Possible causes**:
1. Email backend not configured correctly
2. SMTP credentials are incorrect
3. Email provider blocking the connection
4. Firewall blocking SMTP port (587 or 465)

**Debug steps**:
```python
# Test email configuration in Django shell
python manage.py shell

from django.core.mail import send_mail
send_mail(
    'Test Subject',
    'Test message',
    'noreply@edupulse.com',
    ['recipient@example.com'],
    fail_silently=False,
)
```

### Missing Parent Email Addresses

If a student record doesn't have parent email addresses, the notification will not be sent. Ensure all student records have:
- `father_email_id` - Father's email address
- `mother_email_id` - Mother's email address

### Check Logs

Monitor the application logs for notification status:
```bash
# The system logs notification attempts
# Look for messages like:
# "Absence notification sent to parents of [Student Name] for date [Date]"
# "Failed to send absence notification for [Student Name]: [Error]"
```

## Customization

### Modify Email Template
Edit `xstudent/templates/xstudent/emails/absence_notification.html` to customize:
- Email styling
- Content layout
- Additional information to include

### Modify Email Content
Edit the `send_absence_notification` function in `xstudent/signals.py` to customize:
- Email subject line
- Message text
- Context variables
- Recipient logic

### Disable Notifications
To temporarily disable absence notifications, comment out the signal import in `xstudent/apps.py`:

```python
def ready(self):
    """Import signals when the app is ready"""
    # import xstudent.signals  # Commented out to disable notifications
```

## Best Practices

1. **Email Validation**: Always ensure parent email addresses are valid when creating student records
2. **Testing**: Test the notification system in development mode before deploying to production
3. **Monitoring**: Regularly check email logs to ensure notifications are being delivered
4. **Backup Recipients**: Consider adding a CC to the school administration email for record-keeping
5. **Privacy**: Ensure compliance with data protection regulations when sending student information via email

## Future Enhancements

Potential improvements for the notification system:
- [ ] SMS notifications in addition to email
- [ ] Notification preferences (allow parents to opt-in/opt-out)
- [ ] Daily/weekly absence summary reports
- [ ] Notification for other attendance statuses (late, excused)
- [ ] Multi-language support for email notifications
- [ ] Notification history log in the admin interface
- [ ] Mobile app push notifications
- [ ] Configurable notification templates through admin interface

## Support

For issues or questions about the attendance notification system:
1. Check this documentation
2. Review the troubleshooting section
3. Check application logs for error messages
4. Test with the management command
5. Contact the system administrator

