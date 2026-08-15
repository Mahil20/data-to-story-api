## Live Demo
- Frontend: https://your-actual-netlify-url.netlify.app
- API docs: https://data-to-story-api.netlify.app/

Note: the backend is hosted on a free tier and may take 30-60 seconds to wake up on the first request after a period of inactivity.


# Data-to-Story API

An API that turns uploaded CSV data into AI-generated narrative insights, grounded in real calculated statistics.

## Features
- User authentication (JWT)
- CSV dataset upload and parsing
- Automatic statistical analysis (means, correlations, etc.)
- AI-generated narrative summaries using Google Gemini
- Story history per user

## Tech Stack
- FastAPI
- PostgreSQL + SQLModel
- Pandas
- Google Gemini API
- JWT authentication (passlib + python-jose)

## How it works
1. User uploads a CSV dataset
2. The backend calculates real statistics (mean, min, max, correlations) using pandas
3. Those calculated facts are sent to Gemini, which is instructed to narrate them without inventing new numbers
4. The generated story is saved and can be retrieved later

## Running locally
1. Clone this repo
2. Create a virtual environment and install dependencies: `pip install -r requirements.txt`
3. Set up a `.env` file with `DATABASE_URL`, `SECRET_KEY`, and `GEMINI_API_KEY`
4. Run: `uvicorn main:app --reload`
5. Visit `http://127.0.0.1:8000/docs` to explore the API
