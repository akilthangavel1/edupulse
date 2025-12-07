# Transport Fee Management - Complete Guide

## Overview

The transport fee management system includes comprehensive features for recording fees, automated email notifications to parents, and professional receipt printing.

## Features

### 1. Print Receipt
- **Professional Receipt Design**: Modern, branded receipt template
- **Instant Printing**: Print receipts directly from the fee list
- **Post-Creation Printing**: Quick print button in success message after creating/editing fees
- **Receipt Details**:
  - Unique receipt number (TF-XXXXXX format)
  - Student information with photo-ready layout
  - Parent contact details
  - Fee amount prominently displayed
  - Payment date and notes
  - Signature sections for staff and parents
  - Professional branding and layout

### 2. Automatic Email Notifications
- **When Creating Fee**: Parents receive an email when a new transport fee is recorded
- **When Updating Fee**: Parents receive an email when a fee entry is updated
- **Optional Toggle**: Staff can choose whether to send email when creating/updating fees

### 2. Email Recipients
Emails are automatically sent to:
- **Father's Email** (from student record)
- **Mother's Email** (from student record)

### 3. Email Content
Each notification email includes:
- Student name and admission number
- Grade and program
- Fee amount (in KWD)
- Payment date
- Any notes added
- Professional HTML design with school branding

### 4. Resend Email Feature
- **Manual Resend**: Resend email notification for any fee entry from the fee list
- **Bulk Operations**: Export and notify multiple fees at once

## How to Use

### Printing Receipts

#### Method 1: From Fee List
1. Navigate to **Transport → Fees**
2. Find the fee entry in the list
3. Click the **Print icon** (🖨️) in the Actions column
4. Receipt opens in new window
5. Click **"Print Receipt"** button or use Ctrl+P (Cmd+P on Mac)
6. Select printer and print

#### Method 2: After Creating/Editing Fee
1. After saving a fee, look for success message
2. Click the **"Print Receipt"** button in the success message
3. Receipt opens in new window
4. Print immediately

#### Receipt Features
- **Auto-numbering**: Unique receipt ID (TF-000001 format)
- **Timestamp**: Date and time of receipt generation
- **Complete Details**: Student info, parent contact, fee amount
- **Professional Layout**: Clean, branded design suitable for official records
- **Print-Optimized**: Removes buttons and background colors when printing
- **Signature Sections**: Space for staff and parent acknowledgment

### Creating a New Fee Entry

1. Navigate to **Transport → Fees**
2. Click **"Add New Fee"**
3. Fill in the fee details:
   - Select student
   - Enter amount
   - Choose payment date
   - Add optional notes
4. **Email Notification Checkbox** (checked by default):
   - ✅ Checked: Email will be sent to parents
   - ⬜ Unchecked: No email will be sent
5. Click **"Save"**

### Editing an Existing Fee

1. Go to fee list and click **Edit** (pencil icon)
2. Modify the details
3. Choose whether to send email notification
4. Click **"Save"**

### Resending Email Notification

1. In the fee list, find the entry
2. Click the **envelope icon** (📧) in the Actions column
3. Confirm the resend action
4. Email will be sent to parents

## Email Templates

### Fee Notification Email
**Subject**: `Transport Fee Recorded - [Student Name]`

**Contains**:
- Fee details
- Payment information
- Status badge
- Important notes and disclaimers

### Fee Reminder Email (Coming Soon)
**Subject**: `Transport Fee Reminder - [Student Name]`

**Contains**:
- Outstanding amount
- Payment instructions
- Contact information

## Configuration

### Email Settings

The system uses Django's email backend. In development mode:

```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

For production, configure SMTP settings:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'EduPulse <noreply@edupulse.com>'
```

### Gmail Configuration

If using Gmail:
1. Enable 2-Factor Authentication
2. Generate an **App Password**
3. Use the app password in `EMAIL_HOST_PASSWORD`

### Other Email Providers

- **Office 365**: `smtp.office365.com`, Port 587
- **SendGrid**: `smtp.sendgrid.net`, Port 587
- **AWS SES**: `email-smtp.region.amazonaws.com`, Port 587

## Features Breakdown

### ✅ Current Features
- **Receipt Printing**:
  - Professional receipt template
  - Print from fee list
  - Quick print after create/edit
  - Unique receipt numbering
  - Print-optimized CSS
- **Email Notifications**:
  - Automatic email on fee creation
  - Automatic email on fee update
  - Optional email toggle in form
  - Resend email functionality
  - Professional HTML email templates
  - Dual recipient (father and mother)
  - Email delivery status feedback

### 🔄 Coming Soon
- Bulk email notifications
- Fee reminder scheduler
- Custom email templates
- SMS notifications integration
- Email delivery tracking
- Parent email preferences

## Troubleshooting

### Email Not Sending

**Check:**
1. ✅ Parent email addresses are correct in student record
2. ✅ Email settings configured in `settings.py`
3. ✅ Email backend is not in console mode for production
4. ✅ SMTP credentials are valid
5. ✅ Firewall/network allows SMTP connections

### Email Goes to Spam

**Solutions:**
1. Configure SPF and DKIM records
2. Use a professional email domain
3. Avoid spam trigger words
4. Use a reputable SMTP service
5. Warm up your email domain

### Missing Parent Emails

**Action:**
- Update student records with parent email addresses
- Navigate to: **Dashboard → All Students → Edit Student**
- Fill in: `Father Email ID` and `Mother Email ID`

## Testing Email Notifications

### Development Mode
1. Emails appear in console/terminal
2. Check terminal output after creating/updating fee
3. Verify email content and formatting

### Production Mode
1. Create a test fee entry
2. Check inbox of parent email addresses
3. Verify email received and displays correctly
4. Check spam folder if not in inbox

## Email Statistics

Track email notifications in the system:
- Total emails sent
- Delivery success rate
- Failed deliveries
- Email open rates (if tracking enabled)

## Best Practices

1. **Always verify parent emails** before bulk operations
2. **Test with your own email** first
3. **Schedule reminders** during business hours
4. **Keep email content concise** and professional
5. **Provide contact information** for questions
6. **Allow parents to opt-out** if needed (coming soon)

## Security & Privacy

- Email addresses are stored securely
- Emails are sent via encrypted connection (TLS)
- No sensitive student data exposed in subject lines
- Compliant with data protection regulations

## Support

For issues or questions:
1. Check Django logs for email errors
2. Verify email configuration
3. Test with a simple test email
4. Contact system administrator

---

## Quick Start Checklist

- [ ] Configure email settings in `settings.py`
- [ ] Test email configuration
- [ ] Verify student email addresses
- [ ] Create test fee entry with email
- [ ] Check email received correctly
- [ ] Train staff on email features
- [ ] Document email templates for parents

---

**Last Updated**: December 2025  
**Version**: 1.0  
**Module**: Transport Fee Management

