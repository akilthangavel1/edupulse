# Django Admin URLs Reference

This document lists all correct Django admin URLs for the EduPulse system.

## Important Notes

Django admin automatically generates URLs based on **model names** (lowercase), not verbose names or custom names.

**Format:** `/admin/<app_label>/<model_name_lowercase>/`

---

## Student Management (xstudent)

| Model | Admin URL |
|-------|-----------|
| NewStudent | `/admin/xstudent/newstudent/` |
| OldStudent | `/admin/xstudent/oldstudent/` |
| Attendance | `/admin/xstudent/attendance/` |
| AttendanceSummary | `/admin/xstudent/attendancesummary/` |

---

## Course & Fee Management (xcoursefee)

| Model | Admin URL |
|-------|-----------|
| Course | `/admin/xcoursefee/course/` |
| FeeStructure | `/admin/xcoursefee/feestructure/` |
| StudentEnrollment | `/admin/xcoursefee/studentenrollment/` |
| Payment | `/admin/xcoursefee/payment/` |
| Invoice | `/admin/xcoursefee/invoice/` |
| Discount | `/admin/xcoursefee/discount/` |
| Kit | `/admin/xcoursefee/kit/` |
| CourseKit | `/admin/xcoursefee/coursekit/` |
| KitFee | `/admin/xcoursefee/kitfee/` |

---

## Marks Management (xmark)

| Model | Admin URL |
|-------|-----------|
| Subject | `/admin/xmark/subject/` |
| AssessmentType | `/admin/xmark/assessmenttype/` |
| StudentMark | `/admin/xmark/studentmark/` ⚠️ |
| GradeScale | `/admin/xmark/gradescale/` |
| StudentGradeSummary | `/admin/xmark/studentgradesummary/` ⚠️ |

⚠️ **Previously incorrect URLs:**
- ❌ `/admin/xmark/mark/` → ✅ `/admin/xmark/studentmark/`
- ❌ `/admin/xmark/gradesummary/` → ✅ `/admin/xmark/studentgradesummary/`

---

## Faculty/Trainer Management (xtrainer)

| Model | Admin URL |
|-------|-----------|
| Faculty | `/admin/xtrainer/faculty/` |
| FacultyOnboarding | `/admin/xtrainer/facultyonboarding/` |
| FacultyLeaveRequest | `/admin/xtrainer/facultyleaverequest/` ⚠️ |
| BackupSchedule | `/admin/xtrainer/backupschedule/` |
| FacultyAttendance | `/admin/xtrainer/facultyattendance/` |
| FacultyPayment | `/admin/xtrainer/facultypayment/` |
| ExamRequest | `/admin/xtrainer/examrequest/` |
| NotificationLog | `/admin/xtrainer/notificationlog/` |

⚠️ **Previously incorrect URL:**
- ❌ `/admin/xtrainer/leaverequest/` → ✅ `/admin/xtrainer/facultyleaverequest/`

---

## Batch Management (xbatch)

⚠️ **Status:** Models exist but are NOT registered in Django admin yet.

**To enable:** Register models in `xbatch/admin.py`

**Available Models (not yet in admin):**
- Batch → `/admin/xbatch/batch/`
- BatchStudent → `/admin/xbatch/batchstudent/`
- BatchTransfer → `/admin/xbatch/batchtransfer/`
- BatchFacultyChange → `/admin/xbatch/batchfacultychange/`
- WhatsAppGroup → `/admin/xbatch/whatsappgroup/`

---

## Transport Management (xtransport)

⚠️ **Status:** Models exist but are NOT registered in Django admin yet.

**To enable:** Register models in `xtransport/admin.py`

**Available Models (not yet in admin):**
- Vendor → `/admin/xtransport/vendor/`
- VendorRequest → `/admin/xtransport/vendorrequest/`
- StudentTransportAssignment → `/admin/xtransport/studenttransportassignment/`
- VendorPayment → `/admin/xtransport/vendorpayment/`
- MonthlyPaymentGeneration → `/admin/xtransport/monthlypaymentgeneration/`
- VendorRating → `/admin/xtransport/vendorrating/`

---

## Kit Materials Management (xkit)

| Model | Admin URL |
|-------|-----------|
| MaterialCategory | `/admin/xkit/materialcategory/` |
| Supplier | `/admin/xkit/supplier/` |
| Material | `/admin/xkit/material/` |
| MaterialKit | `/admin/xkit/materialkit/` ⚠️ |
| KitMaterial | `/admin/xkit/kitmaterial/` |
| StockMovement | `/admin/xkit/stockmovement/` |
| KitAssemblyLog | `/admin/xkit/kitassemblylog/` ⚠️ |

⚠️ **Previously incorrect URLs:**
- ❌ `/admin/xkit/kit/` → ✅ `/admin/xkit/materialkit/`
- ❌ `/admin/xkit/assemblylog/` → ✅ `/admin/xkit/kitassemblylog/`

**Note:** `MaterialKit` is different from `xcoursefee.Kit` - they can be linked but are separate models.

---

## Broadcast & Lead Management (xbroadcast)

| Model | Admin URL |
|-------|-----------|
| BroadcastTemplate | `/admin/xbroadcast/broadcasttemplate/` ⚠️ |
| Broadcast | `/admin/xbroadcast/broadcast/` |
| BroadcastRecipient | `/admin/xbroadcast/broadcastrecipient/` |
| Lead | `/admin/xbroadcast/lead/` |
| LeadActivity | `/admin/xbroadcast/leadactivity/` |
| LeadScore | `/admin/xbroadcast/leadscore/` |
| CommunicationLog | `/admin/xbroadcast/communicationlog/` |

⚠️ **Previously incorrect URL:**
- ❌ `/admin/xbroadcast/messagetemplate/` → ✅ `/admin/xbroadcast/broadcasttemplate/`

---

## Certificate Management (xcertificate)

| Model | Admin URL |
|-------|-----------|
| CertificateTemplate | `/admin/xcertificate/certificatetemplate/` |
| CertificateSignatory | `/admin/xcertificate/certificatesignatory/` |
| StudentCertificate | `/admin/xcertificate/studentcertificate/` |
| CertificateVerification | `/admin/xcertificate/certificateverification/` |
| CertificateBatch | `/admin/xcertificate/certificatebatch/` |

**Features:**
- ✅ Manual certificate issuance workflow
- ✅ Public verification system with QR codes
- ✅ Certificate status tracking (Draft, Issued, Printed, Collected, Revoked)
- ✅ Verification logging and security tracking
- ✅ Batch processing for bulk issuance
- ✅ Certificate templates with customization
- ✅ Digital signatures support

**Public Verification URL:**
- `/verify-certificate/{verification_code}/` - Public certificate verification portal

---

## System Admin (xadmin)

⚠️ **Status:** App exists but admin status unknown. Check `xadmin/admin.py` and `xadmin/models.py`

---

## Django Built-in Admin

| Model | Admin URL |
|-------|-----------|
| Users | `/admin/auth/user/` |
| Groups | `/admin/auth/group/` |

---

## Production URLs

For production (`http://edu.brillianzinstitute.com`), replace `http://localhost:8000` with your domain:

- Example: `http://edu.brillianzinstitute.com/admin/xmark/studentmark/`

---

## Quick Reference

### Marks Module (Fixed URLs)
```
✅ /admin/xmark/studentmark/        (not /mark/)
✅ /admin/xmark/studentgradesummary/ (not /gradesummary/)
```

### Faculty Module (Fixed URLs)
```
✅ /admin/xtrainer/facultyleaverequest/ (not /leaverequest/)
```

---

*Last updated: December 6, 2025*


