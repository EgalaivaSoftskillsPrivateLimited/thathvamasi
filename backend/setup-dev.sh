#!/bin/bash

# Development Setup Script for Thathvamasi HR Consultancy Backend

echo "🛠️  Setting up Thathvamasi HR Consultancy Backend for development..."

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    
    # Generate a random JWT secret key
    JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    
    # Update .env with development values
    cat > .env << EOL
# Development Environment
DEBUG=True
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development

# PostgreSQL (using Docker)
POSTGRES_USER=thathvamasi
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=thathvamasi_hr_dev

# Database Pool Configuration
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10
DB_POOL_RECYCLE=3600

# JWT Authentication
JWT_SECRET_KEY=$JWT_SECRET

# Cloudinary (optional for development)
CLOUDINARY_CLOUD_NAME=dev_cloud
CLOUDINARY_API_KEY=dev_key
CLOUDINARY_API_SECRET=dev_secret

# Email (optional for development)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=dev@thathvamasi.com
EMAIL_PASSWORD=dev_password
EMAIL_FROM=noreply@thathvamasi.com
EMAIL_USE_TLS=True

# WhatsApp
WHATSAPP_NUMBER=+919876543210

# Admin User
ADMIN_EMAIL=admin@thathvamasi.com
ADMIN_PASSWORD=admin123

# Redis (optional)
# REDIS_URL=redis://localhost:6379
EOL
    
    echo "✅ .env file created with development settings"
    echo "📝 You can modify these values in the .env file"
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker is not installed. Installing dependencies without Docker..."
    
    # Check if PostgreSQL is installed locally
    if ! command -v psql &> /dev/null; then
        echo "❌ PostgreSQL is not installed locally."
        echo "📦 Please install PostgreSQL or use Docker for development."
        echo "   Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib"
        echo "   macOS: brew install postgresql"
        echo "   Windows: Download from https://www.postgresql.org/download/"
        exit 1
    fi
else
    echo "🐳 Starting PostgreSQL and Redis with Docker..."
    docker-compose up -d postgres redis
    
    echo "⏳ Waiting for PostgreSQL to start..."
    sleep 10
    
    # Check if PostgreSQL is ready
    if docker-compose exec -T postgres pg_isready -U thathvamasi; then
        echo "✅ PostgreSQL is ready at postgres://localhost:5432"
    else
        echo "❌ PostgreSQL failed to start"
        docker-compose logs postgres
        exit 1
    fi
    
    echo "✅ Redis is ready at redis://localhost:6379"
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create upload directories
echo "📁 Creating upload directories..."
mkdir -p app/static/uploads/resumes
mkdir -p app/static/uploads/jds
mkdir -p app/static/uploads/blog_images

# Run database migrations
echo "🗄️  Running database migrations..."
if command -v docker &> /dev/null && docker-compose ps | grep -q "postgres"; then
    # Using Docker
    echo "   Using Docker PostgreSQL instance..."
    # Update alembic.ini with correct URL
    sed -i "s|sqlalchemy.url = .*|sqlalchemy.url = postgresql://thathvamasi:password@localhost:5432/thathvamasi_hr_dev|" alembic.ini
    
    # Run migrations
    alembic upgrade head
else
    # Using local PostgreSQL
    echo "   Using local PostgreSQL instance..."
    # Update alembic.ini with correct URL
    sed -i "s|sqlalchemy.url = .*|sqlalchemy.url = postgresql://thathvamasi:password@localhost:5432/thathvamasi_hr_dev|" alembic.ini
    
    # Create database if it doesn't exist
    if ! psql -U thathvamasi -h localhost -p 5432 -lqt | cut -d \| -f 1 | grep -qw thathvamasi_hr_dev; then
        echo "   Creating database: thathvamasi_hr_dev"
        createdb -U thathvamasi -h localhost -p 5432 thathvamasi_hr_dev
    fi
    
    # Run migrations
    alembic upgrade head
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Start the backend: ./start.sh"
echo "2. Access API docs: http://localhost:8000/docs"
echo "3. Access pgAdmin: http://localhost:5050 (if using Docker)"
echo "   - Email: admin@thathvamasi.com"
echo "   - Password: admin123"
echo "4. Access Redis CLI: redis-cli (if using Docker/Local)"
echo ""
echo "Default admin credentials for API:"
echo "  Email: admin@thathvamasi.com"
echo "  Password: admin123"
echo ""
echo "PostgreSQL connection:"
echo "  Host: localhost:5432"
echo "  Database: thathvamasi_hr_dev"
echo "  Username: thathvamasi"
echo "  Password: password"
echo ""