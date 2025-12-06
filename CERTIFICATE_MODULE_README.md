# Certificate Issuance & Verification System

## Overview

The Certificate Management System (`xcertificate`) provides a complete solution for issuing, managing, and verifying student certificates with security and authenticity features.

---

## 🎯 Key Features

### 1. **Manual Certificate Issuance**
- Complete control over certificate issuance
- No automatic generation - administrator approval required
- Draft → Issued → Printed → Collected workflow

### 2. **Certificate Verification System**
- Public verification portal
- QR code verification
- Unique verification codes
- Verification logging and analytics

### 3. **Security Features**
- Unique certificate numbers (e.g., CERT/2025/0001)
- SHA-256 verification codes
- Revocation support
- Tamper detection
- Verification tracking

### 4. **Certificate Templates**
- Customizable certificate designs
- Multiple template types
- Institution branding (logo, seal)
- Digital signature support

---

## 📋 Admin URLs

| Feature | URL |
|---------|-----|
| **Certificate Templates** | `http://edu.brillianzinstitute.com/admin/xcertificate/certificatetemplate/` |
| **Certificate Signatories** | `http://edu.brillianzinstitute.com/admin/xcertificate/certificatesignatory/` |
| **Student Certificates** | `http://edu.brillianzinstitute.com/admin/xcertificate/studentcertificate/` |
| **Verification Logs** | `http://edu.brillianzinstitute.com/admin/xcertificate/certificateverification/` |
| **Batch Processing** | `http://edu.brillianzinstitute.com/admin/xcertificate/certificatebatch/` |

---

## 🚀 Quick Start Guide

### Step 1: Create Certificate Template

1. Go to: `/admin/xcertificate/certificatetemplate/add/`
2. Fill in:
   - Template name (e.g., "Course Completion Certificate")
   - Template type (Completion, Achievement, etc.)
   - Template code (e.g., "COMP-001")
   - Body text template (use placeholders like `{student_name}`, `{course_name}`)
3. Upload institution logo and seal
4. Configure QR code settings
5. Save the template

### Step 2: Add Certificate Signatories

1. Go to: `/admin/xcertificate/certificatesignatory/add/`
2. Add authorized signatories:
   - Name: "Dr. Ahmed Al-Rashid"
   - Position: Director/Principal/Coordinator
   - Upload signature image
   - Set display order
3. Mark as active

### Step 3: Record Certificate Given to Student

**When you physically give a certificate to a student:**

1. Go to: `/admin/xcertificate/studentcertificate/add/`
2. Fill in certificate details:
   - **Student**: Select student from dropdown
   - **Course**: Select course
   - **Template**: Choose certificate template
   - **Issue Date**: Date certificate was given
   - **Completion Date**: When student completed course
   - **Grade**: Distinction/First Class/Pass/etc.
   - **Percentage**: Optional score
   - **Status**: **"Certificate Issued & Given"** (default)
   - **Collected By**: Student name or parent name
   - **Remarks**: Any notes (e.g., "Collected by student", "Given at ceremony")
3. Select signatories (who signed the physical certificate)
4. **Save**
5. **Done!** Certificate recorded in system
   - Certificate number auto-generated (e.g., CERT/2025/0001)
   - Verification code auto-generated
   - Ready for verification

### Step 4: For Pending Collection (Optional)

**If certificate is ready but student hasn't collected yet:**

1. Create certificate record as above
2. Set status to: **"Pending Collection"**
3. When student collects, change status to: **"Certificate Issued & Given"**
4. Update "Collected By" field

---

## 🔍 Certificate Verification

### Public Verification Portal

**URL Pattern:** `/verify-certificate/{verification_code}/`

**Example:**
```
http://edu.brillianzinstitute.com/verify-certificate/a1b2c3d4e5f6...
```

### Verification Methods

1. **By Certificate Number**
   - Enter: CERT/2025/0001
   - System searches and displays certificate

2. **By QR Code**
   - Scan QR code on physical certificate
   - Redirects to verification page
   - Instant verification

3. **By Verification Code**
   - Use 64-character SHA-256 hash
   - Most secure method

### What Verification Shows

✅ **Valid Certificate:**
```
Certificate: CERT/2025/0001
Student: Ahmed Mohammed
Course: Python Programming
Issue Date: January 15, 2025
Status: Issued
Grade: Distinction
Issued by: Brillianz Institute
```

❌ **Invalid Certificate:**
```
Certificate Not Found
This certificate number does not exist in our records.
```

🚫 **Revoked Certificate:**
```
Certificate Revoked
This certificate has been revoked and is no longer valid.
Revocation Date: March 1, 2025
```

---

## 📊 Simplified Certificate Status Workflow

```
PHYSICAL CERTIFICATE GIVEN TO STUDENT
  ↓ (Record in system)
CERTIFICATE ISSUED & GIVEN ✅
```

**OR (If certificate ready but not yet collected):**

```
CERTIFICATE READY
  ↓ (Create record)
PENDING COLLECTION ⏳
  ↓ (Student collects)
CERTIFICATE ISSUED & GIVEN ✅
```

### Status Options (Simplified)

| Status | Description | When to Use | Color |
|--------|-------------|-------------|-------|
| **Certificate Issued & Given** | Certificate physically given to student | Default - use when recording given certificate | Green ✅ |
| **Pending Collection** | Certificate ready, student hasn't collected | Optional - if you want to track uncollected | Yellow ⏳ |
| **Revoked** | Certificate invalidated/cancelled | Rare - if certificate needs to be cancelled | Red ✗ |

---

## 🎨 Certificate Templates

### Template Types

1. **Course Completion** - For completed courses
2. **Achievement Certificate** - For special achievements
3. **Participation Certificate** - For event participation
4. **Certificate of Excellence** - For excellent performance
5. **Certificate of Merit** - For meritorious performance
6. **Perfect Attendance** - For perfect attendance
7. **Custom Certificate** - Custom certificates

### Placeholders

Use these in template body text:

- `{student_name}` - Student's full name
- `{course_name}` - Course name
- `{completion_date}` - Course completion date
- `{issue_date}` - Certificate issue date
- `{grade}` - Grade/Result
- `{percentage}` - Percentage score
- `{duration_hours}` - Course duration
- `{certificate_number}` - Certificate number

### Example Template Body:

```
This is to certify that {student_name} has successfully 
completed the course "{course_name}" with a grade of {grade} 
on {completion_date}.

Certificate Number: {certificate_number}
```

---

## 🔒 Security Features

### 1. Unique Certificate Numbers
- Format: `CERT/YYYY/NNNN`
- Example: `CERT/2025/0001`
- Auto-incremented yearly

### 2. Verification Codes
- 64-character SHA-256 hash
- Unique for each certificate
- Used for secure verification

### 3. QR Codes
- Embedded in certificate PDF
- Contains verification URL
- Scannable for instant verification

### 4. Verification Logging
- Every verification attempt logged
- IP address tracking
- Geographic location (optional)
- Verification count tracking

### 5. Revocation System
- Certificates can be revoked
- Revocation reason recorded
- Revoked certificates show as invalid

---

## 📈 Verification Analytics

### View Verification Logs

Go to: `/admin/xcertificate/certificateverification/`

### Track:
- Total verifications per certificate
- Verification methods used
- Geographic distribution
- Time patterns
- Suspicious activities

### Statistics Available:
- Verification count (per certificate)
- Last verified timestamp
- Verification result distribution
- Most verified certificates

---

## 🔧 Admin Actions (Bulk Operations)

### Certificate Management

When you select multiple certificates in the admin, you can use these actions:

1. **✓ Mark as Issued & Given to Student** - Record that certificates were given
2. **⏳ Mark as Pending Collection** - Mark certificates as ready but not collected
3. **✗ Revoke Selected Certificates** - Invalidate certificates

### Batch Processing

For issuing multiple certificates at once:

1. Create certificate batch
2. Select course and template
3. Add students to batch
4. Process batch
5. Review results

---

## 🎯 Best Practices

### 1. Certificate Recording

✅ **Do:**
- Record certificates immediately after giving them to students
- Use consistent grade terminology (Distinction, First Class, Pass)
- Fill in "Collected By" field (student or parent name)
- Add remarks for tracking (e.g., "Ceremony", "Office collection")
- Set correct issue and completion dates
- Select appropriate signatories who signed the physical certificate

❌ **Don't:**
- Forget to record certificates after distribution
- Leave "Collected By" field empty
- Skip completion dates

### 2. Template Management

✅ **Do:**
- Create separate templates for different certificate types
- Use clear, professional language
- Test templates before production use
- Keep template codes short and meaningful

### 3. Security

✅ **Do:**
- Monitor verification logs regularly
- Investigate suspicious verification patterns
- Keep revocation reasons documented
- Review expired certificates periodically

---

## 🆘 Common Issues

### Issue 1: Certificate Number Not Generated

**Solution:** Certificate numbers are auto-generated on save. If not generated, check that the certificate was saved properly.

### Issue 2: Verification Not Working

**Solution:** Ensure the certificate status is "Issued" or "Printed". Draft certificates are not publicly verifiable.

### Issue 3: QR Code Not Showing

**Solution:** Check template settings - "Include QR Code" should be enabled.

---

## 📞 Support

For technical issues or questions:
- Check verification logs for errors
- Review certificate status
- Contact system administrator

---

## 🔄 Migration from Manual System

If migrating from a manual certificate system:

1. Create templates matching existing certificates
2. Add all signatories
3. Enter historical certificates with:
   - Correct issue dates
   - Original certificate numbers (if possible)
   - Mark as "Issued" and "Collected" if already distributed
4. Set verification codes for existing certificates

---

## 📝 Notes

- **Manual Issuance**: All certificates must be manually created and approved
- **No Automatic Generation**: System does not auto-generate certificates on course completion
- **Admin Control**: Only administrators can issue certificates
- **Public Verification**: Anyone can verify certificates using the public portal
- **Verification Logging**: All verification attempts are logged for security

---

*Last Updated: December 2025*

