# Exam Marks Email Notifications - Complete Guide

## 📧 Overview

Automatic email notification system that sends exam marks to parents when marks are published or updated in the system.

---

## 🎯 When Emails Are Sent

### 1. ✅ When Marks are Published (First Time)

**Trigger:** Creating or editing a mark with status = "Published"

**Email Sent To:**
- Father's email (from student record)
- Mother's email (from student record)

**Email Contains:**
- Student information
- Subject name
- Assessment type
- Marks obtained / Total marks
- Percentage score
- Grade (if calculated)
- Teacher's remarks (if any)

---

### 2. ✅ When Published Marks are Updated

**Trigger:** Editing an already-published mark

**Email Sent To:**
- Father's email
- Mother's email

**Email Contains:**
- "Marks Updated" notification
- Updated marks details
- New percentage and grade
- Updated remarks

---

### 3. 🔄 Manual Resend

**Trigger:** Clicking "Resend Email" button on mark detail page

**Available For:**
- Only published marks
- Sends current mark details
- Useful if parent didn't receive original email

---

## 🚀 How to Use

### **Recording Marks with Email Notification**

#### **Step 1: Create/Edit Mark**
1. Navigate to **Marks → Student Marks**
2. Click **"Add Mark"** or edit existing mark
3. Fill in mark details:
   - Select student
   - Select subject
   - Choose assessment type
   - Enter marks obtained and total marks
   - Select **status = "Published"** (important!)
   - Add remarks (optional)

#### **Step 2: Email Notification Checkbox**
- **Email notification checkbox** is checked by default
- ✅ **Checked**: Email will be sent to parents
- ⬜ **Unchecked**: No email will be sent

#### **Step 3: Save**
- Click **"Save Mark"** or **"Update Mark"**
- System automatically sends email if:
  - Status is "Published"
  - Email checkbox is checked
  - Parent emails exist in student record

#### **Step 4: Confirmation**
You'll see one of these messages:
- ✅ "Mark created and published successfully! Email notification sent to parents."
- ⚠️ "Mark created successfully! However, email notification could not be sent."
- ℹ️ "Mark created successfully!" (if not published or email unchecked)

---

### **Resending Email Notifications**

1. Go to mark detail page
2. Look for **"Resend Email"** button (blue button)
3. Click to resend
4. Confirm the action
5. Email sent to parents

**Note:** Resend button only appears for published marks

---

## 📧 Email Content

### **Published Marks Email**

**Subject:** `Exam Marks Published - [Student Name] - [Subject]`

**Email Layout:**
```
┌─────────────────────────────────────────┐
│  📊 Exam Marks Published                │
│  [Purple Gradient Header]               │
├─────────────────────────────────────────┤
│  Dear [Father] and [Mother],            │
│                                          │
│  STUDENT INFORMATION                     │
│  • Name: John Doe                       │
│  • Admission No: 2025001                │
│  • Grade: Grade 5                       │
│  • Program: Mathematics                 │
│                                          │
│  EXAM RESULTS                            │
│  • Subject: Mathematics                 │
│  • Assessment: Midterm Exam             │
│  • Exam Date: December 5, 2025          │
│                                          │
│  [MARKS OBTAINED]                        │
│      85 / 100                            │
│  [Large Display in Purple Box]          │
│                                          │
│  Percentage: 85.00%                      │
│  Grade: A                                │
│                                          │
│  Teacher's Remarks: Excellent work!     │
├─────────────────────────────────────────┤
│  ℹ️ Note: For concerns, contact school   │
│  Keep Learning: Encourage your child    │
├─────────────────────────────────────────┤
│  EduPulse - Student Management System   │
│  Automated Notification                  │
└─────────────────────────────────────────┘
```

---

### **Updated Marks Email**

**Subject:** `Marks Updated - [Student Name] - [Subject]`

**Content:** Similar to published email, but with "Updated" header

---

## 📋 Status-Based Email Logic

### **Mark Status Options:**

| Status | Email Sent? | When |
|--------|-------------|------|
| **Draft** | ❌ No | Marks being prepared |
| **Submitted** | ❌ No | Submitted for review |
| **Published** | ✅ **YES** | **Visible to parents** |
| **Revised** | ✅ **YES** | Updated published marks |

**Important:** Emails are ONLY sent when status is "Published"!

---

## 💡 Best Practices

### **For Teachers/Staff:**

1. ✅ **Keep draft first**: Enter marks as "Draft" while checking
2. ✅ **Review carefully**: Verify all marks before publishing
3. ✅ **Publish together**: Publish all students' marks at once
4. ✅ **Add remarks**: Include encouraging or constructive feedback
5. ✅ **Check emails**: Ensure student records have parent emails
6. ✅ **Notify students**: Let students know marks are published

### **Mark Entry Workflow:**

```
1. Enter marks → Status: Draft
2. Review marks → Verify accuracy
3. Add remarks → Personalize feedback
4. Change status → Published
5. Check email box → Keep checked
6. Save → Email sent automatically
```

---

## 🔧 Configuration

### **Email Settings (Already Configured)**

Uses settings from `settings.py`:

**Development:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Emails printed to console
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

---

## 📊 Features

### ✅ **Automatic Notifications**
- Triggered when marks published
- No manual email composition
- Professional HTML template
- Both parents receive email

### ✅ **Smart Email Logic**
- Only sends for published marks
- Detects new vs updated marks
- Different email for updates
- Optional email toggle

### ✅ **Rich Email Content**
- Complete mark details
- Visual percentage display
- Grade badge (color-coded)
- Teacher's remarks included
- Student information

### ✅ **Resend Capability**
- Resend from detail page
- Only for published marks
- Confirmation dialog
- Status feedback

### ✅ **Error Handling**
- Graceful failure handling
- Clear error messages
- Marks still saved if email fails
- Missing email warnings

---

## 📁 Files Created/Modified

### **New Files:**

1. **`xmark/email_notifications.py`**
   - Email sending utilities
   - Published notification function
   - Updated notification function
   - Report card function (future use)

2. **Email Templates:**
   - `xmark/templates/xmark/email/marks_notification.html`
   - `xmark/templates/xmark/email/report_card.html`

### **Modified Files:**

1. **`xmark/views.py`**
   - Added email notification imports
   - Updated `mark_create()` - sends email on publish
   - Updated `mark_edit()` - sends email on publish/update
   - Added `mark_resend_email()` - manual resend

2. **`xmark/urls.py`**
   - Added resend email URL pattern

3. **`xmark/templates/xmark/mark_form.html`**
   - Added email notification checkbox
   - Added informative help text

4. **`xmark/templates/xmark/mark_detail.html`**
   - Added "Resend Email" button for published marks

---

## 🧪 Testing

### **Test Email Sending (Development):**

1. **Create a mark entry:**
   - Fill in student, subject, marks
   - Set status to "Published"
   - Keep email checkbox checked
   - Save

2. **Check terminal/console:**
   - Email content will be printed
   - Verify To: addresses
   - Check subject line
   - Review email HTML

3. **Verify success message:**
   - Should say "Email notification sent"

### **Test Resend:**

1. Go to mark detail page
2. Click "Resend Email" button
3. Check terminal for email output

### **Test Update:**

1. Edit a published mark
2. Change marks or remarks
3. Save
4. Check for "update notification sent" message

---

## 🎯 Use Cases

### **Weekly Marks Publication**

1. Teacher enters all marks as "Draft"
2. Reviews and verifies accuracy
3. Changes status to "Published" for all
4. Saves each mark → Emails sent automatically
5. Parents receive individual emails

### **Mark Corrections**

1. Teacher finds error in published mark
2. Edits the mark
3. Updates marks and/or remarks
4. Saves → Update email sent to parents
5. Parents informed of revision

### **Parent Didn't Receive Email**

1. Parent contacts school
2. Staff opens mark detail page
3. Clicks "Resend Email"
4. Email sent again
5. Parent receives notification

---

## 📊 Email Recipients

### **Who Receives Emails:**

For each student mark:
- **Father's Email**: From `student.father_email_id`
- **Mother's Email**: From `student.mother_email_id`
- Both receive same email simultaneously

### **Email Privacy:**

- Each parent gets individual copy
- No email addresses exposed
- Professional from address
- Compliant with privacy regulations

---

## ⚠️ Troubleshooting

### **Email Not Sent**

**Check:**
1. ✅ Mark status is "Published"
2. ✅ Email checkbox was checked
3. ✅ Parent emails exist in student record
4. ✅ Email settings configured correctly

**Solutions:**
- Update student record with parent emails
- Use "Resend Email" button
- Check terminal/logs for errors

### **Wrong Email Content**

**Solutions:**
- Edit email template: `xmark/templates/xmark/email/marks_notification.html`
- Customize subject line in `email_notifications.py`
- Test changes with dry run

### **Parents Complaining About Spam**

**Solutions:**
- Use professional from address
- Don't send too frequently
- Include unsubscribe info (future)
- Configure SPF/DKIM records

---

## ✨ Email Design Features

### **Visual Elements:**

- 🎨 **Gradient Header**: Purple branded header
- 📊 **Large Score Display**: Prominent marks/total
- 📈 **Percentage Badge**: Large percentage display
- 🎖️ **Grade Badge**: Color-coded grade (A, B, C, etc.)
- ℹ️ **Info Boxes**: Highlighted important information
- 📝 **Clean Layout**: Professional, easy to read

### **Color Coding:**

- **Good Grades (≥80%)**: Green
- **Average Grades (50-79%)**: Yellow
- **Needs Improvement (<50%)**: Red

---

## 🔮 Future Enhancements

- [ ] Bulk email for all students in a class
- [ ] Weekly/monthly report card emails
- [ ] SMS notifications option
- [ ] Parent portal to view marks online
- [ ] Email delivery tracking
- [ ] Parent email preferences
- [ ] Customizable email templates
- [ ] Multi-language support
- [ ] Mobile app push notifications

---

## 📞 Common Questions

**Q: Will email be sent if I save as "Draft"?**  
A: No, emails are only sent when status is "Published".

**Q: Can I disable emails for specific marks?**  
A: Yes, uncheck the email notification checkbox before saving.

**Q: What if parent email is missing?**  
A: Email won't be sent, but mark is still saved. Update student record with email.

**Q: Can I customize the email content?**  
A: Yes, edit the template in `xmark/templates/xmark/email/marks_notification.html`

**Q: How do I know if email was sent?**  
A: Check the success message after saving - it will confirm if email was sent.

**Q: Can students see their marks before parents?**  
A: Yes, marks are visible in system immediately. Email is just a notification.

---

## 🎯 Quick Reference

### **URLs:**
- **Mark List:** `/marks/marks/`
- **Create Mark:** `/marks/marks/create/`
- **Edit Mark:** `/marks/marks/<id>/edit/`
- **Resend Email:** `/marks/marks/<id>/resend-email/`

### **Email Triggers:**
1. Create mark with status="Published" + email checked = ✅ Email sent
2. Update published mark + email checked = ✅ Update email sent
3. Click "Resend Email" button = ✅ Email sent

### **Email Status:**
- ✅ Success: "Email notification sent to parents"
- ⚠️ Warning: "Email notification could not be sent"
- ℹ️ Info: Saved without email (draft or unchecked)

---

## ✅ Implementation Checklist

- [x] Email notification utility created
- [x] Professional HTML email template
- [x] Create mark sends email (if published)
- [x] Edit mark sends email (if published)
- [x] Update detection (new vs revised)
- [x] Resend email functionality
- [x] Email checkbox in form
- [x] Resend button in detail page
- [x] URL patterns configured
- [x] Error handling implemented
- [x] Success/failure feedback
- [x] Documentation complete

---

## 🎉 Ready to Use!

**Everything is implemented:**

1. ✅ Create marks → Email sent when published
2. ✅ Edit marks → Update email sent
3. ✅ Resend option → Manual resend available
4. ✅ Professional template → Beautiful HTML emails
5. ✅ Optional toggle → Can disable per mark
6. ✅ Full error handling → Graceful failures

**Test it now:**
1. Go to: `http://127.0.0.1:8000/marks/marks/create/`
2. Enter student marks
3. Set status to "Published"
4. Keep email checkbox checked
5. Save
6. Check terminal for email (development mode)
7. Parents will receive beautiful HTML email!

---

**Last Updated:** December 2025  
**Version:** 1.0  
**Status:** ✅ Production Ready  
**Module:** Marks Management - Email Notifications

