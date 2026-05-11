import uvicorn

if __name__ == "__main__":
    uvicorn.run("crud.app.api:app", host="127.0.0.1")