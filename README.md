# Personal Portfolio Search Engine

A custom search engine that indexes and provides searchable access to all my portfolio content, personal websites, and professional profiles.

## Features

- 🔍 Real-time search functionality
- 🎯 TF-IDF based search ranking
- 🕷️ Automated web crawler for content indexing
- 🎨 Clean, modern UI inspired by popular search engines
- 📱 Responsive design for all devices
- ⚡ Fast and efficient search results

## Tech Stack

### Frontend
- React 19 with TypeScript
- Vite for build tooling
- React Router for navigation
- Custom CSS with CSS Variables for theming

### Backend
- FastAPI for the REST API
- PostgreSQL for data storage
- psycopg for database connectivity
- BeautifulSoup4 for web crawling

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- Python 3.8+
- PostgreSQL database

### Backend Setup

1. Create a virtual environment and install dependencies:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

2. Set up your environment variables in `.env`:
```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
```

3. Set up the database:
```bash
psql -U your_db_user -d your_db_name -f db/tables.sql
```

4. Start the backend server:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

## Architecture

### Search Implementation
The search functionality uses TF-IDF (Term Frequency-Inverse Document Frequency) scoring for ranking results. The crawler processes content and stores word frequencies in the database, which are then used to calculate relevance scores during search.

### Database Schema
- `pages`: Stores crawled web pages
- `keywords`: Stores unique keywords
- `keyword_pages`: Maps keywords to pages with frequency counts

### Web Crawler
The crawler automatically indexes content from specified start URLs, following links to related pages while respecting robots.txt rules and implementing polite crawling practices.

## API Endpoints

- `GET /search?q={query}`: Search for pages matching the query
- `GET /items/{item_id}`: Retrieve specific item details

## Contributing

Feel free to submit issues and enhancement requests!

## License

[MIT License](LICENSE)

## Contact

- LinkedIn: [linkedin.com/in/rhamzthev](https://linkedin.com/in/rhamzthev)
- GitHub: [github.com/rhamzthev](https://github.com/rhamzthev)
