# Account API Documentation

## Overview
The Account API allows authenticated users to manage their financial accounts in the "Where Is My Money" application. Users can create, list, retrieve, update, and delete accounts, which are linked to their user ID and include details like name, balance, and account type.

## Authentication
All endpoints require a valid JWT token obtained from `/auth/login`. Include the token in the `Authorization` header as `Bearer <token>`.

## Base URL
`http://localhost:5000/accounts` (development)

## Endpoints

### 1. Create an Account
- **Method**: `POST`
- **Path**: `/accounts`
- **Description**: Creates a new account for the authenticated user.
- **Request Body**:
  ```json
  {
    "name": "string",
    "account_type": "string" // Must be one of: "savings", "checking", "cash", "investment"
  }
  ```
- **Response**:
  - **201 Created**:
    ```json
    {
      "id": "uuid",
      "user_id": "uuid",
      "name": "string",
      "balance": number,
      "account_type": "string"
    }
    ```
  - **400 Bad Request**:
    ```json
    {
      "error": "Name and account type are required"
    }
    ```
    or
    ```json
    {
      "error": "Account name already exists for this user"
    }
    ```
  - **401 Unauthorized**: If JWT is invalid or missing.
- **Example**:
  ```bash
  curl -X POST http://localhost:5000/accounts \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{"name": "Savings", "account_type": "savings"}'
  ```

### 2. List All Accounts
- **Method**: `GET`
- **Path**: `/accounts`
- **Description**: Retrieves all accounts for the authenticated user.
- **Request Body**: None
- **Response**:
  - **200 OK**:
    ```json
    [
      {
        "id": "uuid",
        "user_id": "uuid",
        "name": "string",
        "balance": number,
        "account_type": "string"
      },
      ...
    ]
    ```
  - **401 Unauthorized**: If JWT is invalid or missing.
- **Example**:
  ```bash
  curl -X GET http://localhost:5000/accounts \
    -H "Authorization: Bearer <token>"
  ```

### 3. Get a Specific Account
- **Method**: `GET`
- **Path**: `/accounts/<id>`
- **Description**: Retrieves details of a specific account by its ID.
- **Request Body**: None
- **Response**:
  - **200 OK**:
    ```json
    {
      "id": "uuid",
      "user_id": "uuid",
      "name": "string",
      "balance": number,
      "account_type": "string"
    }
    ```
  - **400 Bad Request**:
    ```json
    {
      "error": "Account not found or unauthorized"
    }
    ```
  - **401 Unauthorized**: If JWT is invalid or missing.
- **Example**:
  ```bash
  curl -X GET http://localhost:5000/accounts/<account_id> \
    -H "Authorization: Bearer <token>"
  ```

### 4. Update an Account
- **Method**: `PUT`
- **Path**: `/accounts/<id>`
- **Description**: Updates the name or account type of a specific account.
- **Request Body**:
  ```json
  {
    "name": "string", // Optional
    "account_type": "string" // Optional, must be one of: "savings", "checking", "cash", "investment"
  }
  ```
- **Response**:
  - **200 OK**:
    ```json
    {
      "id": "uuid",
      "user_id": "uuid",
      "name": "string",
      "balance": number,
      "account_type": "string"
    }
    ```
  - **400 Bad Request**:
    ```json
    {
      "error": "Account not found or unauthorized"
    }
    ```
    or
    ```json
    {
      "error": "Account name already exists for this user"
    }
    ```
  - **401 Unauthorized**: If JWT is invalid or missing.
- **Example**:
  ```bash
  curl -X PUT http://localhost:5000/accounts/<account_id> \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{"name": "New Savings", "account_type": "checking"}'
  ```

### 5. Delete an Account
- **Method**: `DELETE`
- **Path**: `/accounts/<id>`
- **Description**: Deletes a specific account by its ID.
- **Request Body**: None
- **Response**:
  - **200 OK**:
    ```json
    {
      "message": "Account deleted"
    }
    ```
  - **400 Bad Request**:
    ```json
    {
      "error": "Account not found or unauthorized"
    }
    ```
  - **401 Unauthorized**: If JWT is invalid or missing.
- **Example**:
  ```bash
  curl -X DELETE http://localhost:5000/accounts/<account_id> \
    -H "Authorization: Bearer <token>"
  ```

## Error Handling
- **400 Bad Request**: Invalid input or business logic violation (e.g., duplicate account name).
- **401 Unauthorized**: Missing or invalid JWT token.
- **404 Not Found**: Not explicitly returned; handled as 400 for invalid account IDs.

## Notes
- All endpoints require authentication via JWT.
- The `account_type` must match one of the predefined values: `"savings"`, `"checking"`, `"cash"`, `"investment"`.
- Account balance updates will be handled by transaction-related endpoints (to be implemented).