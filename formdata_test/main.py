import io
import time

from fastapi import FastAPI, File, Request, UploadFile

app = FastAPI()

@app.middleware('http')
async def time_log(request: Request, call_next):
    """
    Middleware to log the time spent processing each request
    """

    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    print(f'Request took {end_time - start_time}')
    return response


@app.post("/formdata")
async def index(file: UploadFile = File(...)):
    """
    Take in file as multipart/form-data
    """

    file.file.seek(0, io.SEEK_END)
    print(f'[DONE] FORMDATA - Got data <{file.file.tell()} bytes>')
    return {}

@app.post("/body")
async def index(request: Request):
    """
    Take in file as raw body content
    """

    data = await request.body()
    print(f'[DONE] BODY - Got data <{len(data)} bytes>')
    return {}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
