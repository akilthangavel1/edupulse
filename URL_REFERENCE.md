# EduPulse - Complete URL Reference Guide

## ⚠️ IMPORTANT: Module Status

**Not all URLs listed here are fully functional!** Some modules are placeholders showing "under development" messages.

### ✅ Fully Functional Modules (100% Working):
- ✅ **Authentication** (`/accounts/`) - All features working
- ✅ **Student Management** (`/`) - All features working
- ✅ **Course Fee Management** (`/coursefee/`) - All features working
- ✅ **Marks Management** (`/marks/`) - All features working
- ✅ **Faculty Management** (`/faculty/`) - All features working

### ⚠️ Placeholder Modules (URLs exist but not functional):
- ⚠️ **System Admin** (`/system/`) - Use `/admin/` instead
- ⚠️ **Batch Management** (`/batches/`) - Under development
- ⚠️ **Transport Management** (`/transport/`) - Under development
- ⚠️ **Kit Materials** (`/kits/`) - Under development (use `/coursefee/kits/` instead)
- ⚠️ **Broadcast** (`/broadcast/`) - Under development

**📖 For detailed status information, see [MODULE_STATUS.md](MODULE_STATUS.md)**

---

## 📋 Table of Contents
- [System Admin](#-system-admin-panel) ⚠️ Placeholder
- [Authentication](#-authentication-accounts) ✅ Working
- [Student Management](#-student-management) ✅ Working
- [Course Fee Management](#-course-fee-management) ✅ Working
- [Marks Management](#-marks-management) ✅ Working
- [Faculty Management](#-faculty-management) ✅ Working
- [Batch Management](#-batch-management) ⚠️ Placeholder
- [Transport Management](#-transport-management) ⚠️ Placeholder
- [Kit Materials Management](#-kit-materials-management) ⚠️ Placeholder
- [Broadcast & Lead Management](#-broadcast--lead-management) ⚠️ Placeholder

---

## 🔧 Django Admin Panel (Fully Functional)

**Base URL:** `/admin/`

**Status:** ✅ Fully Functional - Django's built-in admin interface

**Access Level:** Superuser/Staff only

### Admin Home
- `/admin/` - Admin dashboard (shows all registered models)

### Authentication & Authorization
- `/admin/auth/user/` - User list
- `/admin/auth/user/add/` - Add new user
- `/admin/auth/user/<id>/change/` - Edit user
- `/admin/auth/user/<id>/delete/` - Delete user confirmation
- `/admin/auth/user/<id>/password/` - Change user password
- `/admin/auth/group/` - Group list (roles/permissions)
- `/admin/auth/group/add/` - Add new group
- `/admin/auth/group/<id>/change/` - Edit group
- `/admin/auth/group/<id>/delete/` - Delete group

### Student Management (Admin Interface)
- `/admin/xstudent/newstudent/` - Student list
- `/admin/xstudent/newstudent/add/` - Add student
- `/admin/xstudent/newstudent/<id>/change/` - Edit student
- `/admin/xstudent/newstudent/<id>/delete/` - Delete student
- `/admin/xstudent/oldstudent/` - Old student list
- `/admin/xstudent/oldstudent/add/` - Add old student
- `/admin/xstudent/attendance/` - Attendance records
- `/admin/xstudent/attendancesummary/` - Attendance summaries

### Course Fee Management (Admin Interface)
- `/admin/xcoursefee/course/` - Course list
- `/admin/xcoursefee/course/add/` - Add course
- `/admin/xcoursefee/feestructure/` - Fee structures
- `/admin/xcoursefee/studentenrollment/` - Enrollments
- `/admin/xcoursefee/payment/` - Payment records
- `/admin/xcoursefee/invoice/` - Invoice list
- `/admin/xcoursefee/discount/` - Discount management
- `/admin/xcoursefee/kit/` - Kit management
- `/admin/xcoursefee/coursekit/` - Course kits
- `/admin/xcoursefee/kitfee/` - Kit fee records

### Marks Management (Admin Interface)
- `/admin/xmark/subject/` - Subject list
- `/admin/xmark/assessmenttype/` - Assessment types
- `/admin/xmark/studentmark/` - Mark records
- `/admin/xmark/gradescale/` - Grade scales
- `/admin/xmark/studentgradesummary/` - Grade summaries

### Faculty Management (Admin Interface)
- `/admin/xtrainer/faculty/` - Faculty list
- `/admin/xtrainer/facultyonboarding/` - Onboarding records
- `/admin/xtrainer/facultyleaverequest/` - Leave requests
- `/admin/xtrainer/backupschedule/` - Backup schedules
- `/admin/xtrainer/facultyattendance/` - Faculty attendance
- `/admin/xtrainer/facultypayment/` - Faculty payments
- `/admin/xtrainer/examrequest/` - Exam requests
- `/admin/xtrainer/notificationlog/` - Notification logs

### Batch Management (Admin Interface)
> **Note:** Batch models are not yet registered in Django admin. Register them in `xbatch/admin.py` to enable admin access.
<!--
- `/admin/xbatch/batch/` - Batch list
- `/admin/xbatch/batchstudent/` - Batch student assignments
- `/admin/xbatch/batchtransfer/` - Transfer records
- `/admin/xbatch/batchfacultychange/` - Faculty changes
- `/admin/xbatch/whatsappgroup/` - WhatsApp groups
-->

### Transport Management (Admin Interface)
> **Note:** Transport models are not yet registered in Django admin. Register them in `xtransport/admin.py` to enable admin access.
<!--
- `/admin/xtransport/vendor/` - Vendor list
- `/admin/xtransport/vendorrequest/` - Vendor requests
- `/admin/xtransport/studenttransportassignment/` - Student transport assignments
- `/admin/xtransport/vendorpayment/` - Vendor payments
- `/admin/xtransport/monthlypaymentgeneration/` - Payment generation
- `/admin/xtransport/vendorrating/` - Vendor ratings
-->
- `/admin/xtransport/studenttransport/` - Student assignments
- `/admin/xtransport/vendorpayment/` - Vendor payments
- `/admin/xtransport/monthlypayment/` - Monthly payments
- `/admin/xtransport/vendorrating/` - Vendor ratings

### Kit Materials (Admin Interface)
- `/admin/xkit/materialcategory/` - Material categories
- `/admin/xkit/supplier/` - Suppliers
- `/admin/xkit/material/` - Materials
- `/admin/xkit/kit/` - Kits
- `/admin/xkit/kitmaterial/` - Kit materials
- `/admin/xkit/stockmovement/` - Stock movements
- `/admin/xkit/assemblylog/` - Assembly logs

### Broadcast Management (Admin Interface)
- `/admin/xbroadcast/messagetemplate/` - Message templates
- `/admin/xbroadcast/broadcast/` - Broadcasts
- `/admin/xbroadcast/lead/` - Leads
- `/admin/xbroadcast/leadactivity/` - Lead activities
- `/admin/xbroadcast/leadscore/` - Lead scores
- `/admin/xbroadcast/communicationlog/` - Communication logs

### Admin System (Admin Interface)
- `/admin/xadmin/systemuser/` - System users
- `/admin/xadmin/role/` - Roles
- `/admin/xadmin/userprofile/` - User profiles
- `/admin/xadmin/auditlog/` - Audit logs
- `/admin/xadmin/securitylog/` - Security logs
- `/admin/xadmin/systemconfig/` - System configuration
- `/admin/xadmin/backup/` - Backups
- `/admin/xadmin/restore/` - Restore points

### Admin Actions
- `/admin/jsi18n/` - JavaScript internationalization
- `/admin/logout/` - Admin logout
- `/admin/password_change/` - Change admin password
- `/admin/password_change/done/` - Password changed confirmation

### Bulk Actions (Available in List Views)
- Select multiple items and use dropdown for actions:
  - Delete selected items
  - Export selected items
  - Custom model-specific actions

### Filters & Search
Each model list view includes:
- Right sidebar filters (by date, status, related objects)
- Search box at the top
- Column sorting (click column headers)

---

## 🔐 System Admin Panel (Placeholder)

**Base URL:** `/system/`

### ⚠️ WARNING: This Module is NOT Functional

**Status:** Placeholder - All URLs show "under development" message

**Alternative:** Use `/admin/` (Django Admin Panel) documented above for all user management and system administration tasks.

All URLs listed below exist in the routing but are **NOT IMPLEMENTED**. They will show a placeholder page.

---

### Dashboard
- `/system/` - System Dashboard ⚠️ Placeholder

### User & Role Management
- `/system/users/` - User list
- `/system/users/create/` - Create new user
- `/system/users/<id>/` - User details
- `/system/users/<id>/edit/` - Edit user
- `/system/users/<id>/activate/` - Activate user
- `/system/users/<id>/deactivate/` - Deactivate user
- `/system/roles/` - Role list
- `/system/roles/create/` - Create role
- `/system/roles/<id>/` - Role details
- `/system/roles/<id>/edit/` - Edit role

### User Profiles
- `/system/profiles/` - Profile list
- `/system/profiles/<id>/` - Profile details
- `/system/profiles/<id>/edit/` - Edit profile

### Audit & Security Logs
- `/system/audit/` - Audit log list
- `/system/audit/<id>/` - Audit log details
- `/system/audit/export/` - Export audit logs
- `/system/security/` - Security log list
- `/system/security/<id>/` - Security log details
- `/system/security/<id>/investigate/` - Investigate security log
- `/system/security/<id>/resolve/` - Resolve security log

### System Configuration
- `/system/config/` - Configuration list
- `/system/config/<config_type>/` - Config by type
- `/system/config/<id>/edit/` - Edit configuration

### Backup & Restore
- `/system/backup/` - Backup dashboard
- `/system/backup/list/` - Backup list
- `/system/backup/create/` - Create backup
- `/system/backup/<id>/` - Backup details
- `/system/backup/<id>/download/` - Download backup
- `/system/backup/<id>/delete/` - Delete backup
- `/system/restore/` - Restore dashboard
- `/system/restore/list/` - Restore list
- `/system/restore/create/` - Create restore
- `/system/restore/<id>/` - Restore details
- `/system/restore/<id>/approve/` - Approve restore

### System Monitoring
- `/system/monitoring/` - Monitoring dashboard
- `/system/monitoring/performance/` - Performance monitoring
- `/system/monitoring/errors/` - Error monitoring
- `/system/health/` - System health
- `/system/health/database/` - Database health
- `/system/health/storage/` - Storage health

### UI & Navigation
- `/system/navigation/` - Navigation management
- `/system/ui/` - UI settings

### Testing
- `/system/testing/` - Role testing dashboard
- `/system/testing/admin/` - Test admin access
- `/system/testing/staff/` - Test staff access
- `/system/security-testing/` - Security testing dashboard
- `/system/security-testing/penetration/` - Penetration testing
- `/system/security-testing/vulnerability/` - Vulnerability scan

### API Endpoints
- `/system/api/system/status/` - System status API
- `/system/api/user/<user_id>/permissions/` - User permissions API
- `/system/api/backup/progress/<backup_id>/` - Backup progress API
- `/system/api/restore/progress/<restore_id>/` - Restore progress API

---

## 🔑 Authentication (Accounts)

**Base URL:** `/accounts/`

### User Authentication
- `/accounts/register/` - User registration
- `/accounts/login/` - User login
- `/accounts/logout/` - User logout
- `/accounts/dashboard/` - User dashboard

### Password Reset
- `/accounts/password_reset/` - Request password reset
- `/accounts/password_reset/done/` - Password reset sent confirmation
- `/accounts/reset/<uidb64>/<token>/` - Password reset confirmation
- `/accounts/reset/done/` - Password reset complete

---

## 👨‍🎓 Student Management

**Base URL:** `/` (Root)

### Dashboard & Students
- `/` - Student dashboard (Home)
- `/students/` - Student list
- `/students/drafts/` - Draft students list
- `/students/create/` - Create new student
- `/students/<id>/` - Student details
- `/students/<id>/edit/` - Edit student
- `/students/<id>/delete/` - Delete student
- `/students/export/` - Export students to CSV

### Old Students
- `/old-students/` - Old students list
- `/old-students/create/` - Create old student record
- `/old-students/<id>/` - Old student details
- `/old-students/<id>/edit/` - Edit old student
- `/old-students/<id>/delete/` - Delete old student

### Attendance Management
- `/attendance/` - Attendance list
- `/attendance/dashboard/` - Attendance dashboard
- `/attendance/create/` - Mark individual attendance
- `/attendance/bulk/` - Bulk attendance marking
- `/attendance/<id>/` - Attendance details
- `/attendance/<id>/edit/` - Edit attendance
- `/attendance/<id>/delete/` - Delete attendance record
- `/attendance/report/` - Generate attendance report

---

## 💰 Course Fee Management

**Base URL:** `/coursefee/`

### Dashboard
- `/coursefee/` - Course fee dashboard
- `/coursefee/test/` - Test template page

### Course Management
- `/coursefee/courses/` - Course list
- `/coursefee/courses/create/` - Create new course
- `/coursefee/courses/<id>/` - Course details
- `/coursefee/courses/<id>/edit/` - Edit course
- `/coursefee/courses/<id>/delete/` - Delete course

### Enrollment Management
- `/coursefee/enrollments/` - Enrollment list
- `/coursefee/enrollments/create/` - Create enrollment (Course Fee Entry)
- `/coursefee/enrollments/<id>/` - Enrollment details

### Payment Management
- `/coursefee/payments/` - Payment list
- `/coursefee/payments/create/` - Record new payment
- `/coursefee/payments/<id>/` - Payment details

### Invoice Management
- `/coursefee/invoices/` - Invoice list
- `/coursefee/invoices/create/` - Create invoice
- `/coursefee/invoices/<id>/` - Invoice details

### Discount Management
- `/coursefee/discounts/` - Discount list
- `/coursefee/discounts/create/` - Create discount

### Kit Management
- `/coursefee/kits/` - Kit list
- `/coursefee/kits/create/` - Create kit
- `/coursefee/kits/<id>/` - Kit details
- `/coursefee/kits/<id>/edit/` - Edit kit
- `/coursefee/kits/<id>/delete/` - Delete kit

### Course Kit Management
- `/coursefee/course-kits/` - Course kit list
- `/coursefee/course-kits/create/` - Link kit to course
- `/coursefee/course-kits/<id>/` - Course kit details
- `/coursefee/course-kits/<id>/edit/` - Edit course kit
- `/coursefee/course-kits/<id>/delete/` - Delete course kit

### Kit Fee Management
- `/coursefee/kit-fees/` - Kit fee list
- `/coursefee/kit-fees/create/` - Create kit fee
- `/coursefee/kit-fees/<id>/` - Kit fee details
- `/coursefee/kit-fees/<id>/edit/` - Edit kit fee
- `/coursefee/kit-fees/<id>/delete/` - Delete kit fee

### Reports
- `/coursefee/reports/financial/` - Financial report

### Receipts
- `/coursefee/receipts/enrollment/<enrollment_id>/print/` - Print enrollment receipt
- `/coursefee/receipts/enrollment/<enrollment_id>/pdf/` - Download enrollment receipt (PDF)
- `/coursefee/receipts/enrollment/<enrollment_id>/excel/` - Download enrollment receipt (Excel)
- `/coursefee/receipts/payment/<payment_id>/print/` - Print payment receipt
- `/coursefee/receipts/payment/<payment_id>/pdf/` - Download payment receipt (PDF)

### AJAX Endpoints
- `/coursefee/ajax/course-fees/<course_id>/` - Get course fees
- `/coursefee/ajax/payment/<payment_id>/complete/` - Mark payment completed
- `/coursefee/ajax/course-kits/<course_id>/` - Get course kits
- `/coursefee/ajax/kit-fee/<kit_fee_id>/mark-paid/` - Mark kit fee paid
- `/coursefee/ajax/kit-fee/<kit_fee_id>/mark-delivered/` - Mark kit delivered

---

## 📊 Marks Management

**Base URL:** `/marks/`

### Dashboard
- `/marks/` - Marks dashboard

### Subject Management
- `/marks/subjects/` - Subject list
- `/marks/subjects/create/` - Create subject
- `/marks/subjects/<id>/` - Subject details
- `/marks/subjects/<id>/edit/` - Edit subject

### Mark Management
- `/marks/marks/` - Mark list
- `/marks/marks/create/` - Create mark entry
- `/marks/marks/<id>/` - Mark details
- `/marks/marks/<id>/edit/` - Edit mark
- `/marks/marks/bulk-entry/` - Bulk mark entry

### Assessment Type Management
- `/marks/assessment-types/` - Assessment type list
- `/marks/assessment-types/create/` - Create assessment type
- `/marks/assessment-types/<id>/edit/` - Edit assessment type

### Grade Scale Management
- `/marks/grade-scales/` - Grade scale list
- `/marks/grade-scales/create/` - Create grade scale
- `/marks/grade-scales/<id>/edit/` - Edit grade scale

### Reports
- `/marks/reports/student/` - Student report

### Utilities
- `/marks/utilities/calculate-summaries/` - Calculate grade summaries

### AJAX Endpoints
- `/marks/ajax/subjects-by-course/` - Get subjects by course
- `/marks/ajax/students-by-course/` - Get students by course
- `/marks/ajax/marks/<id>/status/` - Update mark status

---

## 👨‍🏫 Faculty Management

**Base URL:** `/faculty/`

### Dashboard
- `/faculty/` - Faculty dashboard

### Faculty Management
- `/faculty/faculty/` - Faculty list
- `/faculty/faculty/create/` - Create faculty
- `/faculty/faculty/<id>/` - Faculty details
- `/faculty/faculty/<id>/edit/` - Edit faculty

### Faculty Onboarding
- `/faculty/onboarding/` - Onboarding list
- `/faculty/onboarding/create/` - Create onboarding
- `/faculty/onboarding/<id>/` - Onboarding details
- `/faculty/onboarding/<id>/approve/` - Approve onboarding
- `/faculty/onboarding/<id>/reject/` - Reject onboarding

### Leave Request Management
- `/faculty/leave-requests/` - Leave request list
- `/faculty/leave-requests/create/` - Create leave request
- `/faculty/leave-requests/<id>/` - Leave request details
- `/faculty/leave-requests/<id>/approve/` - Approve leave request
- `/faculty/leave-requests/<id>/reject/` - Reject leave request

### Backup Schedule
- `/faculty/backup-schedules/` - Backup schedule list
- `/faculty/backup-schedules/create/` - Create backup schedule
- `/faculty/backup-schedules/<id>/` - Backup schedule details

### Faculty Payment
- `/faculty/payments/` - Faculty payment list
- `/faculty/payments/create/` - Create faculty payment
- `/faculty/payments/<id>/` - Faculty payment details

### Exam Request Management
- `/faculty/exam-requests/` - Exam request list
- `/faculty/exam-requests/create/` - Create exam request
- `/faculty/exam-requests/<id>/` - Exam request details
- `/faculty/exam-requests/<id>/approve/` - Approve exam request

### Reports
- `/faculty/attendance-report/` - Faculty attendance report

### AJAX Endpoints
- `/faculty/ajax/faculty/<faculty_id>/courses/` - Get faculty courses
- `/faculty/ajax/course/<course_id>/students/` - Get course students

---

## 🎓 Batch Management

**Base URL:** `/batches/`

### ⚠️ WARNING: This Module is NOT Functional

**Status:** Placeholder - All URLs show "under development" message

All URLs listed below exist in the routing but are **NOT IMPLEMENTED**. They will show a placeholder page.

---

### Dashboard
- `/batches/` - Batch dashboard ⚠️ Placeholder

### Batch Management
- `/batches/batches/` - Batch list
- `/batches/batches/create/` - Create batch
- `/batches/batches/<id>/` - Batch details
- `/batches/batches/<id>/edit/` - Edit batch
- `/batches/batches/<id>/delete/` - Delete batch

### Student Management in Batches
- `/batches/batches/<batch_id>/students/` - Batch students
- `/batches/batches/<batch_id>/students/add/` - Add student to batch
- `/batches/batches/<batch_id>/students/<student_id>/remove/` - Remove student from batch

### Batch Transfer
- `/batches/transfers/` - Transfer list
- `/batches/transfers/create/` - Create transfer
- `/batches/transfers/<id>/` - Transfer details
- `/batches/transfers/<id>/approve/` - Approve transfer
- `/batches/transfers/<id>/reject/` - Reject transfer

### Faculty Changes
- `/batches/faculty-changes/` - Faculty change list
- `/batches/faculty-changes/create/` - Create faculty change
- `/batches/faculty-changes/<id>/` - Faculty change details
- `/batches/faculty-changes/<id>/approve/` - Approve faculty change

### WhatsApp Group Management
- `/batches/whatsapp-groups/` - WhatsApp group list
- `/batches/whatsapp-groups/create/` - Create WhatsApp group
- `/batches/whatsapp-groups/<id>/` - WhatsApp group details
- `/batches/whatsapp-groups/<id>/sync/` - Sync WhatsApp group

### API Endpoints
- `/batches/api/batch/<batch_id>/students/` - Batch students API
- `/batches/api/transfer/validate/` - Validate transfer API

---

## 🚌 Transport Management

**Base URL:** `/transport/`

### ⚠️ WARNING: This Module is NOT Functional

**Status:** Placeholder - All URLs show "under development" message

All URLs listed below exist in the routing but are **NOT IMPLEMENTED**. They will show a placeholder page.

---

### Dashboard
- `/transport/` - Transport dashboard ⚠️ Placeholder

### Vendor Management
- `/transport/vendors/` - Vendor list
- `/transport/vendors/create/` - Create vendor
- `/transport/vendors/<id>/` - Vendor details
- `/transport/vendors/<id>/edit/` - Edit vendor
- `/transport/vendors/<id>/delete/` - Delete vendor

### Vendor Requests & Approval
- `/transport/vendor-requests/` - Vendor request list
- `/transport/vendor-requests/create/` - Create vendor request
- `/transport/vendor-requests/<id>/` - Vendor request details
- `/transport/vendor-requests/<id>/approve/` - Approve vendor request
- `/transport/vendor-requests/<id>/reject/` - Reject vendor request

### Student Transport Assignments
- `/transport/assignments/` - Assignment list
- `/transport/assignments/create/` - Create assignment
- `/transport/assignments/<id>/` - Assignment details
- `/transport/assignments/<id>/edit/` - Edit assignment
- `/transport/assignments/<id>/delete/` - Delete assignment

### Vendor Payments
- `/transport/payments/` - Payment list
- `/transport/payments/create/` - Create payment
- `/transport/payments/<id>/` - Payment details
- `/transport/payments/<id>/edit/` - Edit payment
- `/transport/payments/<id>/approve/` - Approve payment

### Monthly Payment Generation
- `/transport/payment-generation/` - Payment generation list
- `/transport/payment-generation/create/` - Create payment generation
- `/transport/payment-generation/<id>/` - Payment generation details
- `/transport/payment-generation/<id>/generate/` - Generate payments

### Vendor Ratings
- `/transport/ratings/` - Rating list
- `/transport/ratings/create/` - Create rating
- `/transport/vendors/<vendor_id>/rate/` - Rate vendor

### Reports
- `/transport/reports/` - Reports dashboard
- `/transport/reports/vendor-payments/` - Vendor payments report
- `/transport/reports/student-transport/` - Student transport report

### API Endpoints
- `/transport/api/vendor/<vendor_id>/assignments/` - Vendor assignments API
- `/transport/api/student/<student_id>/transport-history/` - Student transport history API

---

## 📦 Kit Materials Management

**Base URL:** `/kits/`

### ⚠️ WARNING: This Module is NOT Functional

**Status:** Placeholder - All URLs show "under development" message

**Alternative:** Use `/coursefee/kits/` for course fee kit management (which IS functional).

All URLs listed below exist in the routing but are **NOT IMPLEMENTED**. They will show a placeholder page.

---

### Dashboard
- `/kits/` - Kit materials dashboard ⚠️ Placeholder

### Material Categories
- `/kits/categories/` - Category list
- `/kits/categories/create/` - Create category
- `/kits/categories/<id>/` - Category details
- `/kits/categories/<id>/edit/` - Edit category

### Suppliers
- `/kits/suppliers/` - Supplier list
- `/kits/suppliers/create/` - Create supplier
- `/kits/suppliers/<id>/` - Supplier details
- `/kits/suppliers/<id>/edit/` - Edit supplier

### Materials
- `/kits/materials/` - Material list
- `/kits/materials/create/` - Create material
- `/kits/materials/<id>/` - Material details
- `/kits/materials/<id>/edit/` - Edit material
- `/kits/materials/<id>/delete/` - Delete material

### Material Kits
- `/kits/kits/` - Kit list
- `/kits/kits/create/` - Create kit
- `/kits/kits/<id>/` - Kit details
- `/kits/kits/<id>/edit/` - Edit kit
- `/kits/kits/<id>/delete/` - Delete kit

### Kit Materials (Managing Materials in Kits)
- `/kits/kits/<kit_id>/materials/` - Kit materials
- `/kits/kits/<kit_id>/materials/add/` - Add material to kit
- `/kits/kits/<kit_id>/materials/<material_id>/remove/` - Remove material from kit

### Stock Management
- `/kits/stock/` - Stock dashboard
- `/kits/stock/movements/` - Stock movement list
- `/kits/stock/movements/create/` - Create stock movement
- `/kits/materials/<material_id>/adjust-stock/` - Adjust material stock

### Kit Assembly
- `/kits/assembly/` - Assembly dashboard
- `/kits/assembly/logs/` - Assembly log list
- `/kits/assembly/create/` - Create assembly
- `/kits/assembly/<id>/` - Assembly details
- `/kits/kits/<kit_id>/assemble/` - Assemble kit

### Reports
- `/kits/reports/` - Reports dashboard
- `/kits/reports/inventory/` - Inventory report
- `/kits/reports/low-stock/` - Low stock report
- `/kits/reports/kit-costs/` - Kit costs report

### Integration with Course Fee Kit
- `/kits/sync/` - Sync dashboard
- `/kits/kits/<kit_id>/sync-coursefee/` - Sync with course fee

### API Endpoints
- `/kits/api/materials/search/` - Material search API
- `/kits/api/kit/<kit_id>/can-assemble/` - Check kit assembly API
- `/kits/api/materials/low-stock/` - Low stock materials API

---

## 📢 Broadcast & Lead Management

**Base URL:** `/broadcast/`

### ⚠️ WARNING: This Module is NOT Functional

**Status:** Placeholder - All URLs show "under development" message

All URLs listed below exist in the routing but are **NOT IMPLEMENTED**. They will show a placeholder page.

---

### Dashboard
- `/broadcast/` - Broadcast dashboard ⚠️ Placeholder

### Broadcast Templates
- `/broadcast/templates/` - Template list
- `/broadcast/templates/create/` - Create template
- `/broadcast/templates/<id>/` - Template details
- `/broadcast/templates/<id>/edit/` - Edit template
- `/broadcast/templates/<id>/delete/` - Delete template

### Broadcasts
- `/broadcast/broadcasts/` - Broadcast list
- `/broadcast/broadcasts/create/` - Create broadcast
- `/broadcast/broadcasts/<id>/` - Broadcast details
- `/broadcast/broadcasts/<id>/edit/` - Edit broadcast
- `/broadcast/broadcasts/<id>/send/` - Send broadcast
- `/broadcast/broadcasts/<id>/cancel/` - Cancel broadcast

### General Broadcasts
- `/broadcast/general/` - General broadcast
- `/broadcast/general/new-batch/` - New batch broadcast
- `/broadcast/general/holiday/` - Holiday broadcast

### Specific Broadcasts
- `/broadcast/specific/` - Specific broadcast
- `/broadcast/specific/batch/` - Batch broadcast
- `/broadcast/specific/course/` - Course broadcast
- `/broadcast/specific/fee-reminder/` - Fee reminder broadcast

### Lead Management
- `/broadcast/leads/` - Lead list
- `/broadcast/leads/create/` - Create lead
- `/broadcast/leads/<id>/` - Lead details
- `/broadcast/leads/<id>/edit/` - Edit lead
- `/broadcast/leads/<id>/delete/` - Delete lead

### Lead Activities
- `/broadcast/leads/<lead_id>/activities/` - Lead activities
- `/broadcast/leads/<lead_id>/activities/add/` - Add lead activity
- `/broadcast/activities/<id>/edit/` - Edit lead activity

### Lead Scoring
- `/broadcast/leads/<lead_id>/score/` - Lead score
- `/broadcast/leads/<lead_id>/score/calculate/` - Calculate lead score

### Communication Logs
- `/broadcast/communications/` - Communication log list
- `/broadcast/communications/<id>/` - Communication log details

### Reports and Analytics
- `/broadcast/reports/` - Reports dashboard
- `/broadcast/reports/broadcast-performance/` - Broadcast performance report
- `/broadcast/reports/lead-conversion/` - Lead conversion report
- `/broadcast/reports/communication-costs/` - Communication costs report

### API Endpoints
- `/broadcast/api/leads/search/` - Lead search API
- `/broadcast/api/broadcast/<broadcast_id>/recipients/` - Broadcast recipients API
- `/broadcast/api/templates/<template_id>/content/` - Template content API
- `/broadcast/api/leads/<lead_id>/quick-update/` - Lead quick update API

---

## 🔧 Django Admin Panel

**Admin URL:** `/admin/`

- `/admin/` - Django default admin interface

---

## 📱 Media Files (Development Only)

**Media URL:** `/media/`

- `/media/<path>` - Access uploaded media files (student photos, documents, etc.)

---

## 📝 Quick Access URLs

### Most Commonly Used URLs:

| Function | URL |
|----------|-----|
| **Home Dashboard** | `/` |
| **Login** | `/accounts/login/` |
| **Logout** | `/accounts/logout/` |
| **Student List** | `/students/` |
| **Add Student** | `/students/create/` |
| **Mark Attendance** | `/attendance/create/` |
| **Bulk Attendance** | `/attendance/bulk/` |
| **Course List** | `/coursefee/courses/` |
| **Enroll Student** | `/coursefee/enrollments/create/` |
| **Record Payment** | `/coursefee/payments/create/` |
| **Create Invoice** | `/coursefee/invoices/create/` |
| **Admin Panel** | `/admin/` |
| **System Dashboard** | `/system/` |

---

## 🚀 URL Naming Conventions

EduPulse follows these naming conventions for URLs:

### List Views
- Pattern: `/<module>/` or `/<module>/<entity>/`
- Example: `/students/`, `/coursefee/courses/`

### Create Views
- Pattern: `/<module>/<entity>/create/`
- Example: `/students/create/`, `/coursefee/courses/create/`

### Detail Views
- Pattern: `/<module>/<entity>/<id>/`
- Example: `/students/1/`, `/coursefee/courses/5/`

### Edit/Update Views
- Pattern: `/<module>/<entity>/<id>/edit/`
- Example: `/students/1/edit/`, `/coursefee/courses/5/edit/`

### Delete Views
- Pattern: `/<module>/<entity>/<id>/delete/`
- Example: `/students/1/delete/`, `/coursefee/courses/5/delete/`

### Action Views
- Pattern: `/<module>/<entity>/<id>/<action>/`
- Example: `/faculty/leave-requests/1/approve/`, `/batches/transfers/2/reject/`

### Report/Export Views
- Pattern: `/<module>/<entity>/report/` or `/<module>/<entity>/export/`
- Example: `/attendance/report/`, `/students/export/`

### AJAX/API Endpoints
- Pattern: `/<module>/ajax/<action>/` or `/<module>/api/<action>/`
- Example: `/coursefee/ajax/course-fees/1/`, `/batches/api/batch/1/students/`

---

## 📌 Notes

1. **`<id>`** represents a numeric ID (e.g., 1, 2, 3)
2. **Base URLs** are prefixed to all module URLs
3. **AJAX endpoints** are for frontend JavaScript interactions
4. **API endpoints** provide JSON responses for external integrations
5. All URLs require **authentication** except login and password reset
6. **Media files** are only served in development mode (DEBUG=True)

---

## 🔍 Finding a Specific URL

To find a specific URL in Django templates, use:
```django
{% url 'url_name' %}
```

Examples:
```django
{% url 'student_list' %}
{% url 'student_detail' pk=student.id %}
{% url 'course_edit' pk=course.id %}
```

---

## 📅 Last Updated

**Date:** December 3, 2025  
**Version:** 1.0  
**Project:** EduPulse School Management System

---

## 💡 Tips

- Bookmark frequently used URLs in your browser
- Use the dashboard links for quick navigation
- AJAX URLs are typically called from JavaScript, not accessed directly
- Check URL parameters when using detail/edit/delete views
- All module dashboards are accessible from the main navigation

---

**Need Help?** Contact the development team or refer to the individual module documentation.

