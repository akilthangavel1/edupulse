# Backup Class Email Notifications - Complete System

## 📧 Overview

Comprehensive email notification system for backup class schedules. Automatically sends emails to backup faculty and students at key points in the backup class lifecycle.

---

## 🎯 When Emails Are Sent

### 1. ✅ When Backup Schedule is Created

**Triggers:** Immediately when a new backup schedule is created

#### **📧 Email to Backup Faculty**
- **Subject:** `Backup Class Assignment - [Course] on [Date]`
- **Content:**
  - Assignment notification
  - Course and class details
  - Date, time, and location
  - Original faculty information
  - Action required (confirm availability)

#### **📧 Email to Students/Parents**
- **Subject:** `Class Update - Substitute Teacher for [Course]`
- **Content:**
  - Substitute teacher announcement
  - Course and schedule details
  - Backup faculty information
  - Class will proceed normally

---

### 2. ✅ When Backup is Confirmed

**Triggers:** When backup faculty confirms the assignment

#### **📧 Confirmation Email to Backup Faculty**
- **Subject:** `Backup Class Confirmed - [Course] on [Date]`
- **Content:**
  - Confirmation acknowledgment
  - Confirmed class details
  - Reminder notification promise
  - Contact information

#### **📧 Reminder to Students/Parents**
- **Subject:** `Class Update - Substitute Teacher for [Course]`
- **Content:**
  - Confirmed substitute teacher
  - Updated class information
  - Reassurance about class continuity

---

### 3. ⏰ Day Before Backup Class

**Triggers:** Run daily via management command (automated)

#### **📧 Reminder to Backup Faculty**
- **Subject:** `Reminder: Backup Class Tomorrow - [Course]`
- **Content:**
  - Tomorrow's class reminder
  - Complete schedule details
  - Preparation tips
  - Room/location information

#### **📧 Reminder to Students/Parents**
- **Subject:** `Reminder: Substitute Teacher Tomorrow - [Course]`
- **Content:**
  - Tomorrow's substitute reminder
  - Class timing confirmation
  - What to bring
  - Important notices

---

## 🚀 How It Works

### **Workflow:**

```
1. Admin Creates Backup Schedule
   ↓
   ✉️ Email sent to Backup Faculty
   ✉️ Email sent to Students/Parents
   ↓
2. Backup Faculty Confirms
   ↓
   ✉️ Confirmation email to Faculty
   ✉️ Reminder email to Students
   ↓
3. Day Before Class (Automated)
   ↓
   ✉️ Reminder to Backup Faculty
   ✉️ Reminder to Students/Parents
   ↓
4. Class Happens
```

---

## 📋 Setup & Usage

### **Creating a Backup Schedule (Sends Emails Automatically)**

1. Navigate to **Faculty → Backup Schedules**
2. Click **"Create Backup Schedule"**
3. Fill in the form:
   - Select original faculty
   - Select backup faculty
   - Choose course
   - Set date and time
   - Add batch name and location
   - Add notes (optional)
4. Click **"Create & Send Notifications"**
5. **Automatic Actions:**
   - ✅ Schedule saved to database
   - ✅ Email sent to backup faculty
   - ✅ Email sent to all students/parents
   - ✅ Success message with status

### **Confirming a Backup Schedule**

1. Navigate to backup schedule detail page
2. Click **"Confirm Backup"** button
3. **Automatic Actions:**
   - ✅ Schedule marked as confirmed
   - ✅ Confirmation email to backup faculty
   - ✅ Reminder email to students

### **Sending Day-Before Reminders (Automated)**

**Run via Management Command:**

```bash
# Test (dry run - no emails sent)
python manage.py send_backup_reminders --dry-run

# Actually send reminders
python manage.py send_backup_reminders
```

**Set up Cron Job (Linux/Mac):**

```bash
# Edit crontab
crontab -e

# Add this line to run every day at 6 PM
0 18 * * * cd /path/to/edupulse && source venv/bin/activate && python manage.py send_backup_reminders
```

**For Windows (Task Scheduler):**
1. Create a batch file `send_reminders.bat`:
   ```batch
   cd C:\path\to\edupulse
   call venv\Scripts\activate
   python manage.py send_backup_reminders
   ```
2. Schedule in Task Scheduler to run daily at 6 PM

---

## 📧 Email Templates

### **4 Email Templates Created:**

1. **`backup_assignment.html`**
   - Initial assignment notification to backup faculty
   - Purple gradient header
   - Complete class details
   - Action required notice

2. **`backup_student_notification.html`**
   - Student/parent notification about substitute
   - Purple gradient header
   - Class continuity reassurance
   - Info box with important details

3. **`backup_confirmation.html`**
   - Confirmation to backup faculty
   - Green gradient header (success theme)
   - Thank you message
   - Confirmed details

4. **`backup_reminder_faculty.html`**
   - Day-before reminder to faculty
   - Red/orange gradient header (urgent theme)
   - Tomorrow's class details
   - Preparation tips

5. **`backup_reminder_student.html`**
   - Day-before reminder to students
   - Blue gradient header
   - Tomorrow's substitute reminder
   - What to bring checklist

---

## 📁 Files Created/Modified

### **New Files:**

1. **`xtrainer/email_notifications.py`**
   - Email sending utilities
   - 5 main functions for different notifications
   - Error handling and logging

2. **Email Templates** (5 files):
   - `xtrainer/templates/xtrainer/email/backup_assignment.html`
   - `xtrainer/templates/xtrainer/email/backup_student_notification.html`
   - `xtrainer/templates/xtrainer/email/backup_confirmation.html`
   - `xtrainer/templates/xtrainer/email/backup_reminder_faculty.html`
   - `xtrainer/templates/xtrainer/email/backup_reminder_student.html`

3. **Management Command:**
   - `xtrainer/management/commands/send_backup_reminders.py`
   - Sends day-before reminders
   - Supports dry-run mode

4. **Templates:**
   - `xtrainer/templates/xtrainer/backup_schedule_form.html`
   - `xtrainer/templates/xtrainer/backup_schedule_detail.html`

### **Modified Files:**

1. **`xtrainer/views.py`**
   - Added email notification imports
   - Updated `backup_schedule_create()` - sends emails on creation
   - Added `backup_schedule_confirm()` - sends emails on confirmation
   - Updated `backup_schedule_detail()` - shows confirm button

2. **`xtrainer/urls.py`**
   - Added confirm URL: `/backup-schedules/<id>/confirm/`

---

## ⚙️ Configuration

### **Email Settings (Already Configured)**

The system uses Django's email backend from `settings.py`:

**Development Mode:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Emails printed to console for testing
```

**Production Mode:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'EduPulse <noreply@edupulse.com>'
```

---

## 🧪 Testing

### **Test in Development:**

1. **Create a Backup Schedule:**
   ```bash
   # Start server
   python manage.py runserver
   
   # Go to browser: http://127.0.0.1:8000/faculty/backup-schedules/create/
   # Fill form and submit
   # Check terminal for email output
   ```

2. **Test Day-Before Reminders:**
   ```bash
   # Dry run (no emails)
   python manage.py send_backup_reminders --dry-run
   
   # Actually send (check console output)
   python manage.py send_backup_reminders
   ```

### **Verify Emails:**

In development mode, check the terminal/console where your Django server is running. You'll see:
- Email headers (To, From, Subject)
- Full email content (HTML)
- Confirmation of sending

---

## 📊 Email Recipients

### **Backup Faculty Email:**
- Sent to: `backup_faculty.email`
- Must have valid email in faculty profile

### **Student/Parent Emails:**
- Sent to: Father's email + Mother's email (from student records)
- Uses BCC to protect privacy
- Gets all enrolled students for the course
- Collects both parents' emails
- Removes duplicates automatically

---

## ✨ Features

### ✅ **Automatic Notifications**
- No manual email composition needed
- Triggered automatically on key actions
- Professional HTML templates
- Error handling with fallbacks

### ✅ **Smart Recipient Management**
- Finds all enrolled students
- Collects parent emails
- Uses BCC for privacy
- Handles missing emails gracefully

### ✅ **Professional Templates**
- Branded HTML design
- Gradient headers
- Responsive layout
- Clear information hierarchy
- Action items highlighted

### ✅ **Multiple Notification Points**
1. On creation
2. On confirmation
3. Day before class

### ✅ **Management Command**
- Automated reminder sending
- Dry-run mode for testing
- Detailed console output
- Error tracking

### ✅ **Status Tracking**
- Tracks if emails sent
- Records notification date
- Shows in detail page
- Visual badges for status

---

## 📱 User Interface

### **Backup Schedule Detail Page Shows:**

- ✅ Confirm button (if pending)
- ✅ Notification status section:
  - Backup faculty notified? (Yes/No badge)
  - Students notified? (Yes/No badge)
  - Notification date/time
- ✅ Complete schedule information
- ✅ Faculty contact details
- ✅ Status badges

### **Create Form Shows:**

- ℹ️ Info alert: "Emails will be automatically sent..."
- All schedule fields
- Clear labels and validation
- "Create & Send Notifications" button

---

## 🎯 Email Content Summary

### **Assignment Email (to Backup Faculty)**
```
Subject: Backup Class Assignment - Mathematics on Dec 15, 2025

Dear John Doe,

You have been assigned as a backup teacher...

Class Details:
- Course: Mathematics
- Original Faculty: Jane Smith
- Date: Friday, December 15, 2025
- Time: 9:00 AM - 11:00 AM
- Batch: Morning Batch

⚠️ Action Required: Please confirm your availability...
```

### **Student Notification**
```
Subject: Class Update - Substitute Teacher for Mathematics

Dear Parents/Guardians,

A substitute teacher will be taking tomorrow's class...

Class Information:
- Regular Teacher: Jane Smith
- Substitute Teacher: John Doe
- Date: Friday, December 15, 2025
- Time: 9:00 AM - 11:00 AM

ℹ️ Class will proceed as scheduled...
```

### **Reminder (Day Before)**
```
Subject: Reminder: Backup Class Tomorrow - Mathematics

⚠️ Reminder: Your backup class is TOMORROW!

Class Tomorrow:
- Course: Mathematics
- Date: Friday, December 15, 2025
- Time: 9:00 AM - 11:00 AM

Preparation Tips:
✓ Review course materials
✓ Arrive 10 minutes early
✓ Coordinate with original faculty
```

---

## 🔧 Troubleshooting

### **Emails Not Sending**

**Check:**
1. ✅ Backup faculty has email in profile
2. ✅ Students have parent emails in records
3. ✅ Email settings configured in `settings.py`
4. ✅ Email backend is correct for your environment

**Solution:**
- View schedule detail page → Check notification status
- Look for error messages in success notifications
- Check console/terminal for email output (development)

### **No Student Emails Sent**

**Check:**
1. ✅ Course has enrolled students
2. ✅ Students have active enrollments
3. ✅ Parent emails filled in student records

**Solution:**
- Go to student records and add parent emails
- Re-send notifications if needed

### **Reminders Not Sending**

**Check:**
1. ✅ Management command is scheduled
2. ✅ Cron job is running
3. ✅ Virtual environment is activated in cron

**Solution:**
- Test command manually first
- Use `--dry-run` to debug
- Check system logs

---

## 🔄 Manual Operations

### **Resend Notifications:**

From Django Admin:
1. Go to **Admin Panel → Backup Schedules**
2. Select schedules
3. Actions → "Send notifications for selected schedules"
4. Marks as sent (for tracking)

### **Check Notification Logs:**

From Django Admin:
1. Go to **Admin Panel → Notification Logs**
2. View all sent notifications
3. Filter by type, status, recipient

---

## 📅 Automation Setup

### **Daily Reminder Command**

**Purpose:** Send reminders for tomorrow's backup classes

**Recommended Time:** 6:00 PM daily

**Linux/Mac Cron:**
```bash
# Run every day at 6 PM
0 18 * * * cd /Users/akil/Desktop/kuwait\ project/edupulse && source venv/bin/activate && python manage.py send_backup_reminders >> /tmp/backup_reminders.log 2>&1
```

**Windows Task Scheduler:**
- Task name: "Backup Class Reminders"
- Trigger: Daily at 6:00 PM
- Action: Run `send_reminders.bat`

**Docker/Server:**
```bash
# Add to crontab
docker exec edupulse python manage.py send_backup_reminders
```

---

## 📊 Notification Tracking

### **In Backup Schedule Detail:**

Visual indicators show:
- ✅ **Backup Faculty Notified** (Green badge if sent)
- ✅ **Students Notified** (Green badge if sent)
- 📅 **Notification Date** (Timestamp of first send)

### **In Database:**

Fields tracked:
- `notification_sent_to_backup` (Boolean)
- `notification_sent_to_students` (Boolean)
- `notification_date` (DateTime)

---

## 💡 Best Practices

### **For Administrators:**

1. ✅ Create backup schedules as early as possible
2. ✅ Verify backup faculty email before creating
3. ✅ Check notification status after creation
4. ✅ Ensure students have parent emails
5. ✅ Set up automated reminders via cron
6. ✅ Monitor notification logs regularly

### **For Backup Faculty:**

1. ✅ Confirm assignment promptly
2. ✅ Check email regularly
3. ✅ Prepare materials in advance
4. ✅ Coordinate with original faculty
5. ✅ Arrive early on backup day

### **Email Timing:**

- **Creation Emails:** Immediate (as soon as schedule created)
- **Confirmation Emails:** Immediate (when confirmed)
- **Reminders:** 6 PM day before (via cron)

---

## 🎨 Email Design Features

All emails include:
- ✅ Gradient headers with branding
- ✅ Clear, professional layout
- ✅ Responsive design (mobile-friendly)
- ✅ Color-coded sections
- ✅ EduPulse branding
- ✅ Important info highlighted
- ✅ Contact information
- ✅ Professional footer

---

## 🔐 Privacy & Security

- **BCC for Students:** Parent emails use BCC (blind carbon copy)
- **No Spam:** Professional emails with unsubscribe info
- **Secure Delivery:** Uses TLS encryption
- **Data Protection:** Only sends to verified addresses
- **Consent:** Parents aware of school communications

---

## 📈 Success Metrics

Track effectiveness:
- **Email Delivery Rate:** % of emails successfully sent
- **Confirmation Rate:** % of backup faculty confirming
- **Reminder Effectiveness:** Class attendance after notification
- **Parent Satisfaction:** Feedback on communication

---

## 🔮 Future Enhancements

- [ ] SMS notifications option
- [ ] WhatsApp integration
- [ ] In-app notifications
- [ ] Email templates customization UI
- [ ] Notification preferences per user
- [ ] Read receipts tracking
- [ ] Mobile app push notifications
- [ ] Calendar integration (iCal invites)

---

## 📞 Support

### **Common Questions:**

**Q: Can I disable automatic emails?**  
A: Not currently, but can be added as a setting

**Q: Can parents opt-out?**  
A: Coming in future updates

**Q: What if backup faculty doesn't have email?**  
A: Email won't be sent, but schedule is still created

**Q: How do I customize email content?**  
A: Edit templates in `xtrainer/templates/xtrainer/email/`

**Q: Can I see who received emails?**  
A: Check notification status in schedule details

**Q: What if email fails?**  
A: System shows warning message; schedule is still saved

---

## 🎯 Quick Reference

### **URLs:**
- **List:** `/faculty/backup-schedules/`
- **Create:** `/faculty/backup-schedules/create/`
- **Detail:** `/faculty/backup-schedules/<id>/`
- **Confirm:** `/faculty/backup-schedules/<id>/confirm/`

### **Management Commands:**
```bash
# Send tomorrow's reminders
python manage.py send_backup_reminders

# Test without sending
python manage.py send_backup_reminders --dry-run
```

### **Email Types:**
1. Assignment → Backup Faculty
2. Notification → Students/Parents
3. Confirmation → Backup Faculty
4. Confirmation Reminder → Students
5. Day-Before → Backup Faculty
6. Day-Before → Students/Parents

---

## ✅ Implementation Checklist

- [x] Email notification utilities created
- [x] 5 HTML email templates designed
- [x] Backup creation sends emails
- [x] Confirmation endpoint created
- [x] Confirmation sends emails
- [x] Management command for reminders
- [x] Detail page shows notification status
- [x] Form template created
- [x] URLs configured
- [x] Error handling implemented
- [x] Success messages with status
- [x] Documentation complete

---

## 🎉 Ready to Use!

**Everything is implemented and ready:**

1. ✅ Create backup schedule → Emails sent automatically
2. ✅ Confirm backup → Emails sent automatically
3. ✅ Run reminder command → Day-before emails sent
4. ✅ All templates professional and branded
5. ✅ Full error handling
6. ✅ Status tracking

**Just configure your SMTP settings for production and you're good to go!** 📧

---

**Last Updated:** December 2025  
**Version:** 1.0  
**Status:** ✅ Production Ready  
**Module:** Faculty/Trainer Management - Backup Schedules

