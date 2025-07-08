# Dashboard API - Postman Testing Guide

## Overview
This guide provides instructions for testing the Dashboard API endpoints using Postman.

## Base URL
```
http://localhost:8000/api/dashboard/
```

## Endpoints

### 1. Admin Dashboard Statistics

Get dashboard statistics including counts of courses, students, users, departments, payments, and questions.

**Endpoint:** `GET /api/dashboard/admin/`

**Authentication:** None required

**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Request:**
```
Method: GET
URL: http://localhost:8000/api/dashboard/admin/
```

**Response Example:**
```json
{
  "total_courses": 6,
  "total_students": 4,
  "total_users": 7,
  "total_departments": 8,
  "total_payments": 8,
  "total_questions": 8
}
```

**Response Fields:**
- `total_courses`: Total number of courses available in the system
- `total_students`: Total number of users with role 'student'
- `total_users`: Total number of users with role 'user'
- `total_departments`: Total number of departments available
- `total_payments`: Total number of payment records
- `total_questions`: Total number of active questions (excludes deleted questions)

**Status Codes:**
- `200 OK`: Statistics retrieved successfully
- `500 Internal Server Error`: Server error

## Testing Steps

### Step 1: Setup Postman
1. Open Postman
2. Create a new collection named "Dashboard API"
3. Add environment variables:
   - `base_url`: `http://localhost:8000`

### Step 2: Test Admin Dashboard Endpoint
1. Create a new request in the Dashboard API collection
2. Set request details:
   - Name: "Get Admin Dashboard Stats"
   - Method: `GET`
   - URL: `{{base_url}}/api/dashboard/admin/`
3. Click "Send"
4. Verify the response contains all required fields

### Step 3: Automated Tests
Add the following test script to the request:

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has all required fields", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('total_courses');
    pm.expect(jsonData).to.have.property('total_students');
    pm.expect(jsonData).to.have.property('total_users');
    pm.expect(jsonData).to.have.property('total_departments');
    pm.expect(jsonData).to.have.property('total_payments');
    pm.expect(jsonData).to.have.property('total_questions');
});

pm.test("All values are numbers", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData.total_courses).to.be.a('number');
    pm.expect(jsonData.total_students).to.be.a('number');
    pm.expect(jsonData.total_users).to.be.a('number');
    pm.expect(jsonData.total_departments).to.be.a('number');
    pm.expect(jsonData.total_payments).to.be.a('number');
    pm.expect(jsonData.total_questions).to.be.a('number');
});

pm.test("All values are non-negative", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData.total_courses).to.be.at.least(0);
    pm.expect(jsonData.total_students).to.be.at.least(0);
    pm.expect(jsonData.total_users).to.be.at.least(0);
    pm.expect(jsonData.total_departments).to.be.at.least(0);
    pm.expect(jsonData.total_payments).to.be.at.least(0);
    pm.expect(jsonData.total_questions).to.be.at.least(0);
});
```

## Sample Postman Collection

You can import the following collection JSON into Postman:

```json
{
    "info": {
        "name": "Dashboard API",
        "description": "Collection for testing Dashboard API endpoints",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": [
        {
            "name": "Get Admin Dashboard Stats",
            "request": {
                "method": "GET",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json",
                        "type": "text"
                    }
                ],
                "url": {
                    "raw": "{{base_url}}/api/dashboard/admin/",
                    "host": [
                        "{{base_url}}"
                    ],
                    "path": [
                        "api",
                        "dashboard",
                        "admin",
                        ""
                    ]
                },
                "description": "Get dashboard statistics for admin panel"
            },
            "response": []
        }
    ],
    "variable": [
        {
            "key": "base_url",
            "value": "http://localhost:8000",
            "type": "string"
        }
    ]
}
```

## Notes
- No authentication is required for this endpoint
- The endpoint returns real-time counts from the database
- Deleted questions (is_deleted=True) are excluded from the total_questions count
- The response format is always JSON
