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