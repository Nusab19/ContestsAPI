from fastapi import FastAPI

from platforms import atcoder, codeforces, hackerearth

import httpx, asyncio



HTTPX_CLIENT = {"ses":httpx.AsyncClient(timeout=300)}

async def changeSession():
    while 1:
        await HTTPX_CLIENT.get("ses").aclose()
        HTTPX_CLIENT["ses"] = httpx.AsyncClient(timeout=300)
        await asyncio.sleep(33*60) # 33 minutes interval

asyncio.create_task(changeSession())
    
    



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
    ses = HTTPX_CLIENT.get("ses")
    data = {"ok": True}
    try:
        data["atcoder"] = atcoder.getContests(ses)
    except:
        data["ok"] = False
    
    try:
        data["codeforces"] = codeforces.getContests(ses)
    except:
        data["ok"] = False
     
    try:
        data["hackerearth"] = hackerearth.getContests(ses)
    except:
        data["ok"] = False
    
    return data


@app.get("/atcoder")
@app.get("/1")
async def atcoderContests():
    ses = HTTPX_CLIENT.get("ses")
    try:
        return atcoder.getContests(ses)
    except Exception as e:
        return {"ok":False, "message":"Failed to fetch contests", "error":str(e)}



@app.get("/codeforces")
@app.get("/2")
async def codeforcesContests():
    ses = HTTPX_CLIENT.get("ses")
    try:
        return codeforces.getContests(ses)
    except Exception as e:
        return {"ok":False, "message":"Failed to fetch contests", "error":str(e)}


@app.get("/hackereaeth")
@app.get("/3")
async def hackerEarthContests():
    ses = HTTPX_CLIENT.get("ses")
    try:
        return hackerearth.getContests(ses)
    except Exception as e:
        return {"ok":False, "message":"Failed to fetch contests", "error":str(e)}
    
