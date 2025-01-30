import uvicorn
import requests
import os
from fastapi import FastAPI, Query, HTTPException
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# FatSecret API credentials from .env
CLIENT_ID = os.getenv("ee7e9c7bdf874f63a94b1c71e04e040e")
CLIENT_SECRET = os.getenv(" 3d31c88ef3b1469fa0f43b98f71522bc")
TOKEN_URL = "https://oauth.fatsecret.com/connect/token"

# Function to get OAuth2 token
def get_access_token():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "scope": "basic",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, headers=headers, data=data)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to get access token")
    
    return response.json().get("access_token")

# API Endpoint to search for food items
@app.get("/search_food/")
def search_food(query: str = Query(..., description="Food item to search")):
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    api_url = "https://platform.fatsecret.com/rest/server.api"

    params = {
        "method": "foods.search",
        "format": "json",
        "search_expression": query
    }

    response = requests.get(api_url, headers=headers, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch food data")

    return response.json()

# Explicit main function
def main():
    uvicorn.run(app, host="127.0.0.1", port=8000)

# Entry point
if __name__ == "__main__":
    main()
