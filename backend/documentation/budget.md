# Budget API Documentation

## Overview
The Budget API allows authenticated users to manage spending budgets in the "Where Is My Money" application. Users can create, list, retrieve, update, and delete budgets, which are linked to their user ID and include a category, spending limit, and period.

## Authentication
All endpoints require a valid JWT token obtained from `/auth/login`. Include the token in the `Authorization` header as `Bearer <token>`.

## Base URL
`http://localhost:5000/budgets` (development)

## Endpoints

### 1. Create a Budget
- **Method**: `POST`
- **Path**: `/budgets`
- **Description**: Creates a new budget for the authenticated user.
- **Request Body**:
  ```json
  {
    "category": "string",
    "limit": number,
    "period": "string" // Must be one of: "1 day", "2 days", "1 week", "1 month", "3 months", "6 months", "1 year"
  }
  ```
- **Response**:
  - **201 Created**:
    ```json
    {
      "id": "uuid",
      "user_id": "uuid",
      "category": "string",
      "limit": number,
      "period": "string"
    }
    ```
  - **400 Bad Request**:
    ```json
    {
      "error": "Category, limit, and period are required"
    }
    ```
    or
    ```json
    {
      "error": "Budget for this category already exists"
    }
    ```
    or
    ```json
    {
      "error": "Limit must be positive"
    }
    ```
  - **401 Unauthorized**: If JWT is invalid or missing.
- **Example**:
  ```bash
  curl -X POST http://localhost:5000/budgets \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{"category": "Food", "limit": 200.00, "period": "1 month"}'
  ```

### 2. List All Budgets
- **Method**: `GET`
- **Path**: `/budgets`
- **Description**: Retrieves all budgets for the authenticated user.
- **Request Body**: None
- **Response**:
  - **200 OK**:
    ```json
    [
      {
        "id": "uuid",
        "user_id": "uuid",
        "category": "string",
        "limit": number,
        "period": "string"
      },
      ...
    ]
    ```
  - **401 Unauthorized**: If JWT is invalid or missing.
- **Example**:
  ```bash
  curl -X GET http://localhost:5000/budgets \
    -H "Authorization: Bearer <token>"
  ```

### 3. Get a Specific Budget
- **Method**: `GET`
- **Path**: `/budgets/<id>`
- **Description**: Retrieves details of a specific budget by its ID.
- **Request Body**: None
- **Response**:
  - **200 OK**:
    ```json
    {
      "id": "uuid",
      "user_id": "uuid",
      "category": "string",
      "limit": number,
      "period": "string"
    }
    ```
  - **400 Bad Request**:
    ```json
    {
      "error": "Budget not found or unauthorized"
    }
    ```
  - **401 Unauthorized**: If JWT is invalid or missing.
- **Example**:
  ```bash
  curl -X GET http://localhost:5000/budgets/123e4567-e89b-12d3-a456-426614174002 \
    -H "Authorization: Bearer <token>"
  ```

### 4. Update a Budget
- **Method**: `PUT`
- **Path**: `/budgets/<id>`
- **Description**: Updates a budget’s category, limit, or period.
- **Request Body**:
  ```json
  {
    "category": "string", // Optional
    "limit": number, // Optional
    "period": "string" // Optional, must be one of: "1 day", "2 days", "1 week", "1 month", "3 months", "6 months", "1 year"
  }
  ```
- **Response**:
  - **200 OK**:
    ```json
    {
      "id": "uuid",
      "user_id": "uuid",
      "category": "string",
      "limit": number,
      "period": "string"
    }
    ```
  - **400 Bad Request**:
    ```json
    {
      "error": "Budget not found or unauthorized"
    }
    ```
    or
    ```json
    {
      "error": "Budget for this category already exists"
    }
    ```
    or
    ```json
    {
      "error": "Limit must be positive"
    }
    ```
  - **401 Unauthorized**: If JWT is invalid or missing.
- **Example**:
  ```bash
  curl -X PUT http://localhost:5000/budgets/123e4567-e89b-12d3-a456-426614174002 \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{"category": "Dining", "limit": 250.00, "period": "1 month"}'
  ```

### 5. Delete a Budget
- **Method**: `DELETE`
- **Path**: `/budgets/<id>`
- **Description**: Deletes a specific budget by its ID.
- **Request Body**: None
- **Response**:
  - **200 OK**:
    ```json
    {
      "message": "Budget deleted"
    }
    ```
  - **400 Bad Request**:
    ```json
    {
      "error": "Budget not found or unauthorized"
    }
    ```
  - **401 Unauthorized**: If JWT is invalid or missing.
- **Example**:
  ```bash
  curl -X DELETE http://localhost:5000/budgets/123e4567-e89b-12d3-a456-426614174002 \
    -H "Authorization: Bearer <token>"
  ```

## Error Handling
- **400 Bad Request**: Invalid input (e.g., missing fields, duplicate category, negative limit).
- **401 Unauthorized**: Missing or invalid JWT token.
- **404 Not Found**: Handled as 400 for invalid budget IDs.

## Notes
- All endpoints require authentication via JWT.
- `period` must be one of: `"1 day"`, `"2 days"`, `"1 week"`, `"1 month"`, `"3 months"`, `"6 months"`, `"1 year"`.
- Budgets are unique per user and category.