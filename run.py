import uvicorn

if __name__ == "__main__":
    print("Starting Tool-Manager...")
    print("Access the API docs at http://localhost:8000/docs")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 