class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://qirisiti:zTELBtbfX@localhost/whereismymoney'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = 7 * 3600  # 7 hours in seconds
    JWT_REFRESH_TOKEN_EXPIRES = 4 * 24 * 3600  # 4 days in seconds
    JWT_TOKEN_LOCATION = ['headers']
    ALLOWED_ORIGINS = [
        "http://localhost:5173",  # Development
        "https://your-production-domain.com"  # Replace with actual prod URL
    ]