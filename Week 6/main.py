from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, Welcome to my website!"}

@app.get("/hello/{name}")
def hello(name: str):
    return {"greeting": f"Hello {name}"}

@app.get("/add")
def add(a: int, b: int):
    return {"a": a, "b": b, "sum": a + b}