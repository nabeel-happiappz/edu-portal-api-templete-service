# UPDATE PASSWORD POSTMAN

## 🚀 Password Update APIs Testing Guide

### Server Information
```
Base URL: http://127.0.0.1:8000
```

---

## 📋 API Endpoints

### **1. Update Password with Old Password and Username**
- **URL:** `http://127.0.0.1:8000/api/auth/update-password-with-old/`
- **Method:** `POST`
- **Authentication:** None Required
- **Headers:**
  ```json
  {
    "Content-Type": "application/json"
  }
  ```

### **2. Update Password with Only Username**
- **URL:** `http://127.0.0.1:8000/api/auth/update-password/`
- **Method:** `POST`
- **Authentication:** None Required
- **Headers:**
  ```json
  {
    "Content-Type": "application/json"
  }
  ```

---

## 🧪 Test Data

### **Test Case 1: Update Password with Old Password Verification**

**URL:** `http://127.0.0.1:8000/api/auth/update-password-with-old/`
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
  "username": "testuser",
  "old_password": "aSecurePassword123!",
  "new_password": "newSecurePassword456!"
}
```

**Expected Response (200 OK):**
```json
{
  "detail": "Password updated successfully."
}
```

---

### **Test Case 2: Update Password with Username Only**

**URL:** `http://127.0.0.1:8000/api/auth/update-password/`
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
  "username": "testuser",
  "new_password": "anotherNewPassword789!"
}
```

**Expected Response (200 OK):**
```json
{
  "detail": "Password updated successfully."
}
```

---

## 🔄 Complete Test Workflow

### **Step 1: Create Test User**
```json
POST http://127.0.0.1:8000/api/auth/register/
Content-Type: application/json

{
  "email": "testuser@example.com",
  "username": "testuser",
  "password": "initialPassword123!",
  "first_name": "Test",
  "last_name": "User",
  "role": "student"
}
```

### **Step 2: Update Password with Old Password**
```json
POST http://127.0.0.1:8000/api/auth/update-password-with-old/
Content-Type: application/json

{
  "username": "testuser",
  "old_password": "initialPassword123!",
  "new_password": "updatedPassword456!"
}
```

### **Step 3: Verify Login with New Password (using email)**
```json
POST http://127.0.0.1:8000/api/auth/login/
Content-Type: application/json

{
  "username_or_email": "testuser@example.com",
  "password": "updatedPassword456!"
}
```

### **Step 4: Update Password with Username Only**
```json
POST http://127.0.0.1:8000/api/auth/update-password/
Content-Type: application/json

{
  "username": "testuser",
  "new_password": "finalPassword789!"
}
```

### **Step 5: Verify Login with Final Password**
```json
POST http://127.0.0.1:8000/api/auth/login/
Content-Type: application/json

{
  "email": "testuser@example.com",
  "password": "finalPassword789!"
}
```

---

## ❌ Error Test Cases

### **Test Case 3: Non-existent Username**

**URL:** `http://127.0.0.1:8000/api/auth/update-password/`
**Method:** `POST`

**Body (raw JSON):**
```json
{
  "username": "nonexistentuser",
  "new_password": "somepassword123!"
}
```

**Expected Response (404 Not Found):**
```json
{
  "detail": "User not found."
}
```

---

### **Test Case 4: Wrong Old Password**

**URL:** `http://127.0.0.1:8000/api/auth/update-password-with-old/`
**Method:** `POST`

**Body (raw JSON):**
```json
{
  "username": "testuser",
  "old_password": "wrongpassword",
  "new_password": "newpassword123!"
}
```

**Expected Response (400 Bad Request):**
```json
{
  "detail": "Incorrect old password."
}
```

---

### **Test Case 5: Missing Required Fields**

**URL:** `http://127.0.0.1:8000/api/auth/update-password-with-old/`
**Method:** `POST`

**Body (raw JSON):**
```json
{
  "username": "testuser",
  "new_password": "newpassword123!"
}
```

**Expected Response (400 Bad Request):**
```json
{
  "detail": "Old password is required."
}
```

---

### **Test Case 6: Missing Username**

**URL:** `http://127.0.0.1:8000/api/auth/update-password/`
**Method:** `POST`

**Body (raw JSON):**
```json
{
  "new_password": "newpassword123!"
}
```

**Expected Response (400 Bad Request):**
```json
{
  "detail": "Username is required."
}
```

---

## 📊 Postman Collection JSON

Copy and import this into Postman:

```json
{
  "info": {
    "name": "Password Update APIs",
    "description": "Test collection for password update endpoints",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Create Test User",
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
          "raw": "{\n  \"email\": \"testuser@example.com\",\n  \"username\": \"testuser\",\n  \"password\": \"initialPassword123!\",\n  \"first_name\": \"Test\",\n  \"last_name\": \"User\",\n  \"role\": \"student\"\n}"
        },
        "url": {
          "raw": "http://127.0.0.1:8000/api/auth/register/",
          "protocol": "http",
          "host": ["127", "0", "0", "1"],
          "port": "8000",
          "path": ["api", "auth", "register", ""]
        }
      }
    },
    {
      "name": "Update Password with Old Password",
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
          "raw": "{\n  \"username\": \"testuser\",\n  \"old_password\": \"initialPassword123!\",\n  \"new_password\": \"updatedPassword456!\"\n}"
        },
        "url": {
          "raw": "http://127.0.0.1:8000/api/auth/update-password-with-old/",
          "protocol": "http",
          "host": ["127", "0", "0", "1"],
          "port": "8000",
          "path": ["api", "auth", "update-password-with-old", ""]
        }
      }
    },
    {
      "name": "Update Password with Username Only",
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
          "raw": "{\n  \"username\": \"testuser\",\n  \"new_password\": \"finalPassword789!\"\n}"
        },
        "url": {
          "raw": "http://127.0.0.1:8000/api/auth/update-password/",
          "protocol": "http",
          "host": ["127", "0", "0", "1"],
          "port": "8000",
          "path": ["api", "auth", "update-password", ""]
        }
      }
    },
    {
      "name": "Login with Updated Password",
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
          "raw": "{\n  \"email\": \"testuser@example.com\",\n  \"password\": \"finalPassword789!\"\n}"
        },
        "url": {
          "raw": "http://127.0.0.1:8000/api/auth/login/",
          "protocol": "http",
          "host": ["127", "0", "0", "1"],
          "port": "8000",
          "path": ["api", "auth", "login", ""]
        }
      }
    },
    {
      "name": "Error Test - Non-existent User",
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
          "raw": "{\n  \"username\": \"nonexistentuser\",\n  \"new_password\": \"somepassword123!\"\n}"
        },
        "url": {
          "raw": "http://127.0.0.1:8000/api/auth/update-password/",
          "protocol": "http",
          "host": ["127", "0", "0", "1"],
          "port": "8000",
          "path": ["api", "auth", "update-password", ""]
        }
      }
    },
    {
      "name": "Error Test - Wrong Old Password",
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
          "raw": "{\n  \"username\": \"testuser\",\n  \"old_password\": \"wrongpassword\",\n  \"new_password\": \"newpassword123!\"\n}"
        },
        "url": {
          "raw": "http://127.0.0.1:8000/api/auth/update-password-with-old/",
          "protocol": "http",
          "host": ["127", "0", "0", "1"],
          "port": "8000",
          "path": ["api", "auth", "update-password-with-old", ""]
        }
      }
    }
  ]
}
```

---

## 🎯 Quick Test Commands (cURL)

### Update Password with Old Password:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/update-password-with-old/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "old_password": "initialPassword123!",
    "new_password": "updatedPassword456!"
  }'
```

### Update Password with Username Only:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/update-password/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "new_password": "finalPassword789!"
  }'
```

---

## 🔧 Testing Steps

1. **Start Django Server:**
   ```bash
   python manage.py runserver
   ```

2. **Open Postman and import the collection above**

3. **Run tests in sequence:**
   - Create Test User
   - Update Password with Old Password
   - Login with Updated Password
   - Update Password with Username Only
   - Login with Final Password

4. **Test error cases:**
   - Non-existent User
   - Wrong Old Password

---

## 📝 Notes

- **No Authentication Required:** Both password update endpoints can be accessed without any login tokens
- **Security Note:** The "username only" endpoint is less secure as it doesn't verify the old password
- **Password Encryption:** All passwords are properly hashed using Django's built-in security
- **Error Handling:** Comprehensive error responses for various failure scenarios

Happy testing! 🚀
