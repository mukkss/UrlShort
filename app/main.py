import os
import fastapi
from app.models import Base, URL
from urllib.parse import urlparse
from sqlalchemy.orm import Session
from app.database import get_db, engine
from fastapi import HTTPException, Depends
from pydantic import BaseModel, field_validator
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Base URL for shortened URLs.  Make this configurable.
BASE_URL = os.environ.get("BASE_URL", "http://shorty")


# Define the data model for the request
class URLShortenRequest(BaseModel):
    long_url: str

    @field_validator("long_url")
    @classmethod
    def validate_long_url(cls, value):
        """
        Validates that the provided URL is a valid URL.
        """
        parsed_url = urlparse(value)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError("Invalid URL")
        return value


# Define the data model for the response.
class URLShortenResponse(BaseModel):
    short_url: str



# FastAPI application instance
app = fastapi.FastAPI()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# Create the database tables
Base.metadata.create_all(bind=engine)

# --- ADD THIS SECTION FOR STATIC FILES ---
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="app/templates")  # Create a "templates" directory


@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: fastapi.Request):  # Add the request parameter
    """
    Serves the main HTML frontend using Jinja2.
    """
    return templates.TemplateResponse("index.html", {"request": request})  # Pass the request to the template


def generate_short_code(length=6):
    """
    Generates a random short code of the specified length.
    """
    import string
    import random
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))



@app.post("/shorten", response_model=URLShortenResponse)
async def shorten_url(request: URLShortenRequest, db: Session = Depends(get_db)):
    """
    Shortens a long URL and stores it in the database.

    Args:
        request (URLShortenRequest): The request containing the long URL.
        db (Session):  The database session (dependency injection).

    Returns:
        URLShortenResponse: The shortened URL.

    Raises:
        HTTPException (400): If the long URL is invalid.
        HTTPException (500): If a database error occurs.
    """
    long_url = request.long_url
    short_code = generate_short_code()

    try:
        # Check if the long URL already exists in the database.
        existing_url = db.query(URL).filter(URL.long_url == long_url).first()
        if existing_url:
            short_url = f"{BASE_URL}/{existing_url.short_code}"
            return URLShortenResponse(short_url=short_url)

        # Check if the short code already exists
        existing_short_code = db.query(URL).filter(URL.short_code == short_code).first()
        if existing_short_code:
            short_code = generate_short_code()  # Keep generating until unique

        # Insert the new URL mapping into the database.
        new_url = URL(long_url=long_url, short_code=short_code)
        db.add(new_url)
        db.commit()
        db.refresh(new_url)  # Get the newly created id

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to store URL mapping")

    short_url = f"{BASE_URL}/{short_code}"
    return URLShortenResponse(short_url=short_url)



@app.get("/{short_code}")
async def redirect_url(short_code: str, db: Session = Depends(get_db)):
    """
    Redirects to the original URL based on the short code.

    Args:
        short_code (str): The short code.
        db (Session): The database session.

    Returns:
        RedirectResponse:  A redirect to the original URL.

    Raises:
        HTTPException (404): If the short code is not found in the database.
        HTTPException (500):  If a database error occurs.
    """
    try:
        url = db.query(URL).filter(URL.short_code == short_code).first()
        if not url:
            raise HTTPException(status_code=404, detail="Short URL not found")
        long_url = url.long_url
        return fastapi.responses.RedirectResponse(url=long_url, status_code=302)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve URL")


