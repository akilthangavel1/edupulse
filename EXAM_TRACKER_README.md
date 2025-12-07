# Exam Details Tracker - Quick Guide

## Overview

A simple exam tracker/filter system for recording and managing exam details at `/faculty/exam-requests/`

## Features

### 📊 Statistics Dashboard
- **Pending**: Yellow card showing pending exams
- **Scheduled**: Green card showing scheduled exams  
- **Completed**: Blue card showing completed exams
- **Total Exams**: Primary card showing all exam records

### 🔍 Simple Filters

**Three Filter Options:**
1. **Faculty Dropdown**: Filter by specific faculty member
2. **Status Dropdown**: Filter by request status
   - Pending Approval
   - Approved
   - Rejected
   - Scheduled
   - Completed
   - Cancelled
3. **Exam Type Dropdown**: Filter by exam type
   - Quiz
   - Midterm Exam
   - Final Exam
   - Assignment
   - Project Evaluation
   - Oral Exam
   - Practical Exam

### 📋 Exam Details Table

**Columns:**
- Exam ID
- Faculty Name
- Course
- Exam Title
- Exam Type (badge)
- Exam Date & Time
- Status (color-coded badge)
- Actions (View Details button)

### ✨ Features

✅ **Color-Coded Status Badges**
- Yellow: Pending
- Green: Approved
- Blue: Scheduled
- Red: Rejected
- Gray: Cancelled/Other

✅ **Pagination**: Shows 15 requests per page

✅ **Clear Filters**: Quick reset button to remove all filters

✅ **Responsive Design**: Works on all screen sizes

✅ **Empty State**: Shows friendly message when no requests match filters

## How to Use

### Viewing Exam Details

1. Navigate to **Faculty → Exam Requests**
2. View statistics cards at the top
3. Browse all exam details in the table

### Filtering Exams

1. **Select Faculty**: Choose a specific faculty member
2. **Select Status**: Choose request status
3. **Select Exam Type**: Choose exam type
4. **Click "Apply Filters"**: Results update immediately
5. **Click "Clear Filters"** or **"Reset"**: Remove all filters

### Recording Exam Details

1. Click **"Record Exam Details"** button (top right)
2. Fill in complete exam information
3. Save exam details

### Viewing Details

1. Find the exam in the table
2. Click the **blue eye icon** (👁️)
3. View complete exam details

## URL

```
http://127.0.0.1:8000/faculty/exam-requests/
```

## Quick Stats

Access real-time statistics:
- Total number of exam records
- Pending exams needing attention
- Scheduled exams coming up
- Completed exams

## Status Workflow

```
Pending → Approved → Scheduled → Completed
   ↓
Rejected/Cancelled
```

## Tips

1. ✅ Use status filter to focus on pending exams
2. ✅ Filter by faculty to see individual workload
3. ✅ Check scheduled exams to avoid conflicts
4. ✅ Use pagination for large lists
5. ✅ Color badges help quick visual scanning
6. ✅ Record exam details immediately after scheduling

## Future Enhancements

- [ ] Date range filter
- [ ] Search by exam title
- [ ] Export to CSV
- [ ] Bulk approve feature
- [ ] Calendar view
- [ ] Email notifications

---

**Created**: December 2025  
**Page**: `/faculty/exam-requests/`  
**Status**: ✅ Ready to Use

