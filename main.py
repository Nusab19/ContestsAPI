from fastapi import FastAPI

from platforms import atcoder, codeforces, hackerearth

import httpx, asyncio, uvicorn



HTTPX_CLIENT = httpx.AsyncClient(timeout=300)


app = FastAPI()


platforms = "atcoder codeforces hackerearth".split()

welcomeMessage = """
This API is created by Nusab Taha.

For the docs, visit /docs endpoint.

More info at: https://github.com/Nusab19

Made using FastAPI with python3


""".strip()


@app.get("/")
async def index():
    return {"message": welcomeMessage, "ok": True}

@app.get("/platforms")
async def platformNames():
    return {"message": platforms, "ok": True}


@app.get("/all")
async def allPlatformContests():
    ses = HTTPX_CLIENT
    data = {"ok": True}
    try:
        data["atcoder"] = await atcoder.getContests(ses)
    except:
        data["ok"] = False
    
    try:
        data["codeforces"] = await codeforces.getContests(ses)
    except:
        data["ok"] = False
     
    try:
        data["hackerearth"] = await hackerearth.getContests(ses)
    except:
        data["ok"] = False
    
    return data


@app.get("/atcoder")
@app.get("/1")
async def atcoderContests():
    ses = HTTPX_CLIENT
    try:
        return await atcoder.getContests(ses)
    except Exception as e:
        return {"ok":False, "message":"Failed to fetch contests", "error":str(e)}



@app.get("/codeforces")
@app.get("/2")
async def codeforcesContests():
    ses = HTTPX_CLIENT.get("ses")
    try:
        return await codeforces.getContests(ses)
    except Exception as e:
        return {"ok":False, "message":"Failed to fetch contests", "error":str(e)}


@app.get("/hackerearth")
@app.get("/3")
async def hackerEarthContests():
    ses = HTTPX_CLIENT
    try:
        return await hackerearth.getContests(ses)
    except Exception as e:
        return {"ok":False, "message":"Failed to fetch contests", "error":str(e)}
    

if __name__ == "__main__":
    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=8080,
        reload=True
    )

    server = uvicorn.Server(config=config)
    server.run()

