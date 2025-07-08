# Departments API Documentation

## Overview
This document provides comprehensive information about the Departments API endpoints, including URLs, request/response formats, and test data for Postman testing.

## Base URL
```
http://localhost:8000/api/departments/
```

## Authentication
No authentication required - all endpoints are publicly accessible.

## API Endpoints

### 1. GET /api/departments/ - List All Departments
**Method:** GET  
**URL:** `http://localhost:8000/api/departments/`  
**Description:** Retrieve a paginated list of all departments  

**Example Request:**
```
GET http://localhost:8000/api/departments/
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
      "name": "General",
      "description": "General medical department covering a wide range of medical conditions",
      "created_at": "2024-01-01T00:00:00.000Z",
      "updated_at": "2024-01-01T00:00:00.000Z"
    }
  ]
}
```

### 2. POST /api/departments/ - Create New Department
**Method:** POST  
**URL:** `http://localhost:8000/api/departments/`  
**Description:** Create a new department  

**Request Body:**
```json
{
  "name": "General",
  "description": "General medical department covering a wide range of medical conditions"
}
```

**Example Response:**
```json
{
  "message": "Department created successfully",
  "data": {
    "id": 1,
    "name": "General",
    "description": "General medical department covering a wide range of medical conditions",
    "created_at": "2024-01-01T00:00:00.000Z",
    "updated_at": "2024-01-01T00:00:00.000Z"
  }
}
```

### 3. GET /api/departments/{id}/ - Get Single Department
**Method:** GET  
**URL:** `http://localhost:8000/api/departments/1/`  
**Description:** Retrieve a specific department by ID  

**Example Response:**
```json
{
  "id": 1,
  "name": "General",
  "description": "General medical department covering a wide range of medical conditions",
  "created_at": "2024-01-01T00:00:00.000Z",
  "updated_at": "2024-01-01T00:00:00.000Z"
}
```

### 4. PUT /api/departments/{id}/ - Update Department (Full Update)
**Method:** PUT  
**URL:** `http://localhost:8000/api/departments/1/`  
**Description:** Update all fields of a specific department  

**Request Body:**
```json
{
  "name": "General Updated",
  "description": "Updated description for the general medical department."
}
```

**Example Response:**
```json
{
  "message": "Department updated successfully",
  "data": {
    "id": 1,
    "name": "General Updated",
    "description": "Updated description for the general medical department.",
    "created_at": "2024-01-01T00:00:00.000Z",
    "updated_at": "2024-01-01T12:00:00.000Z"
  }
}
```

### 5. PATCH /api/departments/{id}/ - Update Department (Partial Update)
**Method:** PATCH  
**URL:** `http://localhost:8000/api/departments/1/`  
**Description:** Update specific fields of a department  

**Request Body:**
```json
{
  "description": "Partially updated description for the general department."
}
```

**Example Response:**
```json
{
  "message": "Department updated successfully",
  "data": {
    "id": 1,
    "name": "General",
    "description": "Partially updated description for the general department.",
    "created_at": "2024-01-01T00:00:00.000Z",
    "updated_at": "2024-01-01T12:00:00.000Z"
  }
}
```

### 6. DELETE /api/departments/{id}/ - Delete Department
**Method:** DELETE  
**URL:** `http://localhost:8000/api/departments/1/`  
**Description:** Delete a specific department  

**Example Response:**
```json
{
  "message": "Department deleted successfully"
}
```

## Test Data for Postman

### Test Department 1 - General
```json
{
  "name": "General",
  "description": "General medical department covering a wide range of medical conditions"
}
```

### Test Department 2 - Cardiology
```json
{
  "name": "Cardiology",
  "description": "Department specializing in heart-related medical conditions."
}
```

### Test Department 3 - Neurology
```json
{
  "name": "Neurology",
  "description": "Department focusing on neurological disorders and conditions."
}
```

