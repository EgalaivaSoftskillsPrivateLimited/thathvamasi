# Thathvamasi HR Consultancy - Backend API

FastAPI backend for Thathvamasi HR Consultancy website with PostgreSQL database.

## Features

- **Candidate Management**: Registration with resume upload
- **Client Management**: Hiring requirement submission
- **Blog CMS**: Full blog management system
- **File Upload**: Secure file upload with Cloudinary / local storage
- **Admin Authentication**: JWT-based authentication
- **Email Notifications**: Automated email notifications
- **API Documentation**: Auto-generated OpenAPI/Swagger docs

## Tech Stack

- **Framework**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL with SQLAlchemy 2.0 (AsyncPG) & Alembic migrations
- **File Storage**: Cloudinary
- **Authentication**: JWT with bcrypt
- **Email**: SMTP with aiosmtplib
- **Validation**: Pydantic v2

## Project Structure

```
backend/
├── app/
│   ├── api/                 # API endpoints
│   │   ├── candidates/     # Candidate routes
│   │   ├── clients/        # Client routes
│   │   ├── blogs/         # Blog routes
│   │   ├── auth/          # Authentication routes
│   │   ├── upload/        # File upload routes
│   │   └── contact/       # Contact routes
│   ├── core/              # Core configurations
│   │   ├── config.py      # Settings
│   │   ├── database.py    # MongoDB connection
│   │   └── security.py    # Security utilities
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   ├── utils/             # Utilities
│   └── main.py           # FastAPI application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md            # This file
```

## Setup Instructions

### 1. Prerequisites

- Python 3.10 or higher
- MongoDB (local or MongoDB Atlas)
- Cloudinary account (for file storage)

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configurations
# Required:
# - POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
# - JWT_SECRET_KEY
# - CLOUDINARY credentials (optional)
# - EMAIL credentials (optional)
```

### 4. Database Setup

Ensure PostgreSQL is running locally or with Docker:

```bash
# Using Docker Compose
docker-compose up -d postgres

# Run database migrations
alembic upgrade head
```

### 5. Running the Application

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 6. API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/auth/login` - Admin login
- `POST /api/auth/register` - Admin registration
- `POST /api/auth/refresh` - Refresh token

### Candidates
- `POST /api/candidates/` - Register new candidate
- `GET /api/candidates/` - Get candidates (admin)
- `GET /api/candidates/{id}` - Get candidate by ID (admin)
- `PUT /api/candidates/{id}/status` - Update candidate status (admin)

### Clients
- `POST /api/clients/` - Submit client hiring requirement
- `GET /api/clients/` - Get clients (admin)
- `GET /api/clients/{id}` - Get client by ID (admin)

### Blogs
- `GET /api/blogs/` - Get published blogs
- `GET /api/blogs/{slug}` - Get blog by slug
- `POST /api/blogs/` - Create blog (admin)
- `PUT /api/blogs/{id}` - Update blog (admin)
- `DELETE /api/blogs/{id}` - Delete blog (admin)

### File Upload
- `POST /api/upload/resume` - Upload resume
- `POST /api/upload/jd` - Upload job description
- `POST /api/upload/image` - Upload image

### Contact
- `POST /api/contact/` - Submit contact form

## File Upload

The backend supports secure file uploads:

### Supported File Types:
- **Resumes**: PDF, DOC, DOCX (max 5MB)
- **Job Descriptions**: PDF, DOC, DOCX (max 10MB)
- **Images**: JPEG, PNG, GIF, WebP (max 5MB)

### Storage:
- Files are stored in Cloudinary
- Secure URLs are returned
- Automatic optimization for images

## Security Features

- JWT authentication with refresh tokens
- Password hashing with bcrypt
- CORS configuration
- Rate limiting
- Input validation with Pydantic
- File type and size validation
- Secure file upload with sanitization

## Email Notifications

Automatic emails are sent for:
- Candidate registration confirmation
- Client enquiry notification
- Admin notifications for new submissions
- Password reset requests

## Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/
```

## Deployment

### Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Platform Deployment Options:
- **Railway**: Easy deployment with MongoDB integration
- **Render**: Free tier available
- **Heroku**: Traditional PaaS
- **AWS ECS/Fargate**: Production-grade
- **DigitalOcean App Platform**: Simple deployment

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `MONGODB_URI` | MongoDB connection string | Yes | - |
| `JWT_SECRET_KEY` | Secret key for JWT tokens | Yes | - |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | Yes | - |
| `CLOUDINARY_API_KEY` | Cloudinary API key | Yes | - |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | Yes | - |
| `EMAIL_HOST` | SMTP server host | Yes | - |
| `EMAIL_USERNAME` | SMTP username | Yes | - |
| `EMAIL_PASSWORD` | SMTP password | Yes | - |
| `DEBUG` | Debug mode | No | False |
| `CORS_ORIGINS` | CORS allowed origins | No | Localhost + production |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is proprietary software for Thathvamasi HR Consultancy.

## Support

For technical support, contact the development team.

---

**Thathvamasi HR Consultancy**  
Coimbatore, Tamil Nadu  
contact@thathvamasi.com