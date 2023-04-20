import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from app.api.routers.veiculo_router import get_veiculo_router

# Initialize the FastAPI app.
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["OPTIONS", "GET", "POST", "PUT", "DELETE"],
    # Headers should be pdf or json, but more testing is required
    # "Content-Type", "application/pdf", "application/json"
    allow_headers=["*"]
)

# Create a handler for AWS Lambda.
handler = Mangum(app)

# Include the car router.
app.include_router(get_veiculo_router())

# Start the server.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
