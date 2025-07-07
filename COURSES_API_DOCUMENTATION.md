# Courses API Documentation

## Overview
This document provides comprehensive information about the Courses API endpoints, including URLs, request/response formats, and test data for Postman testing.

## Base URL
```
http://localhost:8000/api/courses/
```

## Authentication
No authentication required - all endpoints are publicly accessible.

## API Endpoints

### 1. GET /api/courses/ - List All Courses
**Method:** GET  
**URL:** `http://localhost:8000/api/courses/`  
**Description:** Retrieve a paginated list of all courses  

**Query Parameters:**
- `page` - Page number (optional)
- `search` - Search in code, name, or description (optional)
- `code` - Filter by course code (optional)
- `duration` - Filter by duration (optional)
- `ordering` - Sort by field (options: created_at, updated_at, name, code, -created_at, -updated_at, -name, -code)

**Example Request:**
```
GET http://localhost:8000/api/courses/?search=NCLEX&ordering=-created_at
```

**Example Response:**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "code": "NCLEX",
      "name": "National Council Licensure Examination",
      "description": "Standardized exam that each state board of nursing uses to determine whether a candidate is prepared for entry-level nursing practice.",
      "duration": "3",
      "created_at": "2024-01-01T00:00:00.000Z",
      "updated_at": "2024-01-01T00:00:00.000Z"
    }
  ]
}
```

### 2. POST /api/courses/ - Create New Course
**Method:** POST  
**URL:** `http://localhost:8000/api/courses/`  
**Description:** Create a new course  

**Request Body:**
```json
{
  "code": "NCLEX",
  "name": "National Council Licensure Examination",
  "description": "Standardized exam that each state board of nursing uses to determine whether a candidate is prepared for entry-level nursing practice.",
  "duration": "3"
}
```

**Example Response:**
```json
{
  "message": "Course created successfully",
  "data": {
    "id": 1,
    "code": "NCLEX",
    "name": "National Council Licensure Examination",
    "description": "Standardized exam that each state board of nursing uses to determine whether a candidate is prepared for entry-level nursing practice.",
    "duration": "3",
    "created_at": "2024-01-01T00:00:00.000Z",
    "updated_at": "2024-01-01T00:00:00.000Z"
  }
}
```

### 3. GET /api/courses/{id}/ - Get Single Course
**Method:** GET  
**URL:** `http://localhost:8000/api/courses/1/`  
**Description:** Retrieve a specific course by ID  

**Example Response:**
```json
{
  "id": 1,
  "code": "NCLEX",
  "name": "National Council Licensure Examination",
  "description": "Standardized exam that each state board of nursing uses to determine whether a candidate is prepared for entry-level nursing practice.",
  "duration": "3",
  "created_at": "2024-01-01T00:00:00.000Z",
  "updated_at": "2024-01-01T00:00:00.000Z"
}
```

### 4. PUT /api/courses/{id}/ - Update Course (Full Update)
**Method:** PUT  
**URL:** `http://localhost:8000/api/courses/1/`  
**Description:** Update all fields of a specific course  

**Request Body:**
```json
{
  "code": "NCLEX-RN",
  "name": "National Council Licensure Examination for Registered Nurses",
  "description": "Updated description for the standardized exam that each state board of nursing uses to determine whether a candidate is prepared for entry-level nursing practice.",
  "duration": "4"
}
```

**Example Response:**
```json
{
  "message": "Course updated successfully",
  "data": {
    "id": 1,
    "code": "NCLEX-RN",
    "name": "National Council Licensure Examination for Registered Nurses",
    "description": "Updated description for the standardized exam that each state board of nursing uses to determine whether a candidate is prepared for entry-level nursing practice.",
    "duration": "4",
    "created_at": "2024-01-01T00:00:00.000Z",
    "updated_at": "2024-01-01T12:00:00.000Z"
  }
}
```

### 5. PATCH /api/courses/{id}/ - Update Course (Partial Update)
**Method:** PATCH  
**URL:** `http://localhost:8000/api/courses/1/`  
**Description:** Update specific fields of a course  

**Request Body:**
```json
{
  "duration": "5"
}
```

**Example Response:**
```json
{
  "message": "Course updated successfully",
  "data": {
    "id": 1,
    "code": "NCLEX",
    "name": "National Council Licensure Examination",
    "description": "Standardized exam that each state board of nursing uses to determine whether a candidate is prepared for entry-level nursing practice.",
    "duration": "5",
    "created_at": "2024-01-01T00:00:00.000Z",
    "updated_at": "2024-01-01T12:00:00.000Z"
  }
}
```

### 6. DELETE /api/courses/{id}/ - Delete Course
**Method:** DELETE  
**URL:** `http://localhost:8000/api/courses/1/`  
**Description:** Delete a specific course  

**Example Response:**
```json
{
  "message": "Course deleted successfully"
}
```

## Test Data for Postman

### Test Course 1 - NCLEX
```json
{
  "code": "NCLEX",
  "name": "National Council Licensure Examination",
  "description": "Standardized exam that each state board of nursing uses to determine whether a candidate is prepared for entry-level nursing practice.",
  "duration": "3"
}
```

### Test Course 2 - CGFNS
```json
{
  "code": "CGFNS",
  "name": "Commission on Graduates of Foreign Nursing Schools",
  "description": "Certification program for foreign-educated nurses who want to practice in the United States.",
  "duration": "2"
}
```

### Test Course 3 - TEAS
```json
{
  "code": "TEAS",
  "name": "Test of Essential Academic Skills",
  "description": "Standardized test used by nursing schools to evaluate the academic readiness of applicants for nursing programs.",
  "duration": "4"
}
```

### Test Course 4 - HESI
```json
{
  "code": "HESI",
  "name": "Health Education Systems Incorporated",
  "description": "Comprehensive review and testing system for nursing students and professionals.",
  "duration": "2"
}
```

### Test Course 5 - NACE
```json
{
  "code": "NACE",
  "name": "Nurse Aide Competency Evaluation",
  "description": "Test required for certification as a Certified Nursing Assistant (CNA).",
  "duration": "1"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "code": ["Course with this code already exists."]
}
```


### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error."
}
```

## Postman Collection Setup

1. **Create Environment Variables:**
   - `base_url`: `http://localhost:8000`

2. **No Authorization Required:**
   - All endpoints are publicly accessible

3. **Create Tests:**
   Add the following test script to verify responses:
   ```javascript
   pm.test("Status code is 200", function () {
       pm.response.to.have.status(200);
   });
   
   pm.test("Response has required fields", function () {
       const responseJson = pm.response.json();
       pm.expect(responseJson).to.have.property("id");
       pm.expect(responseJson).to.have.property("code");
       pm.expect(responseJson).to.have.property("name");
       pm.expect(responseJson).to.have.property("description");
       pm.expect(responseJson).to.have.property("duration");
   });
   ```

## Database Migration

Before testing, make sure to run the database migrations:

```bash
python manage.py makemigrations courses
python manage.py migrate
```

## Notes

- All timestamps are in ISO 8601 format
- The `code` field must be unique across all courses
- No authentication required - all endpoints are publicly accessible
- The API supports pagination with a default page size of 20 items
- Search functionality works across code, name, and description fields
- Filtering and ordering are supported for better data retrieval