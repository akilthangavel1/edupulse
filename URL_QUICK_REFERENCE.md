# EduPulse - URL Quick Reference Cheat Sheet

## 🎯 Most Used URLs

### Authentication
```
/accounts/login/          - Login page
/accounts/logout/         - Logout
/accounts/register/       - Registration
/accounts/password_reset/ - Reset password
```

### Student Management
```
/                         - Dashboard (Home)
/students/                - Student list
/students/create/         - Add new student
/students/<id>/           - View student details
/students/<id>/edit/      - Edit student
/students/export/         - Export students CSV
```

### Attendance
```
/attendance/              - Attendance list
/attendance/dashboard/    - Attendance dashboard
/attendance/create/       - Mark attendance (single)
/attendance/bulk/         - Mark attendance (bulk)
/attendance/report/       - Generate report
```

### Course Fee Management
```
/coursefee/                        - Course fee dashboard
/coursefee/courses/                - Course list
/coursefee/courses/create/         - Add course
/coursefee/enrollments/create/     - Enroll student (Fee Entry)
/coursefee/payments/create/        - Record payment
/coursefee/invoices/create/        - Create invoice
/coursefee/reports/financial/      - Financial report
```

### Marks/Grades
```
/marks/                   - Marks dashboard
/marks/subjects/          - Subject list
/marks/marks/create/      - Enter marks
/marks/marks/bulk-entry/  - Bulk mark entry
/marks/reports/student/   - Student report
```

### Faculty Management
```
/faculty/                 - Faculty dashboard
/faculty/faculty/         - Faculty list
/faculty/faculty/create/  - Add faculty
/faculty/leave-requests/  - Leave requests
/faculty/payments/        - Faculty payments
```

### Batch Management
```
/batches/                 - Batch dashboard
/batches/batches/         - Batch list
/batches/batches/create/  - Create batch
/batches/transfers/       - Transfer requests
```

### Transport
```
/transport/               - Transport dashboard
/transport/vendors/       - Vendor list
/transport/assignments/   - Student assignments
/transport/payments/      - Vendor payments
```

### Kit Materials
```
/kits/                    - Kit dashboard
/kits/materials/          - Material list
/kits/kits/               - Kit list
/kits/stock/              - Stock management
/kits/assembly/           - Kit assembly
```

### Broadcast & Leads
```
/broadcast/               - Broadcast dashboard
/broadcast/broadcasts/    - Broadcast list
/broadcast/leads/         - Lead management
/broadcast/templates/     - Message templates
```

### Django Admin (Functional)
```
/admin/                           - Admin dashboard
/admin/auth/user/                 - User management
/admin/auth/group/                - Groups (roles)
/admin/xstudent/newstudent/       - Students (admin)
/admin/xcoursefee/course/         - Courses (admin)
/admin/xcoursefee/payment/        - Payments (admin)
/admin/xmark/mark/                - Marks (admin)
/admin/xtrainer/faculty/          - Faculty (admin)
```

### System Admin (Not Functional - Use /admin/ instead)
```
/system/                  - ⚠️ Placeholder (use /admin/ instead)
/system/users/            - ⚠️ Placeholder (use /admin/auth/user/)
/system/audit/            - ⚠️ Placeholder
/system/backup/           - ⚠️ Placeholder
```

---

## 📱 URL Pattern Reference

### Standard CRUD Operations
```
/<module>/                        - List all
/<module>/create/                 - Create new
/<module>/<id>/                   - View details
/<module>/<id>/edit/              - Edit/Update
/<module>/<id>/delete/            - Delete
```

### Common Actions
```
/<module>/<id>/approve/           - Approve request
/<module>/<id>/reject/            - Reject request
/<module>/<id>/activate/          - Activate item
/<module>/<id>/deactivate/        - Deactivate item
/<module>/<id>/send/              - Send/Publish
/<module>/<id>/cancel/            - Cancel action
```

---

## 🔗 URL Names for Templates

Use in Django templates: `{% url 'name' %}`

### Students
```python
'student_dashboard'     # /
'student_list'          # /students/
'student_create'        # /students/create/
'student_detail'        # /students/<id>/
'student_edit'          # /students/<id>/edit/
'student_delete'        # /students/<id>/delete/
'student_export'        # /students/export/
```

### Attendance
```python
'attendance_list'       # /attendance/
'attendance_dashboard'  # /attendance/dashboard/
'attendance_create'     # /attendance/create/
'attendance_bulk_create' # /attendance/bulk/
'attendance_detail'     # /attendance/<id>/
'attendance_edit'       # /attendance/<id>/edit/
'attendance_report'     # /attendance/report/
```

### Course Fee
```python
'coursefee_dashboard'   # /coursefee/
'course_list'           # /coursefee/courses/
'course_create'         # /coursefee/courses/create/
'course_detail'         # /coursefee/courses/<id>/
'enrollment_create'     # /coursefee/enrollments/create/
'payment_create'        # /coursefee/payments/create/
'invoice_create'        # /coursefee/invoices/create/
'financial_report'      # /coursefee/reports/financial/
```

### Marks
```python
'marks_dashboard'       # /marks/
'subject_list'          # /marks/subjects/
'mark_create'           # /marks/marks/create/
'bulk_mark_entry'       # /marks/marks/bulk-entry/
'student_report'        # /marks/reports/student/
```

### Faculty
```python
'faculty_dashboard'     # /faculty/
'faculty_list'          # /faculty/faculty/
'faculty_create'        # /faculty/faculty/create/
'faculty_leave_request_list' # /faculty/leave-requests/
'faculty_payment_list'  # /faculty/payments/
```

---

## 🎨 Module Prefixes

| Module | Prefix | Description | Status |
|--------|--------|-------------|--------|
| **Django Admin** | `/admin/` | Django admin panel | ✅ Functional |
| **Accounts** | `/accounts/` | Authentication | ✅ Functional |
| **Students** | `/` | Student management (root) | ✅ Functional |
| **Course Fee** | `/coursefee/` | Fee & enrollment | ✅ Functional |
| **Marks** | `/marks/` | Grades & assessments | ✅ Functional |
| **Faculty** | `/faculty/` | Teacher management | ✅ Functional |
| **System Admin** | `/system/` | System administration | ⚠️ Use `/admin/` |
| **Batch** | `/batches/` | Class groups | ⚠️ Placeholder |
| **Transport** | `/transport/` | Transport vendors | ⚠️ Placeholder |
| **Kit** | `/kits/` | Material inventory | ⚠️ Placeholder |
| **Broadcast** | `/broadcast/` | Communication | ⚠️ Placeholder |

---

## 🔐 Access Levels

### Public (No Login Required)
- `/accounts/login/` - Login page
- `/accounts/register/` - Registration
- `/accounts/password_reset/` - Password reset

### Authenticated Users (Login Required)
- All student, course, mark, faculty URLs
- Access depends on user role/permissions
- Most application features

### Admin/Superuser Only
- `/admin/` - Django admin panel (full access)
- `/admin/auth/user/` - User management
- `/admin/auth/group/` - Role management

### Staff Users (in Django Admin)
- Can access `/admin/` with limited permissions
- Permissions set by admin per model
- Can view/edit assigned modules only

---

## 💡 Quick Tips

### In Templates
```django
<!-- Simple URL -->
<a href="{% url 'student_list' %}">Students</a>

<!-- URL with parameter -->
<a href="{% url 'student_detail' pk=student.id %}">View</a>

<!-- URL with multiple parameters -->
<a href="{% url 'kit_materials' kit_id=kit.id %}">Materials</a>
```

### In Views (Python)
```python
from django.shortcuts import redirect

# Simple redirect
return redirect('student_list')

# Redirect with parameter
return redirect('student_detail', pk=student.id)

# Redirect with reverse
from django.urls import reverse
url = reverse('student_detail', kwargs={'pk': student.id})
return redirect(url)
```

### In JavaScript/AJAX
```javascript
// Using Django template tag in JS
const url = "{% url 'api_batch_students' batch_id=batch.id %}";

// Or construct URL manually
const url = `/coursefee/ajax/course-fees/${courseId}/`;
```

---

## 📋 Common URL Patterns

### List + Filter
```
/students/?search=John&grade=5&status=active
/attendance/?date_from=2025-01-01&date_to=2025-12-31
```

### Pagination
```
/students/?page=2
/coursefee/courses/?page=3
```

### Sorting
```
/students/?sort=name
/payments/?sort=-date  (descending)
```

---

## 🔄 URL Redirects After Actions

| Action | Redirect To |
|--------|-------------|
| Create Student | Student detail page |
| Edit Student | Student detail page |
| Delete Student | Student list |
| Mark Attendance | Attendance list |
| Record Payment | Payment detail page |
| Create Invoice | Invoice detail page |

---

## 📞 Support URLs

Need to report an issue or bug?
- Contact system administrator
- Check audit logs: `/system/audit/`
- View system health: `/system/health/`

---

**Quick Reference Version 1.0** | Last Updated: December 3, 2025

