# Packages API Documentation

## Overview
This API provides endpoints to manage packages for the education portal. All endpoints are open (no authentication required).

## Base URL
```
http://localhost:8000/api
```

## Endpoints

### 1. GET /api/packages/
**Description:** List all active packages

**Method:** GET

**URL:** `http://localhost:8000/api/packages/`

**Headers:**
```
Content-Type: application/json
```

**Response:**
```json
{
    "status": "success",
    "data": [
        {
            "id": 1,
            "name": "Basic Package",
            "description": "Access to 500 practice questions",
            "price": "500.00",
            "currency": "INR",
            "features": {
                "questionCount": 500,
                "validityDays": 180,
                "allowedAttempts": "unlimited",
                "includesExplanations": true,
                "includesAnalytics": false
            },
            "is_active": true,
            "tags": ["beginner", "popular"],
            "created_at": "2024-07-04T12:27:00Z",
            "updated_at": "2024-07-04T12:27:00Z"
        }
    ],
    "count": 1
}
```

---

### 2. GET /api/packages/:id
**Description:** Get package details by ID

**Method:** GET

**URL:** `http://localhost:8000/api/packages/1/`

**Headers:**
```
Content-Type: application/json
```

**Response:**
```json
{
    "status": "success",
    "data": {
        "id": 1,
        "name": "Basic Package",
        "description": "Access to 500 practice questions",
        "price": "500.00",
        "currency": "INR",
        "features": {
            "questionCount": 500,
            "validityDays": 180,
            "allowedAttempts": "unlimited",
            "includesExplanations": true,
            "includesAnalytics": false
        },
        "is_active": true,
        "tags": ["beginner", "popular"],
        "created_at": "2024-07-04T12:27:00Z",
        "updated_at": "2024-07-04T12:27:00Z"
    }
}
```

---

### 3. POST /api/packages/
**Description:** Create a new package

**Method:** POST

**URL:** `http://localhost:8000/api/packages/`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "name": "Premium Package",
    "description": "Access to 1000 practice questions with detailed analytics",
    "price": 1200,
    "currency": "INR",
    "question_count": 1000,
    "validity_days": 365,
    "allowed_attempts": "unlimited",
    "includes_explanations": true,
    "includes_analytics": true,
    "is_active": true,
    "tags": ["advanced", "premium"]
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Package created successfully",
    "data": {
        "id": 2,
        "name": "Premium Package",
        "description": "Access to 1000 practice questions with detailed analytics",
        "price": "1200.00",
        "currency": "INR",
        "features": {
            "questionCount": 1000,
            "validityDays": 365,
            "allowedAttempts": "unlimited",
            "includesExplanations": true,
            "includesAnalytics": true
        },
        "is_active": true,
        "tags": ["advanced", "premium"],
        "created_at": "2024-07-04T12:30:00Z",
        "updated_at": "2024-07-04T12:30:00Z"
    }
}
```

---

### 4. PUT /api/packages/:id
**Description:** Update an existing package

**Method:** PUT

**URL:** `http://localhost:8000/api/packages/1/`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "name": "Basic Package - Updated",
    "description": "Access to 600 practice questions with updated content",
    "price": 600,
    "question_count": 600,
    "validity_days": 200,
    "tags": ["beginner", "popular", "updated"]
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Package updated successfully",
    "data": {
        "id": 1,
        "name": "Basic Package - Updated",
        "description": "Access to 600 practice questions with updated content",
        "price": "600.00",
        "currency": "INR",
        "features": {
            "questionCount": 600,
            "validityDays": 200,
            "allowedAttempts": "unlimited",
            "includesExplanations": true,
            "includesAnalytics": false
        },
        "is_active": true,
        "tags": ["beginner", "popular", "updated"],
        "created_at": "2024-07-04T12:27:00Z",
        "updated_at": "2024-07-04T12:35:00Z"
    }
}
```

---

### 5. DELETE /api/packages/:id
**Description:** Delete a package

**Method:** DELETE

**URL:** `http://localhost:8000/api/packages/1/`

**Headers:**
```
Content-Type: application/json
```

**Response:**
```json
{
    "status": "success",
    "message": "Package deleted successfully"
}
```

---

## Test Data for Postman

### Test Package 1 (Basic)
```json
{
    "name": "Basic Package",
    "description": "Access to 500 practice questions",
    "price": 500,
    "currency": "INR",
    "question_count": 500,
    "validity_days": 180,
    "allowed_attempts": "unlimited",
    "includes_explanations": true,
    "includes_analytics": false,
    "is_active": true,
    "tags": ["beginner", "popular"]
}
```

### Test Package 2 (Premium)
```json
{
    "name": "Premium Package",
    "description": "Access to 1000 practice questions with detailed analytics",
    "price": 1200,
    "currency": "INR",
    "question_count": 1000,
    "validity_days": 365,
    "allowed_attempts": "unlimited",
    "includes_explanations": true,
    "includes_analytics": true,
    "is_active": true,
    "tags": ["advanced", "premium"]
}
```

### Test Package 3 (Professional)
```json
{
    "name": "Professional Package",
    "description": "Access to 2000 practice questions with AI-powered recommendations",
    "price": 2000,
    "currency": "INR",
    "question_count": 2000,
    "validity_days": 730,
    "allowed_attempts": "unlimited",
    "includes_explanations": true,
    "includes_analytics": true,
    "is_active": true,
    "tags": ["professional", "ai-powered", "comprehensive"]
}
```

### Test Package 4 (Student)
```json
{
    "name": "Student Package",
    "description": "Budget-friendly access to 250 practice questions",
    "price": 250,
    "currency": "INR",
    "question_count": 250,
    "validity_days": 90,
    "allowed_attempts": "unlimited",
    "includes_explanations": false,
    "includes_analytics": false,
    "is_active": true,
    "tags": ["student", "budget", "basic"]
}
```

### Test Package 5 (Limited Attempts)
```json
{
    "name": "Trial Package",
    "description": "Limited trial access to 100 practice questions",
    "price": 100,
    "currency": "INR",
    "question_count": 100,
    "validity_days": 30,
    "allowed_attempts": "5",
    "includes_explanations": false,
    "includes_analytics": false,
    "is_active": true,
    "tags": ["trial", "limited"]
}
```

## Error Responses

### 400 Bad Request
```json
{
    "status": "error",
    "message": "Validation failed",
    "errors": {
        "name": ["This field is required."],
        "price": ["A valid number is required."]
    }
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

## Postman Collection Setup

1. Create a new collection named "Packages API"
2. Set the base URL as an environment variable: `{{base_url}}` = `http://localhost:8000/api`
3. Create the following requests:

### Request 1: List Packages
- **Method:** GET
- **URL:** `{{base_url}}/packages/`
- **Headers:** Content-Type: application/json

### Request 2: Get Package
- **Method:** GET
- **URL:** `{{base_url}}/packages/1/`
- **Headers:** Content-Type: application/json

### Request 3: Create Package
- **Method:** POST
- **URL:** `{{base_url}}/packages/`
- **Headers:** Content-Type: application/json
- **Body:** Use any of the test package data above

### Request 4: Update Package
- **Method:** PUT
- **URL:** `{{base_url}}/packages/1/`
- **Headers:** Content-Type: application/json
- **Body:** Partial update data

### Request 5: Delete Package
- **Method:** DELETE
- **URL:** `{{base_url}}/packages/1/`
- **Headers:** Content-Type: application/json

## Notes
- All endpoints are open and do not require authentication
- The API returns JSON responses with a consistent structure
- Package IDs are auto-generated integers
- Tags field accepts an array of strings
- Price is stored as decimal with 2 decimal places
- Dates are in ISO 8601 format (UTC)
- The `features` field in responses is computed from individual feature fields
