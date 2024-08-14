from fastapi import FastAPI
from api.endpoints import players

app = FastAPI()

app.include_router(players.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
