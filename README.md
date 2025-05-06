# Search Engine

A personal search engine application that crawls, indexes, and provides search capabilities across multiple websites!

## Description

This project is a full-stack web application that creates a personalized search engine for Rhamsez Thevenin's websites and repositories. It consists of a web crawler that indexes content from specified websites, a search API that ranks results using TF-IDF, and a clean, responsive front-end interface that allows users to search through the indexed content. The application also includes a resume viewer component and external links to professional profiles.

The system is designed to be easily deployable using Docker containers and includes CI/CD configuration with GitHub Actions for automatic builds and deployment.

![Screenshot 2025-04-03 at 12-06-55 Search](https://github.com/user-attachments/assets/9e90cdcb-ab74-4eef-a65e-4648810d1760)

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Technologies](#technologies)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [License](#license)

## Installation

### Prerequisites

```
- Docker and Docker Compose
- Git
- Node.js (for local development)
- Python (for local development)
```

### Dependencies

```
Frontend:
- React 19.0.0
- React Router 7.2.0
- TypeScript 5.7
- Vite 6.2.0

Backend:
- FastAPI
- PostgreSQL
- BeautifulSoup4
- psycopg
```

### Installation Steps

```bash
# Step 1: Clone the repository
git clone https://github.com/rhamzthev/search.git

# Step 2: Navigate to the project directory
cd search

# Step 3: Set up environment variables
# Create a .env file with the following variables:
# DOCKERHUB_USERNAME=yourusername
# DOCKERHUB_REPOSITORY_CLIENT=search-client
# DOCKERHUB_REPOSITORY_SERVER=search-server
# DB_HOST=your_db_host
# DB_PASSWORD=your_db_password
# DB_PORT=your_db_port
# DB_NAME=your_db_name
# DB_USER=your_db_user

# Step 4: Build and start containers
docker compose up -d
```

### Platform-Specific Instructions

#### Local Development
```bash
# Client
cd client
npm install
npm run dev

# Server
cd server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd src
uvicorn main:app --reload
```

## Usage

### Basic Example

The search engine provides a simple and intuitive interface. Visit the main page, enter your search terms in the search box, and press Enter or click the search icon.

Results will display with the most relevant matches first, showing titles, URLs, and brief descriptions of the matching content.

### Common Use Cases

1. **Searching across personal websites**
   Navigate to the search page and enter your query to find content across all indexed websites.

2. **Viewing resume**
   Click the "Resume" link in the navigation to view and download the resume in PDF format.

## Features

### Core Functionality
- Web crawler that indexes website content
- Search API with TF-IDF ranking algorithm
- Full-text search across multiple websites
- Resume viewer with PDF support
- Responsive UI that works on mobile and desktop

### Key Highlights
- Fast search results with relevance ranking
- Clean, modern user interface
- Containerized deployment with Docker
- Automated CI/CD pipeline with GitHub Actions

## Technologies

### Tech Stack
- **Frontend**: React, TypeScript, Vite, CSS Modules
- **Backend**: Python, FastAPI
- **Database**: PostgreSQL
- **Deployment**: Docker, GitHub Actions, Nginx
- **Search Algorithm**: TF-IDF (Term Frequency-Inverse Document Frequency)

### Project Structure
```
project/
├── client/               # Frontend React application
│   ├── public/           # Static assets
│   ├── src/              # React components and styles
│   ├── nginx/            # Nginx configuration
│   └── Dockerfile        # Client container configuration
├── server/               # Backend FastAPI application
│   ├── src/              # API code
│   │   ├── db/           # Database operations
│   │   ├── utils/        # Crawler and utility functions
│   │   └── main.py       # API entry point
│   └── Dockerfile        # Server container configuration
├── .github/              # GitHub Actions workflows
└── compose.yaml          # Docker Compose configuration
```

## API Documentation

### Endpoints

#### `GET /api/search`
- **Description**: Search indexed pages based on query terms
- **Parameters**: 
  - `q` (string, required): Search query
  - `limit` (integer, optional, default=10): Maximum number of results
- **Response**: Array of search results, each containing:
  - `id`: Page identifier
  - `url`: Page URL 
  - `title`: Page title
  - `description`: Brief description
  - `score`: Relevance score

## Configuration

### Environment Variables
```
DOCKERHUB_USERNAME=yourusername        # Docker Hub username for image publishing
DOCKERHUB_REPOSITORY_CLIENT=repo-name  # Docker repository for client image
DOCKERHUB_REPOSITORY_SERVER=repo-name  # Docker repository for server image
DB_HOST=hostname                       # PostgreSQL host
DB_PASSWORD=password                   # PostgreSQL password
DB_PORT=5432                           # PostgreSQL port
DB_NAME=database                       # PostgreSQL database name
DB_USER=username                       # PostgreSQL username
```

### Nginx Configuration
The project includes Nginx configuration for SSL termination and reverse proxy to the backend API.

## License

This project uses the MIT License - see the LICENSE file for details.

---

Built by Rhamsez Thevenin 🌹
