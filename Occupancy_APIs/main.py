from fastapi import FastAPI
from router import occupancy
import uvicorn



app = FastAPI()
app.include_router(occupancy.routers)

if __name__ == "__main__":
    uvicorn.run("app", host="0.0.0.0", port=8000, reload=True)
