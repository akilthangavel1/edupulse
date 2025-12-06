# Certificate Issue Tracker - Simple Guide

## 📋 Overview

This is a **simple certificate issue tracker** that records when certificates are given to students. Nothing complicated - just tracks:
- Student name
- Course name  
- Date given
- Certificate number (auto-generated)
- Optional notes

That's it!

---

## 🌐 Access URLs

### Main Dashboard
```
http://edu.brillianzinstitute.com/certificates/
```

### All Pages
- **Dashboard:** `/certificates/`
- **Record New:** `/certificates/create/`
- **View All:** `/certificates/list/`
- **Bulk Record:** `/certificates/bulk-create/`

---

## ✅ How to Use

### 1. Record a Single Certificate

1. Go to `/certificates/create/`
2. Fill in 3 required fields:
   - Student (dropdown)
   - Course (dropdown)
   - Issue Date (date picker)
3. Optional: Add remarks
4. Click **"Save"**
5. Done! Certificate number auto-generated (e.g., CERT/2025/0001)

**Time: 30 seconds**

---

### 2. Record Multiple Certificates (Ceremony)

1. Go to `/certificates/bulk-create/`
2. Select course
3. Set issue date (same for all)
4. Optional: Add remarks
5. Check students to include
6. Click **"Record Certificates"**
7. Done! All certificates created

**Time: 2 minutes for 50 students**

---

### 3. View All Certificates

1. Go to `/certificates/list/`
2. Use search if needed
3. Click certificate number to view details
4. Can edit or delete from here

---

## 📊 What's Tracked

For each certificate record:
- ✅ **Certificate Number** (CERT/2025/0001) - auto-generated
- ✅ **Student Name**
- ✅ **Course Name**
- ✅ **Issue Date** (when given)
- ✅ **Remarks** (optional notes)
- ✅ **Recorded By** (your name)
- ✅ **Recorded At** (timestamp)

---

## 🎯 Simple Workflows

### Daily Use
```
1. Student completes course
2. You give them certificate
3. You record it: Student + Course + Today's Date
4. Done!
```

### Graduation Ceremony
```
1. 20 students get certificates at ceremony
2. Use bulk record
3. Select all 20 students
4. Set ceremony date
5. Done! All recorded
```

---

## 💡 Tips

### Certificate Numbers
- Auto-generated as CERT/YEAR/NUMBER
- Example: CERT/2025/0001, CERT/2025/0002
- Sequential, no gaps

### Remarks Field
Use for notes like:
- "Given at graduation ceremony"
- "Collected by father"
- "Express delivery"
- "Ceremony Dec 10, 2025"

### Searching
- Search by student name
- Search by certificate number
- Filter by course
- Filter by date range

---

## 🗂️ Admin URLs

If you need direct database access:
```
http://edu.brillianzinstitute.com/admin/xcertificate/studentcertificate/
```

---

## ❌ What This Does NOT Do

This is intentionally simple. It does NOT:
- ❌ Track collection status
- ❌ Have verification codes/QR codes
- ❌ Generate PDFs
- ❌ Track grades/percentages
- ❌ Have templates or signatories
- ❌ Send notifications
- ❌ Track revocations

**It just records: Who got what certificate when.**

---

## 📝 Example Records

### Example 1: Single Certificate
```
Certificate Number: CERT/2025/0001
Student: Ahmed Mohammed
Course: Python Programming
Issue Date: Dec 6, 2025
Remarks: Given in office
Recorded By: Admin User
```

### Example 2: Ceremony
```
Certificate Number: CERT/2025/0015
Student: Sara Ali  
Course: Web Development
Issue Date: Dec 10, 2025
Remarks: Graduation Ceremony December 2025
Recorded By: Admin User
```

---

## 🔧 Troubleshooting

### Can't find student?
- Check student is registered in Student Management

### Can't find course?
- Check course exists in Course Management

### Wrong date entered?
- Click Edit button and correct it

### Need to delete?
- Click Delete button on detail page

---

## 📊 Dashboard

The dashboard shows:
- **Total certificates** recorded
- **Recent certificates** (last 10)
- **Certificates by course** (top 5)
- **Quick action buttons**

---

## 🎉 That's It!

Super simple certificate tracking:
1. Record when you give a certificate
2. Search/view records later
3. That's all!

**Main URL:** http://edu.brillianzinstitute.com/certificates/

---

*Simple, fast, effective!*  
*Updated: December 6, 2025*

