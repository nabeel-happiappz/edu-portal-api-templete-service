# Departments API - Complete Postman Testing Guide

## Setup Instructions

### 1. Import to Postman
1. Open Postman
2. Create a new collection named "Departments API"
3. Add the following environment variables:
   - `base_url`: `http://localhost:8000`
   - `api_prefix`: `/api/departments`

### 2. Headers Configuration
For all requests, add these headers:
```
Content-Type: application/json
Accept: application/json
```

## Complete Test Scenarios

### Test 1: Create Department - General
**Method:** POST  
**URL:** `{{base_url}}{{api_prefix}}/`  
**Body (raw JSON):**
```json
{
  "name": "General",
  "description": "General medical department covering a wide range of medical conditions"
}
```

**Expected Response (201 Created):**
```json
{
  "message": "Department created successfully",
  "data": {
    "id": 1,
    "name": "General",
    "description": "General medical department covering a wide range of medical conditions",
    "created_at": "2025-07-08T05:33:48.000Z",
    "updated_at": "2025-07-08T05:33:48.000Z"
  }
}
```

**Tests Tab Script:**
```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Response has correct structure", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('message');
    pm.expect(jsonData).to.have.property('data');
    pm.expect(jsonData.data).to.have.property('id');
    pm.expect(jsonData.data).to.have.property('created_at');
    pm.expect(jsonData.data).to.have.property('updated_at');
});

// Save department ID for future tests
if (pm.response.code === 201) {
    pm.environment.set("department_id", pm.response.json().data.id);
}
```

### Test 2: Create Department - Cardiology
**Method:** POST  
**URL:** `{{base_url}}{{api_prefix}}/`  
**Body (raw JSON):**
```json
{
  "name": "Cardiology",
  "description": "Department specializing in diagnosing and treating heart and cardiovascular system conditions"
}
```

### Test 3: Create Department - Neurology
**Method:** POST  
**URL:** `{{base_url}}{{api_prefix}}/`  
**Body (raw JSON):**
```json
{
  "name": "Neurology",
  "description": "Department focusing on disorders of the nervous system including brain, spinal cord, and nerves"
}
```

### Test 4: Create Department - Pediatrics
**Method:** POST  
**URL:** `{{base_url}}{{api_prefix}}/`  
**Body (raw JSON):**
```json
{
  "name": "Pediatrics",
  "description": "Medical department dedicated to the health and medical care of infants, children, and adolescents"
}
```

### Test 5: Create Department - Emergency Medicine
**Method:** POST  
**URL:** `{{base_url}}{{api_prefix}}/`  
**Body (raw JSON):**
```json
{
  "name": "Emergency Medicine",
  "description": "Department providing immediate medical care for acute illnesses and injuries requiring urgent attention"
}
```

### Test 6: List All Departments
**Method:** GET  
**URL:** `{{base_url}}{{api_prefix}}/`  

**Expected Response (200 OK):**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 5,
      "name": "Emergency Medicine",
      "description": "Department providing immediate medical care for acute illnesses and injuries requiring urgent attention",
      "created_at": "2025-07-08T05:35:00.000Z",
      "updated_at": "2025-07-08T05:35:00.000Z"
    },
    // ... other departments
  ]
}
```

**Tests Tab Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response is paginated", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('count');
    pm.expect(jsonData).to.have.property('results');
    pm.expect(jsonData.results).to.be.an('array');
});
```

### Test 7: Get Single Department
**Method:** GET  
**URL:** `{{base_url}}{{api_prefix}}/{{department_id}}/`  

**Tests Tab Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response contains department details", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('id');
    pm.expect(jsonData).to.have.property('name');
    pm.expect(jsonData).to.have.property('description');
});
```

### Test 8: Update Department (Full Update)
**Method:** PUT  
**URL:** `{{base_url}}{{api_prefix}}/{{department_id}}/`  
**Body (raw JSON):**
```json
{
  "name": "General Medicine",
  "description": "Updated: Comprehensive general medical department providing primary healthcare services"
}
```

**Tests Tab Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Department is updated", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.data.name).to.eql("General Medicine");
    pm.expect(jsonData.data.description).to.include("Updated:");
});
```

### Test 9: Partial Update Department
**Method:** PATCH  
**URL:** `{{base_url}}{{api_prefix}}/{{department_id}}/`  
**Body (raw JSON):**
```json
{
  "description": "Partially updated: General medical department with enhanced services"
}
```

### Test 10: Search Departments
**Method:** GET  
**URL:** `{{base_url}}{{api_prefix}}/?search=neuro`  

**Tests Tab Script:**
```javascript
pm.test("Search returns filtered results", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.results.length).to.be.at.least(1);
    
    // Check if results contain 'neuro' in name or description
    jsonData.results.forEach(function(dept) {
        var nameMatch = dept.name.toLowerCase().includes('neuro');
        var descMatch = dept.description.toLowerCase().includes('neuro');
        pm.expect(nameMatch || descMatch).to.be.true;
    });
});
```

### Test 11: Filter by Name
**Method:** GET  
**URL:** `{{base_url}}{{api_prefix}}/?name=Cardiology`  

### Test 12: Sort Departments
**Method:** GET  
**URL:** `{{base_url}}{{api_prefix}}/?ordering=name`  

**Tests Tab Script:**
```javascript
pm.test("Results are sorted by name", function () {
    var jsonData = pm.response.json();
    var names = jsonData.results.map(d => d.name);
    var sortedNames = [...names].sort();
    pm.expect(names).to.eql(sortedNames);
});
```

### Test 13: Duplicate Name Validation
**Method:** POST  
**URL:** `{{base_url}}{{api_prefix}}/`  
**Body (raw JSON):**
```json
{
  "name": "Cardiology",
  "description": "Attempting to create duplicate department"
}
```

**Expected Response (400 Bad Request):**
```json
{
  "name": ["Department with this name already exists."]
}
```

**Tests Tab Script:**
```javascript
pm.test("Duplicate name returns 400", function () {
    pm.response.to.have.status(400);
});

pm.test("Error message is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.name[0]).to.include("already exists");
});
```

### Test 14: Delete Department
**Method:** DELETE  
**URL:** `{{base_url}}{{api_prefix}}/{{department_id}}/`  

**Expected Response (204 No Content)**

**Tests Tab Script:**
```javascript
pm.test("Status code is 204", function () {
    pm.response.to.have.status(204);
});

// Clean up environment variable
pm.environment.unset("department_id");
```

### Test 15: Verify Deletion
**Method:** GET  
**URL:** `{{base_url}}{{api_prefix}}/{{department_id}}/`  

**Expected Response (404 Not Found)**

## Advanced Test Scenarios

### Pagination Test
**Method:** GET  
**URL:** `{{base_url}}{{api_prefix}}/?page=1&page_size=2`  

### Invalid Data Test
**Method:** POST  
**URL:** `{{base_url}}{{api_prefix}}/`  
**Body (raw JSON):**
```json
{
  "name": "",
  "description": "Test with empty name"
}
```

## Postman Collection Export

After creating all tests, export your collection:
1. Right-click on "Departments API" collection
2. Select "Export"
3. Choose "Collection v2.1"
4. Save as "Departments_API_Collection.json"

## Running Tests

### Run All Tests
1. Click on the collection name
2. Click "Run" button
3. Select all requests
4. Click "Run Departments API"

### Expected Results
- All tests should pass
- Total run time should be under 5 seconds
- No failed assertions

## Environment Variables Summary
- `base_url`: http://localhost:8000
- `api_prefix`: /api/departments
- `department_id`: (dynamically set during tests)

## Common Issues and Solutions

1. **Connection Refused**: Ensure Django server is running on port 8000
2. **CSRF Token Error**: The API should be configured to allow any access
3. **JSON Parse Error**: Check Content-Type header is set to application/json
