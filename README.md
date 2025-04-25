# UrlShort 🚀

A FastAPI-based URL Shortener service that allows users to convert long URLs into shortened links, and redirect users to the original URLs using the short codes.

## Features

- Shorten long URLs with a unique short code
- Redirect users from short code to the original URL
- PostgreSQL-backed persistent storage
- Fast and lightweight, built with FastAPI

---

## Endpoints

### `POST /shorten`

**Description**: Accepts a long URL and returns a shortened version.  
**Request Body**:
```json
{
  "long_url": "https://example.com"
}
```

**Response**:
```json
{
  "short_url": "http://localhost:8000/abc123"
}
```

---

### `GET /{short_code}`

**Description**: Redirects the user to the original long URL associated with the short code.

---

## Database Setup

This project uses **PostgreSQL** as its database. Ensure the following environment variables are set:

| Variable   | Description                          |
|------------|--------------------------------------|
| `DB_HOST`  | Hostname of the PostgreSQL server    |
| `DB_PORT`  | Port number (usually `5432`)         |
| `DB_USER`  | Username for the database            |
| `DB_PASS`  | Password for the database            |
| `DB_NAME`  | Database name                        |

The database should have a table called `urls` with the following schema:

```sql
CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    long_url TEXT NOT NULL,
    short_code TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/urlshort.git
cd urlshort
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

You can use a `.env` file or export variables directly in your terminal:

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_USER=your_user
export DB_PASS=your_password
export DB_NAME=your_db
```

### 4. Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at: [http://localhost:8000](http://localhost:8000)

---

## 📁 Project Structure

```
urlshort/
├── app/                      # Application module
│   ├── database.py           # DB connection setup
│   ├── main.py               # FastAPI routes & logic
│   └── models.py             # SQLAlchemy models/schema
│
├── output_IMG/               # API flow screenshots
│   ├── DB.png
│   ├── GetRequest.png
│   └── PostRequest.png
│
├── .env                      # Environment variables
├── .gitignore                # Git ignored files
├── README.md                 # Project documentation
└── requirements.txt          # Python dependencies
```

---
