from fastapi import FastAPI, Depends, HTTPException
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# FatSecret API credentials
CLIENT_ID = os.getenv("ee7e9c7bdf874f63a94b1c71e04e040e")
CLIENT_SECRET = os.getenv(" 78c9febbbe6b4eb4a385182cbe219f70")
TOKEN_URL = "https://oauth.fatsecret.com/connect/token"
SEARCH_URL = "https://platform.fatsecret.com/rest/server.api"

async def get_access_token():
    """Fetch OAuth 2.0 token from FatSecret API"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TOKEN_URL,
            data={"grant_type": "client_credentials"},
            auth=(CLIENT_ID, CLIENT_SECRET),
        )
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Failed to get access token")
        
        return response.json().get("access_token")

@app.get("/search-foods/")
async def search_foods(query: str, token: str = Depends(get_access_token)):
    """Search for foods using FatSecret API"""
    params = {
        "method": "foods.search",
        "search_expression": query,
        "format": "json"
    }
    headers = {"Authorization": f"Bearer {token}"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(SEARCH_URL, params=params, headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch food data")
        
        return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

