# Transport Fee Management - Complete Guide

## 📋 Overview

The Transport Fee Management system is a comprehensive module for managing student transport fees with advanced features including filtering, email notifications, receipt printing, and CSV export.

---

## 🎯 Key Features

### 1. ✅ Fee Management
- Create and edit transport fee entries
- Record fee amount (KWD with 3 decimal precision)
- Track payment dates
- Add optional notes
- Link to student records

### 2. 🔍 Advanced Filtering
- **Search**: By student name or admission number
- **Student Filter**: Dropdown to select specific student
- **Date Range**: From date and To date filters
- **Amount Range**: Min and max amount filters
- **Combined Filters**: All filters work together
- **Statistics**: Real-time total amount and entry count
- **Clear Filters**: Quick reset button

### 3. 🖨️ Professional Receipt Printing
- **Beautiful Design**: Modern, branded receipt template
- **Print Options**:
  - Print button in fee list (🖨️ icon)
  - Quick print after creating/editing fee
  - Opens in new window for immediate printing
- **Receipt Contents**:
  - Unique receipt number (TF-XXXXXX)
  - Timestamp of generation
  - Complete student information
  - Parent contact details
  - Fee amount prominently displayed
  - Payment date
  - Notes section
  - Signature lines for staff and parents
  - Professional EduPulse branding
- **Print-Optimized**: Clean layout without backgrounds/buttons when printed

### 4. 📧 Email Notifications
- **Automatic Emails**: Sent to both parents (father and mother)
- **Email Triggers**:
  - Creating new fee entry
  - Updating existing fee
- **Optional Toggle**: Checkbox to enable/disable email per entry
- **Resend Option**: Resend email notification anytime from fee list
- **Professional Templates**: HTML emails with modern design
- **Email Contents**:
  - Complete fee details
  - Student information
  - Payment confirmation
  - Important notices
  - Contact information

### 5. 📊 Export to CSV
- Export filtered fee data to CSV
- Maintains active filters
- Timestamped filename
- Includes all relevant fields
- Ready for Excel/Sheets

### 6. 📈 Statistics Dashboard
- **Total Amount Card**: Sum of all filtered fees
- **Total Entries Card**: Count of filtered entries
- Real-time updates based on filters

---

## 🚀 How to Use

### Creating a New Fee Entry

1. **Navigate**: Go to **Transport → Fees**
2. **Click**: "Add New Fee" button
3. **Fill Form**:
   - Select student from dropdown
   - Enter amount (in KWD)
   - Choose payment date
   - Add optional notes
4. **Email Option**: Check/uncheck "Send Email Notification to Parents" (checked by default)
5. **Save**: Click "Save" button
6. **Print**: Click "Print Receipt" in success message (optional)

### Editing an Existing Fee

1. **Find Fee**: Locate fee entry in the list
2. **Click Edit**: Yellow pencil icon (✏️)
3. **Modify**: Update any fields
4. **Email Option**: Choose whether to send update notification
5. **Save**: Click "Save"
6. **Print**: Use quick print button in success message

### Printing Receipts

**Option 1: From Fee List**
1. Find the fee entry
2. Click green Print icon (🖨️)
3. Receipt opens in new window
4. Click "Print Receipt" or press Ctrl+P

**Option 2: After Creating/Editing**
1. Look for success message after saving
2. Click "Print Receipt" button in the message
3. Print immediately

### Using Filters

1. **Locate Filter Section**: Below statistics cards
2. **Apply Filters**:
   - **Search Box**: Type student name or admission number
   - **Student Dropdown**: Select specific student
   - **From Date**: Set start date
   - **To Date**: Set end date
   - **Min Amount**: Set minimum KWD amount
   - **Max Amount**: Set maximum KWD amount
3. **Click "Apply Filters"**
4. **View Results**: Table updates with filtered data
5. **Statistics Update**: Cards show filtered totals
6. **Clear**: Click "Clear Filters" or "Reset" to remove all filters

### Sending Email Notifications

**Automatic (During Create/Edit)**:
- Email checkbox is checked by default
- Email sends automatically when you save
- Success message confirms if email was sent

**Manual Resend**:
1. Find fee in the list
2. Click blue Envelope icon (📧)
3. Confirm the resend action
4. Check success message

### Exporting Data

1. **Apply Filters**: (optional) Filter data as needed
2. **Click "Export to CSV"**: Button in header
3. **Download**: CSV file downloads automatically
4. **Open**: Open in Excel, Google Sheets, or any spreadsheet software

---

## 📋 Receipt Details

### Receipt Sections

**Header**:
- 🚌 Transport Fee Receipt title
- EduPulse branding
- Gradient background

**Receipt Information**:
- Unique receipt number (TF-000001, TF-000002, etc.)
- Generation date and time

**Student Information**:
- Full name
- Admission number
- Grade and program

**Parent Contact**:
- Father's name and mobile
- Mother's name and mobile

**Fee Details**:
- Payment date (formatted)
- Amount in large, prominent display
- "PAID IN FULL" status badge
- Notes (if any)

**Signatures**:
- Staff signature line
- Parent/Guardian signature line

**Footer**:
- Official statement
- Contact information
- Timestamp

### Receipt Features

✅ **Professional Design**: Modern gradient header with icons  
✅ **Color-Coded**: Visual hierarchy with colors  
✅ **Print-Optimized**: Clean black-and-white for printing  
✅ **Unique Numbering**: Sequential receipt IDs  
✅ **Official Format**: Suitable for record keeping  
✅ **Easy to Print**: One-click printing  
✅ **Complete Information**: All necessary details included  

---

## 📧 Email Configuration

### Development Mode (Current)
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
Emails are printed to console/terminal for testing.

### Production Configuration

Add to `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # or your SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'EduPulse <noreply@edupulse.com>'
```

### Gmail Setup

1. Enable 2-Factor Authentication in Gmail
2. Go to Google Account → Security → App Passwords
3. Generate new app password
4. Use app password in `EMAIL_HOST_PASSWORD`

### Other Email Providers

- **Office 365**: `smtp.office365.com`, Port 587
- **Outlook**: `smtp-mail.outlook.com`, Port 587
- **SendGrid**: `smtp.sendgrid.net`, Port 587
- **AWS SES**: `email-smtp.[region].amazonaws.com`, Port 587

---

## 🎨 Action Buttons Guide

In the fee list, each entry has three action buttons:

| Icon | Color | Action | Description |
|------|-------|--------|-------------|
| ✏️ | Yellow | Edit | Modify fee details |
| 🖨️ | Green | Print | Generate and print receipt |
| 📧 | Blue | Email | Resend email to parents |

---

## 💡 Tips & Best Practices

### Fee Management
1. ✅ Always verify student selection before saving
2. ✅ Use notes field for payment method, voucher numbers, etc.
3. ✅ Print receipt immediately after recording fee
4. ✅ Keep email notification enabled for transparency
5. ✅ Double-check amount (3 decimal places for KWD)

### Filtering
1. ✅ Use date range for monthly reports
2. ✅ Search by admission number for quick lookup
3. ✅ Export filtered data for accounting
4. ✅ Clear filters when switching tasks
5. ✅ Check statistics card for quick totals

### Receipts
1. ✅ Print receipts for parent records
2. ✅ Keep physical copies for audit trail
3. ✅ Use receipt numbers for tracking
4. ✅ Print before closing browser window
5. ✅ Save as PDF if needed (Print to PDF option)

### Email Notifications
1. ✅ Verify parent emails in student records
2. ✅ Test with your own email first
3. ✅ Use resend if parent didn't receive
4. ✅ Check spam folder if issues reported
5. ✅ Disable email only when parent explicitly requests

---

## 🔧 Troubleshooting

### Receipt Won't Print
- **Check**: Popup blocker might be blocking new window
- **Solution**: Allow popups for the site

### Email Not Received
- **Check**: Parent email addresses in student record
- **Check**: Spam/junk folder
- **Check**: Email configuration in settings.py
- **Solution**: Use "Resend Email" button

### Filters Not Working
- **Check**: Click "Apply Filters" button
- **Solution**: Clear browser cache and try again

### Export Shows No Data
- **Check**: Current filters might be too restrictive
- **Solution**: Clear some filters and try again

---

## 📊 Reports You Can Generate

### 1. Monthly Transport Fee Report
- Set date range for the month
- Export to CSV
- Open in Excel for analysis

### 2. Student-Specific Report
- Select student from dropdown
- View all their transport fees
- Print receipts as needed

### 3. Amount Range Report
- Set min/max amounts
- Find high-value or low-value payments
- Export for accounting

### 4. Daily Collection Report
- Set from_date = to_date = today
- View all fees collected today
- Check statistics card for total

---

## 🎯 Workflow Examples

### Daily Fee Collection Workflow

1. **Morning**: Open Transport Fee Management
2. **As fees come in**:
   - Click "Add New Fee"
   - Fill student and amount
   - Keep email checkbox checked
   - Save and print receipt
   - Give receipt to parent
3. **End of day**:
   - Filter by today's date
   - Check statistics for total
   - Export to CSV for records
   - Send data to accounts department

### Monthly Reporting Workflow

1. **Set date range**: First to last day of month
2. **Review statistics**: Total amount and count
3. **Export to CSV**: Download monthly data
4. **Generate report**: Use Excel/Sheets
5. **Share**: Send to management/accounts
6. **Archive**: Save CSV for records

### Parent Inquiry Workflow

1. **Search**: Type student name in search box
2. **View History**: See all transport fees
3. **Print Receipt**: Click print icon for any fee
4. **Resend Email**: If parent lost original email
5. **Provide Info**: Reference receipt numbers

---

## 📁 File Structure

```
xtransport/
├── views.py                          # Fee CRUD, filters, export, receipts
├── models.py                         # TransportFee model
├── forms.py                          # Fee form with Bootstrap styling
├── urls.py                           # URL routing
├── email_notifications.py            # Email sending utilities
└── templates/xtransport/
    ├── transport_fee_list.html       # Main fee list with filters
    ├── transport_fee_form.html       # Create/Edit form
    ├── receipt_print.html            # Printable receipt
    └── email/
        ├── fee_notification.html     # Email template
        └── fee_reminder.html         # Reminder template
```

---

## ✅ Feature Checklist

- [x] Create transport fee entries
- [x] Edit existing fees
- [x] Advanced filtering system
- [x] Real-time statistics
- [x] Professional receipt printing
- [x] Automatic email notifications
- [x] Manual email resend
- [x] CSV export with filters
- [x] Responsive design
- [x] Print-optimized layouts
- [x] Parent contact display
- [x] Unique receipt numbering
- [x] Quick print after save
- [x] Bootstrap UI components
- [x] Success/error messaging

---

## 🔮 Future Enhancements (Roadmap)

- [ ] Bulk fee import (Excel/CSV)
- [ ] Scheduled fee reminders
- [ ] SMS notifications
- [ ] Receipt email attachment
- [ ] Payment method tracking
- [ ] Multi-currency support
- [ ] Recurring fee setup
- [ ] Parent portal access
- [ ] Mobile app integration
- [ ] Analytics dashboard
- [ ] Automated reports
- [ ] WhatsApp integration

---

## 📞 Support & Help

### Common Questions

**Q: Can I delete a fee entry?**  
A: Not directly through UI (by design). Contact system admin if needed.

**Q: How do I change the receipt logo?**  
A: Modify the receipt template in `xtransport/templates/xtransport/receipt_print.html`

**Q: Can I customize email content?**  
A: Yes! Edit templates in `xtransport/templates/xtransport/email/`

**Q: How do I export to Excel directly?**  
A: Export to CSV, then open in Excel

**Q: Can parents access receipts online?**  
A: Not yet. Coming in future updates.

### Getting Help

1. Check this documentation
2. Review error messages carefully
3. Check terminal/console for errors
4. Verify student data is complete
5. Contact system administrator

---

## 📚 Related Documentation

- [AUTHENTICATION_README.md](./AUTHENTICATION_README.md) - Login and user management
- [ATTENDANCE_NOTIFICATION_README.md](./ATTENDANCE_NOTIFICATION_README.md) - Attendance emails
- [URL_REFERENCE.md](./URL_REFERENCE.md) - Complete URL guide

---

## 🎉 Quick Start Checklist

- [ ] Configure email settings (for production)
- [ ] Test email with your address
- [ ] Verify student records have parent emails
- [ ] Create test fee entry
- [ ] Print test receipt
- [ ] Test all filters
- [ ] Export test CSV
- [ ] Train staff on features
- [ ] Document local procedures
- [ ] Set up backup processes

---

**Last Updated**: December 2025  
**Version**: 2.0  
**Module**: Transport Fee Management  
**Status**: Production Ready ✅

