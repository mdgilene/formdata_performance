import os
from io import BytesIO

os.environ['HTTPX_LOG_LEVEL'] = 'debug'

import httpx


def get_data():
    # Generate 128 Mb of dummy bytes
    return b'0' * 128 * (1024) ** 2

async def run_formdata():
    async with httpx.AsyncClient(timeout=None) as client:

        # Send data as multipart/form-data
        await client.post(
            "http://localhost:8000/formdata",
            files={"file": BytesIO(get_data())}
        )


async def run_body():
    async with httpx.AsyncClient(timeout=None) as client:

        # Generator - Allows us to control in how large of chunks
        # the data is streamed
        async def stream(data, chunk_size=1024):
            while True:
                chunk = data.read(chunk_size)
                if not chunk:
                    break
                yield chunk

        # Send data as body content
        await client.post(
            "http://localhost:8000/body",
            data=stream(BytesIO(get_data()), chunk_size=1024**2)
        )



if __name__ == "__main__":
    import asyncio

    asyncio.run(run_body())
    asyncio.run(run_formdata())
