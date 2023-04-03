import uvicorn
from fastapi import FastAPI
from mangum import Mangum
from app.api.routers.car_router import get_car_router

# Initialize the FastAPI app.
app = FastAPI()

# Create a handler for AWS Lambda.
handler = Mangum(app)

# Include the car router.
app.include_router(get_car_router())

# Start the server.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
