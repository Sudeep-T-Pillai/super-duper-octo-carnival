from fastapi import FastAPI, Depends
from apps.anatomy import SessionLocal, init_db
from apps.locker import DatabaseGateway
from apps.oyster import format_scraper_result
from apps.tentacles import get_linkedin_data 

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

init_db()

@app.post("/internal/processor")
def process_request(payload: dict, db = Depends(get_db)):
    page_id = payload.get("page_id")
    gateway = DatabaseGateway(db)
    
    # 1. Check DB
    check_payload = {"flag": 0, "page_id": page_id}
    db_result = gateway.execute(check_payload)
    
    if db_result["status"] == "found":
        print("[Part B] Hit! Returning from DB.")
        return db_result["data"]
    
    print(f"[Part B] Miss! Scraping LinkedIn for {page_id}...")
    
    # --- CALLING THE SCRAPER ---
    raw_data = get_linkedin_data(page_id)
    
    # 2. Format
    formatted_payload = format_scraper_result(raw_data, page_id)
    
    # 3. Save to DB
    insert_result = gateway.execute(formatted_payload)
    
    if insert_result["status"] == "success":
        return formatted_payload["data"]
        
    return {"error": "Processing Failed"}