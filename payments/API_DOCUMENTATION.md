# Payments API Documentation

## Overview
This document provides comprehensive information about the Payments API endpoints, including URLs, request/response formats, and test data for Postman testing.

## Base URL
```
http://localhost:8000/api/payments/
```

## Authentication
No authentication required - all endpoints are publicly accessible.

## API Endpoints

### 1. GET /api/payments/ - List All Payments
**Method:** GET  
**URL:** `http://localhost:8000/api/payments/`  
**Description:** Retrieve a paginated list of all payments  

**Query Parameters:**
- `page` - Page number (optional)
- `status` - Filter by payment status (optional)
- `search` - Search in studentName, course, or status (optional)
- `ordering` - Sort by field (options: createdAt, updatedAt, date, amount, -createdAt, -updatedAt, -date, -amount)

**Example Request:**
```
GET http://localhost:8000/api/payments/?search=John&ordering=-createdAt
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
      "studentName": "John Doe",
      "course": "NCLEX",
      "amount": 1500.00,
      "date": "2024-01-15",
      "status": "Paid",
      "createdAt": "2024-01-01T00:00:00.000Z",
      "updatedAt": "2024-01-01T00:00:00.000Z"
    }
  ]
}
```

### 2. POST /api/payments/ - Create New Payment
**Method:** POST  
**URL:** `http://localhost:8000/api/payments/`  
**Description:** Create a new payment  

**Request Body:**
```json
{
  "studentName": "John Doe",
  "course": "NCLEX",
  "amount": 1500.00,
  "date": "2024-01-15",
  "status": "Paid"
}
```

**Example Response:**
```json
{
  "message": "Payment created successfully",
  "data": {
    "id": 1,
    "studentName": "John Doe",
    "course": "NCLEX",
    "amount": 1500.00,
    "date": "2024-01-15",
    "status": "Paid",
    "createdAt": "2024-01-01T00:00:00.000Z",
    "updatedAt": "2024-01-01T00:00:00.000Z"
  }
}
```

### 3. GET /api/payments/{id}/ - Get Single Payment
**Method:** GET  
**URL:** `http://localhost:8000/api/payments/1/`  
**Description:** Retrieve a specific payment by ID  

**Example Response:**
```json
{
  "id": 1,
  "studentName": "John Doe",
  "course": "NCLEX",
  "amount": 1500.00,
  "date": "2024-01-15",
  "status": "Paid",
  "createdAt": "2024-01-01T00:00:00.000Z",
  "updatedAt": "2024-01-01T00:00:00.000Z"
}
```

### 4. PUT /api/payments/{id}/ - Update Payment (Full Update)
**Method:** PUT  
**URL:** `http://localhost:8000/api/payments/1/`  
**Description:** Update all fields of a specific payment  

**Request Body:**
```json
{
  "studentName": "John Doe",
  "course": "NCLEX-RN",
  "amount": 1600.00,
  "date": "2024-02-15",
  "status": "Pending"
}
```

**Example Response:**
```json
{
  "message": "Payment updated successfully",
  "data": {
    "id": 1,
    "studentName": "John Doe",
    "course": "NCLEX-RN",
    "amount": 1600.00,
    "date": "2024-02-15",
    "status": "Pending",
    "createdAt": "2024-01-01T00:00:00.000Z",
    "updatedAt": "2024-01-01T12:00:00.000Z"
  }
}
```

### 5. PATCH /api/payments/{id}/ - Update Payment (Partial Update)
**Method:** PATCH  
**URL:** `http://localhost:8000/api/payments/1/`  
**Description:** Update specific fields of a payment  

**Request Body:**
```json
{
  "status": "Completed"
}
```

**Example Response:**
```json
{
  "message": "Payment updated successfully",
  "data": {
    "id": 1,
    "studentName": "John Doe",
    "course": "NCLEX-RN",
    "amount": 1600.00,
    "date": "2024-02-15",
    "status": "Completed",
    "createdAt": "2024-01-01T00:00:00.000Z",
    "updatedAt": "2024-01-01T12:00:00.000Z"
  }
}
```

### 6. DELETE /api/payments/{id}/ - Delete Payment
**Method:** DELETE  
**URL:** `http://localhost:8000/api/payments/1/`  
**Description:** Delete a specific payment  

**Example Response:**
```json
{
  "message": "Payment deleted successfully"
}
```

## Test Data for Postman

### Test Payment 1 - Full Payment
```json
{
  "studentName": "John Doe",
  "course": "NCLEX",
  "amount": 1500.00,
  "date": "2024-01-15",
  "status": "Paid"
}
```

### Test Payment 2 - Pending Payment
```json
{
  "studentName": "Jane Smith",
  "course": "CGFNS",
  "amount": 1200.00,
  "date": "2024-02-01",
  "status": "Pending"
}
```

### Test Payment 3 - Overdue Payment
```json
{
  "studentName": "Robert Johnson",
  "course": "TEAS",
  "amount": 800.00,
  "date": "2023-12-15",
  "status": "Overdue"
}
```

### Test Payment 4 - Refunded Payment
```json
{
  "studentName": "Maria Garcia",
  "course": "HESI",
  "amount": 1000.00,
  "date": "2024-01-20",
  "status": "Refunded"
}
```

### Test Payment 5 - Partial Payment
```json
{
  "studentName": "David Williams",
  "course": "NCLEX-RN",
  "amount": 2000.00,
  "date": "2024-03-01",
  "status": "Partial"
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
       pm.expect(responseJson).to.have.property("studentName");
       pm.expect(responseJson).to.have.property("course");
       pm.expect(responseJson).to.have.property("amount");
       pm.expect(responseJson).to.have.property("date");
       pm.expect(responseJson).to.have.property("status");
   });
   ```

## Database Migration

Before testing, make sure to run the database migrations:

```bash
python manage.py makemigrations payments
python manage.py migrate
```

## Notes

- All timestamps are in ISO 8601 format
- No authentication required - all endpoints are publicly accessible
- The API supports pagination with a default page size of 20 items
- Search functionality works across studentName, course, and status fields
- Filtering and ordering are supported for better data retrieval

