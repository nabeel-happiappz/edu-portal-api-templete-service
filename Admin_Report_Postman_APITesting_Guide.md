# Postman API Testing Guide for Admin Report Endpoint

This guide will help you test the admin report endpoint using Postman.

### Prerequisites
- Make sure the Django server is running at `http://127.0.0.1:8000`.
- Install [Postman](https://www.postman.com/downloads/).

### Testing the Admin Report Endpoint

1. **Open Postman**
   - Launch the Postman application on your computer.

2. **Create a New Request**
   - Click the `+` button or `New` to create a new request.

3. **Set Request Type and URL**
   - Change the request type to `GET`.
   - Enter the request URL: `http://127.0.0.1:8000/api/reports/admin_report/`

4. **Send the Request**
   - Click `Send` to execute the request.

5. **Review the Response**
   - The response body should contain the JSON data with statistics, similar to:
     ```json
     {
         "totalCourses": 6,
         "totalStudents": 4,
         "totalUsers": 7,
         "totalRevenue": 6500.0,
         "courseEnrollmentReport": [
             {
                 "courseName": "National Council Licensure Examination",
                 "courseCode": "NCLEX",
                 "students": 2,
                 "revenue": 1500.0
             },
             // More courses...
         ],
         "pendingPayments": 2,
         "completedPayments": 5
     }
     ```

6. **Check for Errors**
   - If any errors occur, ensure the server is running and the URL is correct.

### Additional Tips:
- Use Postman's features like history, collections, and environment variables for better management.
- To test authentication or headers, modify the request using Postman's interface options.

By following these steps, you should be able to successfully test the admin report endpoint with Postman.
