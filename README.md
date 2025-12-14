# LinkedIn Insights Microservice

A robust, RESTful microservice designed to **scrape, cache, store, and retrieve LinkedIn Company Page insights**.  
The system implements a **read-through caching strategy** to minimize scraping overhead and maximize performance.

---

## 🚀 Features

- **Smart Read-Through Caching**  
  Checks the database first; triggers scraping only when data is missing or stale.

- **Live Scraping via Apify**  
  Uses Apify actors to fetch real-time metadata such as:
  - Followers
  - Company description
  - Industry
  - Recent posts

- **Clean, Scalable Architecture**  
  Follows **SOLID principles** with a clear separation of concerns:
  - Surface: API Gateway (Entry Point)

  - Brain: Logic Orchestrator (Business Logic)

  - Tentacles: External Scrapers (Data Fetching)
 
  - Locker: Database Storage (Persistence)



- **Resilient by Design**
- Handles emoji storage using `utf8mb4`
- Gracefully manages API failures
- Safely handles missing or partial data

---

## 🛠️ Tech Stack

- **Framework:** FastAPI (Python 3.13)
- **Database:** MariaDB (SQLAlchemy ORM)
- **Scraping Engine:** Apify Client (`apify-client`, `apimaestro`)
- **Server:** Uvicorn (ASGI)

---
## Project Structure (The Octo-Architecture)
```
super-duper-octo-carnival/
├── apps/
│   ├── surface.py       # API Gateway (Layer 1)
│   ├── brain.py         # Logic Orchestrator (Layer 2)
│   ├── locker.py        # Database Access (Layer 3)
│   ├── oyster.py        # Data Formatter & Cleaner
│   ├── tentacles.py     # Apify Scraper Integration
│   ├── anatomy.py       # Database Models
│   ├── sonar.py         # Utilities (ID Extraction)
│   └── CONSTANTS.py     # API Keys
├── requirements.txt
└── README.md
```

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Sudeep-T-Pillai/super-duper-octo-carnival.git
cd super-duper-octo-carnival
```

### 2. Install Dependencies
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Database Configuration
You must create the database with UTF8MB4 support to handle emojis in LinkedIn posts. Run these SQL commands
```sql
-- Log into MySQL
mysql -u root -p

-- Run inside SQL Shell:
CREATE DATABASE linkedin_insights_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'dev_user'@'localhost' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON linkedin_insights_db.* TO 'dev_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
 ```
####  Update apps/anatomy.py with your database credentials:
```
DATABASE_URL = "mysql+pymysql://<user>:<password>@localhost/linkedin_insights_db"
```
### 4. API Keys
```
APIFY_TOKEN = "YOUR_APIFY_TOKEN_HERE"
```

# Running the Microservices
This architecture requires two services running in parallel. Open two terminal windows:

Terminal 1: The Orchestrator (brain.py) This initializes the DB and handles the logic.
```python
python -m uvicorn apps.brain:app --port 8000 --reload
```

Terminal 2: The Gateway API (surface.py) This is the public-facing API.
```python
python -m uvicorn apps.surface:app --port 8001 --reload 
```
---
## API Usage
Endpoint: GET /api/v1/page/insights

- Parameters: url_or_id (string): The LinkedIn Company URL or ID (e.g., deepsolv, microsoft).

curl example 
```curl 
curl "http://localhost:8001/api/v1/page/insights?url_or_id=deepsolv"
 ```

# Response 
```
{
  "page_alias": "deepsolv",
  "name": "Deepsolv",
  "industry": "Computer Software",
  "follower_count": 1231,
  "posts": [
    {
      "content": "🚀 Hackathon Highlights at Deepsolv!..."
    }
  ]
}

```