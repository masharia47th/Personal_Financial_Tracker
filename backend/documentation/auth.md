# Authentication Flow Documentation - Where Is My Money

## Overview
The authentication system for "Where Is My Money" enables secure user registration, login, and token-based access using JWT (JSON Web Tokens). It uses PostgreSQL for data storage, PBKDF2-SHA256 for password hashing, and Flask for the API.

## Components
- **User Model**: Stores user data (UUID, username, password hash, currency).
- **Auth Service**: Handles registration, login, and token refresh logic.
- **Auth Routes**: REST API endpoints (`/auth/register`, `/auth/login`, `/auth/refresh`).
- **Config**: Defines token expiration (7 hours for access token, 4 days for refresh token).

## Authentication Flow

### 1. Registration
- **Endpoint**: `POST /auth/register`
- **Input**: JSON payload with `username`, `password`, optional `currency` (default: USD).
- **Process**:
  1. Validate input (username and password required).
  2. Check if username exists in the `users` table.
  3. Hash password using PBKDF2-SHA256 (600,000 iterations).
  4. Create new user with UUID, username, hashed password, and currency.
  5. Save to PostgreSQL database.
- **Output**:
  - Success: `201` with user data (`id`, `username`, `currency`).
  - Failure: `400` (missing input or username taken).

### 2. Login
- **Endpoint**: `POST /auth/login`
- **Input**: JSON payload with `username`, `password`.
- **Process**:
  1. Validate input.
  2. Query user by username.
  3. Verify password using PBKDF2-SHA256.
  4. Generate JWT access token (7-hour expiry) and refresh token (4-day expiry) with user ID.
- **Output**:
  - Success: `200` with `access_token`, `refresh_token`, and user data (`id`, `username`, `currency`).
  - Failure: `401` (invalid credentials).

### 3. Token Refresh
- **Endpoint**: `POST /auth/refresh`
- **Input**: JSON payload with `refresh_token`.
- **Process**:
  1. Validate refresh token (JWT decode, check expiry, verify user ID).
  2. Generate new access token (7-hour expiry).
- **Output**:
  - Success: `200` with new `access_token`.
  - Failure: `401` (invalid or expired refresh token).

## Security
- **Password Hashing**: PBKDF2-SHA256 with 600,000 iterations for strong security.
- **JWT**: Signed with a secret key, includes user ID and expiration.
- **Database**: PostgreSQL with UUID for unique user identification.
- **Transport**: Use HTTPS to encrypt API requests.

## Example API Usage
1. **Register**:
   ```bash
   curl -X POST http://localhost:5000/auth/register -H "Content-Type: application/json" -d '{"username":"johndoe","password":"secure123","currency":"USD"}'
   ```
   Response: `{"user":{"id":"uuid","username":"johndoe","currency":"USD"}}`

2. **Login**:
   ```bash
   curl -X POST http://localhost:5000/auth/login -H "Content-Type: application/json" -d '{"username":"johndoe","password":"secure123"}'
   ```
   Response: `{"access_token":"jwt","refresh_token":"jwt","user":{"id":"uuid","username":"johndoe","currency":"USD"}}`

3. **Refresh**:
   ```bash
   curl -X POST http://localhost:5000/auth/refresh -H "Content-Type: application/json" -d '{"refresh_token":"jwt"}'
   ```
   Response: `{"access_token":"new_jwt"}`