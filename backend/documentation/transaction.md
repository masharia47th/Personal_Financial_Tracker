# Transaction API Documentation

## Overview
The Transaction API allows authenticated users to manage financial transactions in the "Where Is My Money" application. Users can create, list, retrieve, update, and delete transactions, which are linked to their accounts and affect account balances based on type (income/expense) and status (completed/pending/canceled).

## Authentication
All endpoints require a valid JWT token obtained from `/auth/login`. Include the token in the `Authorization` header as `Bearer <token>`.

## Base URL
`http://localhost:5000/transactions` (development)

## Endpoints

### 1. Create a Transaction
- **Method**: `POST`
- **Path**: `/transactions`
- **Description**: Creates a new transaction for an account. Updates account balance if `status` is `"completed"`.
- **Request Body**:
  ```json
  {
    "account_id": "uuid",
    "amount": number,
    "category": "string",
    "date": "string", // ISO 8601 format (e.g., "2025-08-13T16:28:00")
    "type": "string", // Must be "income" or "expense"
    "status": "string", // Must be "pending", "completed", or "canceled"
    "note": "string" // Optional
  }
  ```
- **Response**:
  - **201 Created**:
    ```json
    {
      "id": "uuid",
      "account_id": "uuid",
      "amount": number,
      "category": "string",
      "date": "string",
      "type": "string",
      "status": "string",
      "note": "string" // or null
    }
    ```
  - **400 Bad Request**:
    ```json
    {
      "error": "All required fields must be provided"
    }
    ```
    or
    ```json
    {
      "error": "Account not found or unauthorized"
    }
    ```
    or
    ```json
    {
      "error": "Amount must be positive"
    }
    ```
  - **401 Unauthorized**: If JWT is invalid or missing.
- **Example**:
  ```bash
  curl -X POST http://localhost:5000/transactions \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{"account_id": "123e4567-e89b-12d3-a456-426614174000", "amount": 100.00, "category": "Salary", "date": "2025-08-13T16:28:00", "type": "income", "status": "completed", "note": "Monthly salary"}'
  ```

### 2. List All Transactions
- **Method**: `GET`
- **Path**: `/transactions`
- **Description**: Retrieves all transactions for the authenticated user. Optionally filter by `account_id` query parameter.
- **Query Parameters**:
  - `account_id` (optional): UUID of the account to filter transactions.
- **Request Body**: None
- **Response**:
  - **200 OK**:
    ```json
    [
      {
        "id": "uuid",
        "account_id": "uuid",
        "amount": number,
        "category": "string",
        "date": "string",
        "type": "string",
        "status": "string",
        "note": "string" // or null
      },
      ...
    ]
    ```
  - **401 Unauthorized**: If JWT is invalid or missing.
- **Example**:
  ```bash
  curl -X GET http://localhost:5000/transactions?account_id=123e4567-e89b-12d3-a456-426614174000 \
    -H "Authorization: Bearer <token>"
  ```

### 3. Get a Specific Transaction
- **Method**: `GET`
- **Path**: `/transactions/<id>`
- **Description**: Retrieves details of a specific transaction by its ID.
- **Request Body**: None
- **Response**:
  - **200 OK**:
    ```json
    {
      "id": "uuid",
      "account_id": "uuid",
      "amount": number,
      "category": "string",
      "date": "string",
      "type": "string",
      "status": "string",
      "note": "string" // or null
    }
    ```
  - **400 Bad Request**:
    ```json
    {
      "error": "Transaction not found or unauthorized"
    }
    ```
  - **401 Unauthorized**: If JWT is invalid or missing.
- **Example**:
  ```bash
  curl -X GET http://localhost:5000/transactions/123e4567-e89b-12d3-a456-426614174001 \
    -H "Authorization: Bearer <token>"
  ```

### 4. Update a Transaction
- **Method**: `PUT`
- **Path**: `/transactions/<id>`
- **Description**: Updates a transaction’s details. Reverts and reapplies balance changes if `type` or `status` changes.
- **Request Body**:
  ```json
  {
    "amount": number, // Optional
    "category": "string", // Optional
    "date": "string", // Optional, ISO 8601 format
    "type": "string", // Optional, "income" or "expense"
    "status": "string", // Optional, "pending", "completed", or "canceled"
    "note": "string" // Optional
  }
  ```
- **Response**:
  - **200 OK**:
    ```json
    {
      "id": "uuid",
      "account_id": "uuid",
      "amount": number,
      "category": "string",
      "date": "string",
      "type": "string",
      "status": "string",
      "note": "string" // or null
    }
    ```
  - **400 Bad Request**:
    ```json
    {
      "error": "Transaction not found or unauthorized"
    }
    ```
    or
    ```json
    {
      "error": "Amount must be positive"
    }
    ```
  - **401 Unauthorized**: If JWT is invalid or missing.
- **Example**:
  ```bash
  curl -X PUT http://localhost:5000/transactions/123e4567-e89b-12d3-a456-426614174001 \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{"amount": 150.00, "category": "Bonus", "status": "completed"}'
  ```

### 5. Delete a Transaction
- **Method**: `DELETE`
- **Path**: `/transactions/<id>`
- **Description**: Deletes a transaction and reverts its balance impact if `status` was `"completed"`.
- **Request Body**: None
- **Response**:
  - **200 OK**:
    ```json
    {
      "message": "Transaction deleted"
    }
    ```
  - **400 Bad Request**:
    ```json
    {
      "error": "Transaction not found or unauthorized"
    }
    ```
  - **401 Unauthorized**: If JWT is invalid or missing.
- **Example**:
  ```bash
  curl -X DELETE http://localhost:5000/transactions/123e4567-e89b-12d3-a456-426614174001 \
    -H "Authorization: Bearer <token>"
  ```

## Error Handling
- **400 Bad Request**: Invalid input (e.g., missing fields, invalid `account_id`, negative amount).
- **401 Unauthorized**: Missing or invalid JWT token.
- **404 Not Found**: Handled as 400 for invalid transaction IDs.

## Notes
- All endpoints require authentication via JWT.
- `type` must be `"income"` or `"expense"`.
- `status` must be `"pending"`, `"completed"`, or `"canceled"`.
- Account balance updates occur only for `"completed"` transactions.