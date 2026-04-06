# House Finder Bot

This project consists of a FastAPI backend and a React frontend built with Vite.

## Project Structure
```
house_finder_bot/
├── backend/    # FastAPI backend
├── frontend/   # React frontend
└── docker-compose.yml
```

## Prerequisites
- Docker & Docker Compose
- Node.js (if running frontend locally)
- Python 3.10+ (if running backend locally)

## Running the Project

### Using Docker Compose
1. Create a `.env` file in the project root:
   ```env
   POSTGRES_USER=hf_user
   POSTGRES_PASSWORD=hf_pass
   POSTGRES_DB=hf_db
   DATABASE_URL=postgresql://hf_user:hf_pass@db:5432/hf_db
   VITE_API_URL=http://localhost:8000
   ```
2. Run the following command:
   ```bash
   docker-compose up --build
   ```
3. Access the services:
   - Backend: [http://localhost:8000](http://localhost:8000)
   - Frontend: [http://localhost:3000](http://localhost:3000)

### Running Locally
#### Backend
1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

#### Frontend
1. Navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Access the frontend at [http://localhost:3000](http://localhost:3000).

## Notes
- Ensure the `VITE_API_URL` in the `.env` file points to the backend URL.
- Use `docker-compose logs` to debug any issues.