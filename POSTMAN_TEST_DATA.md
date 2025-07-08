# Postman Testing Guide for Student Creation API

## 🚀 Quick Start

### 1. Start Django Server
```bash
cd "/Users/nashway/HappiAppz/DEVELOPMENT/PROJECTS/DAVID ACADEMY/edu-portal-api-templete-service"
source .venv/bin/activate
python manage.py runserver
```

### 2. Server URL
```
http://127.0.0.1:8000
```

## 📋 Postman Test Configuration

### **API Endpoint**
```
POST http://127.0.0.1:8000/api/students/create
```

### **Headers**
```
Content-Type: application/json
Accept: application/json
```

### **Method**
```
POST
```

## 🧪 Test Data

### **Test Case 1: Valid Student Creation**

**URL:** `http://127.0.0.1:8000/api/students/create`
**Method:** `POST`
**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Body (raw JSON):**
```json
{
  "name": "John Student",
  "address": "123 Main St, Apt 4B, Downtown Area",
  "district": "Central District",
  "state": "California",
  "pinCode": "90001",
  "courses": ["NCLEX", "DHA"],
  "mobile": "555-123-4567",
  "countryCode": "+1",
  "mobileVerified": true,
  "email": "john.student@example.com",
  "emailVerified": true,
  "startDate": "2024-01-15",
  "endDate": "2024-07-15",
  "username": "john_student",
  "password": "password123"
}
```

**Expected Response (201 Created):**
```json
{
  "message": "Student created successfully",
  "user": {
    "id": 1,
    "email": "john.student@example.com",
    "username": "john_student",
    "first_name": "",
    "last_name": "",
    "is_active": true,
    "role": "student",
    "student_profile": {
      "id": 1,
      "user": 1,
      "user_email": "john.student@example.com",
      "name": "John Student",
      "address": "123 Main St, Apt 4B, Downtown Area",
      "district": "Central District",
      "state": "California",
      "pin_code": "90001",
      "courses": ["NCLEX", "DHA"],
      "mobile": "555-123-4567",
      "country_code": "+1",
      "mobile_verified": true,
      "email": "john.student@example.com",
      "email_verified": true,
      "start_date": "2024-01-15",
      "end_date": "2024-07-15",
      "is_enrollment_active": false,
      "full_mobile": "+1555-123-4567",
      "created_at": "2025-07-03T17:43:40.123456Z",
      "updated_at": "2025-07-03T17:43:40.123456Z"
    }
  },
  "student_id": 1
}
```

---

### **Test Case 2: Another Valid Student**

**URL:** `http://127.0.0.1:8000/api/students/create`
**Method:** `POST`

**Body (raw JSON):**
```json
{
  "name": "Jane Doe",
  "address": "456 Oak Avenue, Suite 12B",
  "district": "Downtown",
  "state": "Texas",
  "pinCode": "75001",
  "courses": ["NCLEX", "HESI", "RN"],
  "mobile": "555-987-6543",
  "countryCode": "+1",
  "mobileVerified": false,
  "email": "jane.doe@example.com",
  "emailVerified": false,
  "startDate": "2024-02-01",
  "endDate": "2024-08-01",
  "username": "jane_doe",
  "password": "SecurePass123!"
}
```

---

### **Test Case 3: International Student**

**URL:** `http://127.0.0.1:8000/api/students/create`
**Method:** `POST`

**Body (raw JSON):**
```json
{
  "name": "Raj Patel",
  "address": "789 Gandhi Road, Sector 15",
  "district": "Andheri",
  "state": "Maharashtra",
  "pinCode": "400053",
  "courses": ["NCLEX", "CGFNS"],
  "mobile": "9876543210",
  "countryCode": "+91",
  "mobileVerified": true,
  "email": "raj.patel@example.com",
  "emailVerified": true,
  "startDate": "2024-03-01",
  "endDate": "2024-09-01",
  "username": "raj_patel",
  "password": "MySecurePassword456!"
}
```

---

### **Test Case 4: Minimal Required Fields**

**URL:** `http://127.0.0.1:8000/api/students/create`
**Method:** `POST`

**Body (raw JSON):**
```json
{
  "name": "Michael Brown",
  "address": "321 Pine Street",
  "district": "Westside",
  "state": "Florida",
  "pinCode": "33101",
  "mobile": "555-555-5555",
  "email": "michael.brown@example.com",
  "startDate": "2024-04-01",
  "endDate": "2024-10-01",
  "username": "michael_brown",
  "password": "TestPassword789!"
}
```

---

## ❌ Error Test Cases

### **Test Case 5: Missing Required Fields**

**URL:** `http://127.0.0.1:8000/api/students/create`
**Method:** `POST`

**Body (raw JSON):**
```json
{
  "name": "Incomplete Student",
  "email": "incomplete@example.com",
  "username": "incomplete_student",
  "password": "password123"
}
```

**Expected Response (400 Bad Request):**
```json
{
  "error": "Validation failed",
  "details": {
    "address": ["This field is required."],
    "district": ["This field is required."],
    "state": ["This field is required."],
    "pinCode": ["This field is required."],
    "mobile": ["This field is required."],
    "startDate": ["This field is required."],
    "endDate": ["This field is required."]
  }
}
```

---

### **Test Case 6: Duplicate Email**

**URL:** `http://127.0.0.1:8000/api/students/create`
**Method:** `POST`

**Body (raw JSON):**
```json
{
  "name": "Duplicate User",
  "address": "999 Duplicate Lane",
  "district": "Error District",
  "state": "Error State",
  "pinCode": "99999",
  "mobile": "555-999-9999",
  "email": "john.student@example.com",
  "startDate": "2024-05-01",
  "endDate": "2024-11-01",
  "username": "duplicate_user",
  "password": "password123"
}
```

**Expected Response (400 Bad Request):**
```json
{
  "error": "Validation failed",
  "details": {
    "email": ["User with this email already exists."]
  }
}
```

---

### **Test Case 7: Invalid Date Range**

**URL:** `http://127.0.0.1:8000/api/students/create`
**Method:** `POST`

**Body (raw JSON):**
```json
{
  "name": "Invalid Date User",
  "address": "123 Invalid Date Street",
  "district": "Date District",
  "state": "Date State",
  "pinCode": "12345",
  "mobile": "555-111-2222",
  "email": "invalid.date@example.com",
  "startDate": "2024-12-01",
  "endDate": "2024-06-01",
  "username": "invalid_date_user",
  "password": "password123"
}
```

**Expected Response (400 Bad Request):**
```json
{
  "error": "Validation failed",
  "details": {
    "endDate": ["End date must be after start date."]
  }
}
```

---

## 📊 Postman Collection JSON

Copy and import this into Postman:

```json
{
  "info": {
    "name": "Student Creation API",
    "description": "Test collection for student creation endpoint",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Create Student - Valid",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"name\": \"John Student\",\n  \"address\": \"123 Main St, Apt 4B, Downtown Area\",\n  \"district\": \"Central District\",\n  \"state\": \"California\",\n  \"pinCode\": \"90001\",\n  \"courses\": [\"NCLEX\", \"DHA\"],\n  \"mobile\": \"555-123-4567\",\n  \"countryCode\": \"+1\",\n  \"mobileVerified\": true,\n  \"email\": \"john.student@example.com\",\n  \"emailVerified\": true,\n  \"startDate\": \"2024-01-15\",\n  \"endDate\": \"2024-07-15\",\n  \"username\": \"john_student\",\n  \"password\": \"password123\"\n}"
        },
        "url": {
          "raw": "http://127.0.0.1:8000/api/students/create",
          "protocol": "http",
          "host": ["127", "0", "0", "1"],
          "port": "8000",
          "path": ["api", "students", "create"]
        }
      }
    },
    {
      "name": "Create Student - Missing Fields",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"name\": \"Incomplete Student\",\n  \"email\": \"incomplete@example.com\",\n  \"username\": \"incomplete_student\",\n  \"password\": \"password123\"\n}"
        },
        "url": {
          "raw": "http://127.0.0.1:8000/api/students/create",
          "protocol": "http",
          "host": ["127", "0", "0", "1"],
          "port": "8000",
          "path": ["api", "students", "create"]
        }
      }
    }
  ]
}
```

---

## 🔧 Testing Steps

### **Step 1: Start Server**
```bash
cd "/Users/nashway/HappiAppz/DEVELOPMENT/PROJECTS/DAVID ACADEMY/edu-portal-api-templete-service"
source .venv/bin/activate
python manage.py runserver
```

### **Step 2: Verify Server is Running**
Open browser and go to: `http://127.0.0.1:8000/api/swagger/`

### **Step 3: Test in Postman**
1. Open Postman
2. Create new request
3. Set method to `POST`
4. Set URL to `http://127.0.0.1:8000/api/students/create`
5. Set header `Content-Type: application/json`
6. Copy any test data above into the body
7. Send request

### **Step 4: Check Response**
- **Success**: Status 201 with student data
- **Error**: Status 400 with validation errors

---

## 🎯 Quick Test Commands

You can also test using curl:

```bash
# Test 1: Valid student
curl -X POST http://127.0.0.1:8000/api/students/create \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Student",
    "address": "123 Test Street",
    "district": "Test District",
    "state": "Test State",
    "pinCode": "12345",
    "mobile": "555-TEST-001",
    "email": "test.student@example.com",
    "startDate": "2024-01-01",
    "endDate": "2024-12-31",
    "username": "test_student",
    "password": "TestPassword123!"
  }'
```

Happy testing! 🚀
