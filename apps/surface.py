from fastapi import FastAPI, HTTPException, Query
import httpx
from apps.sonar import extract_page_id

app = FastAPI(title="LinkedIn Insights Gateway")

# Configuration for the Intermediary Service
INTERMEDIARY_SERVICE_URL = "http://localhost:8000/internal/processor" 

@app.get("/api/v1/page/insights")
async def get_page_insights(url_or_id: str = Query(..., description="LinkedIn Page URL or Page ID")):
    """
    First Layer: 
    1. Receives the user request.
    2. Extracts the clean Page ID.
    3. Forwards it to the Intermediary Process via REST API.
    4. Waits and returns the final response.
    """
    
    # Step 1
    page_id = extract_page_id(url_or_id)
    
    if not page_id:
        raise HTTPException(status_code=400, detail="Invalid LinkedIn URL or Page ID provided.")

    print(f"[*] Received Request. Extracted ID: {page_id}")
    print(f"[*] Forwarding to Intermediary Process at: {INTERMEDIARY_SERVICE_URL}")

    # Step 2: Send request to Intermediary Process and wait for response
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                INTERMEDIARY_SERVICE_URL,
                json={"page_id": page_id},
                timeout=700.0 
            )
            
            # Check if intermediary failed
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code, 
                    detail=f"Intermediary Error: {response.text}"
                )
                
            # Step 3: Return the JSON data to the user
            return response.json()

        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=503, 
                detail=f"Failed to connect to Intermediary Service: {exc}"
            )
        
@app.get("/api/v1/page/search")
async def search_companies(
    name: str = Query(None, description="Search by company name"),
    industry: str = Query(None, description="Filter by industry"),
    min_followers: int = Query(None, description="Minimum follower count"),
    max_followers: int = Query(None, description="Maximum follower count"),
    page: int = 1,
    limit: int = 10
):
    # Construct the internal URL
    BRAIN_SEARCH_URL = "http://localhost:8000/internal/search"
    
    params = {
        "name": name,
        "industry": industry,
        "min_followers": min_followers,
        "max_followers": max_followers,
        "page": page,
        "limit": limit
    }
    
    # Remove None values
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BRAIN_SEARCH_URL, params=clean_params)
            return response.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Brain service unavailable")       

# --- TEST ---
@app.post("/internal/processor")
async def mock_intermediary(data: dict):
    return {
        "status": "success", 
        "data": {
            "page_id": data["page_id"],
            "name": "DeepSolv (Mock Data)",
            "industry": "IT Services",
            "source": "This response came from the Intermediary Layer"
        }
    }