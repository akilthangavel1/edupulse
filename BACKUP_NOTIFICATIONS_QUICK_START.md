# Backup Class Notifications - Quick Start Guide

## 🎯 Three Automatic Email Triggers

### 1. 📧 When Backup Schedule is Created

**What Happens:**
- Admin creates backup schedule
- System **AUTOMATICALLY** sends 2 emails:

#### Email 1: To Backup Faculty ✉️
- **Subject:** Backup Class Assignment
- **Message:** You've been assigned to cover [Course]
- **Includes:** Date, time, location, original faculty
- **Action:** Please confirm availability

#### Email 2: To Students/Parents ✉️
- **Subject:** Class Update - Substitute Teacher
- **Message:** Substitute teacher for [Course]
- **Includes:** Who's covering, when, where
- **Reassurance:** Class proceeds normally

---

### 2. ✅ When Backup is Confirmed

**What Happens:**
- Backup faculty clicks "Confirm Backup" button
- System **AUTOMATICALLY** sends 2 emails:

#### Email 1: Confirmation to Backup Faculty ✉️
- **Subject:** Backup Class Confirmed
- **Message:** Thank you for confirming
- **Includes:** Confirmed details
- **Promise:** Reminder coming tomorrow

#### Email 2: Reminder to Students/Parents ✉️
- **Subject:** Class Update - Substitute Teacher
- **Message:** Confirmed substitute teacher
- **Includes:** Updated class info
- **Note:** Class will run normally

---

### 3. ⏰ Day Before Backup Class

**What Happens:**
- Automated command runs daily at 6 PM
- System **AUTOMATICALLY** sends 2 emails:

#### Email 1: Reminder to Backup Faculty ✉️
- **Subject:** Reminder: Backup Class Tomorrow
- **Message:** Your backup class is TOMORROW
- **Includes:** Complete schedule
- **Tips:** Preparation guidelines

#### Email 2: Reminder to Students/Parents ✉️
- **Subject:** Reminder: Substitute Teacher Tomorrow
- **Message:** Substitute teacher tomorrow
- **Includes:** Class details
- **Checklist:** What to bring

---

## 🚀 How to Use

### **Step 1: Create Backup Schedule**

1. Go to: `http://127.0.0.1:8000/faculty/backup-schedules/create/`
2. Fill in:
   - Original faculty (who's away)
   - Backup faculty (who will cover)
   - Course
   - Date and time
   - Batch name
   - Room location
3. Click **"Create & Send Notifications"**
4. ✅ Emails sent automatically!

**You'll see:**
```
✓ Backup schedule BKP-202412-0001 created! 
  Email notifications sent to backup faculty and students.
```

---

### **Step 2: Backup Faculty Confirms**

1. Backup faculty goes to schedule detail page
2. Clicks **"Confirm Backup"** button
3. ✅ Confirmation emails sent automatically!

**You'll see:**
```
✓ Backup schedule confirmed! 
  Confirmation emails sent to you and students.
```

---

### **Step 3: Automated Day-Before Reminders**

**Setup Once:**

```bash
# Add to crontab (runs daily at 6 PM)
crontab -e

# Add this line:
0 18 * * * cd /Users/akil/Desktop/kuwait\ project/edupulse && source venv/bin/activate && python manage.py send_backup_reminders
```

**Test Manually:**

```bash
# Test without sending
python manage.py send_backup_reminders --dry-run

# Actually send reminders
python manage.py send_backup_reminders
```

---

## 📊 Email Flow Diagram

```
CREATE BACKUP SCHEDULE
        ↓
   ✉️ Email → Backup Faculty (Assignment)
   ✉️ Email → Students (Substitute Notice)
        ↓
BACKUP FACULTY CONFIRMS
        ↓
   ✉️ Email → Backup Faculty (Confirmation)
   ✉️ Email → Students (Reminder)
        ↓
DAY BEFORE CLASS (6 PM)
        ↓
   ✉️ Email → Backup Faculty (Tomorrow Reminder)
   ✉️ Email → Students (Tomorrow Reminder)
        ↓
CLASS HAPPENS ✓
```

---

## ✅ Quick Checklist

**Before Creating Backup:**
- [ ] Backup faculty profile has email address
- [ ] Students enrolled in course
- [ ] Parent emails in student records
- [ ] Email settings configured

**After Creating Backup:**
- [ ] Check success message
- [ ] Verify "emails sent" confirmation
- [ ] View detail page for notification status
- [ ] Backup faculty confirms assignment

**Setup Automation:**
- [ ] Test reminder command manually
- [ ] Set up cron job for daily reminders
- [ ] Test with dry-run first
- [ ] Monitor logs for errors

---

## 🎯 Email Recipients

| Email Type | Sent To | When |
|------------|---------|------|
| Assignment | Backup Faculty | On creation |
| Substitute Notice | All Parents | On creation |
| Confirmation | Backup Faculty | On confirm |
| Confirm Reminder | All Parents | On confirm |
| Faculty Reminder | Backup Faculty | Day before (6 PM) |
| Student Reminder | All Parents | Day before (6 PM) |

---

## 📧 Email Addresses Used

**Backup Faculty:**
- `backup_faculty.email` from Faculty model

**Students/Parents:**
- `student.father_email_id` (if exists)
- `student.mother_email_id` (if exists)
- Sent via BCC (privacy protected)
- Duplicates removed automatically

---

## 🎨 What Emails Look Like

All emails have:
- 🎨 **Professional Design:** Gradient headers, clean layout
- 📱 **Mobile Friendly:** Responsive HTML
- 🏫 **Branded:** EduPulse logo and colors
- ✅ **Clear Info:** Easy to read and understand
- 📞 **Contact Info:** How to get help

---

## 🔧 Testing Your Setup

### **Test Email Sending:**

```bash
# 1. Create a backup schedule via web interface
# 2. Check terminal output for emails
# 3. Verify content looks correct
```

### **Test Reminder Command:**

```bash
# Create a backup for tomorrow
# Then run:
python manage.py send_backup_reminders --dry-run

# Should show:
# Found 1 backup schedule(s) for 2025-12-XX
# [DRY RUN] Would send reminders for: BKP-...
```

### **Test in Production:**

1. Configure SMTP settings
2. Create test backup with your email
3. Check inbox for notification
4. Confirm and check for confirmation email
5. Run reminder command day before

---

## 🎉 Summary

**You now have:**
✅ Automatic emails when creating backup  
✅ Automatic emails when confirming backup  
✅ Automated day-before reminders  
✅ Professional HTML email templates  
✅ Complete notification tracking  
✅ Management command for automation  
✅ Error handling and logging  

**Total Email Touchpoints:** 6 emails per backup schedule
- 2 on creation
- 2 on confirmation  
- 2 day before class

**Everything is automated and ready to use!** 🚀

---

**Created:** December 2025  
**Status:** ✅ Fully Implemented  
**Module:** Faculty Backup Class Notifications

