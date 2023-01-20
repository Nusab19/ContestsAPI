from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime


import httpx
import asyncio
import uvicorn


# Local Assets
from platforms import atcoder, codeforces, hackerearth


HTTPX_CLIENT = httpx.AsyncClient(timeout=300)


app = FastAPI()

scheduler = AsyncIOScheduler()

cachedData = {}


keyword_platforms = {
    "1": "atcoder",
    "2": "codeforces",
    "3": "hackerearth"
}


platform_funcs = {
    "1": atcoder.getContests,
    "2": codeforces.getContests,
    "3": hackerearth.getContests
}


@app.on_event("startup")
async def fx():
    await cacheOnStart()
    scheduler.add_job(cacheOnStart, 'interval', seconds=7 * 60)
    scheduler.start()


async def cacheOnStart():
    x = [i(HTTPX_CLIENT) for i in platform_funcs.values()]
    x = await asyncio.gather(*x)
    y = keyword_platforms.values()

    cachedData.update(dict(zip(y, x)))

    print(f"Cached Data at {datetime.now()}")


# Index / root
@app.get("/")
async def index():
    welcomeMessage = """
This API is created by Nusab Taha.

For the docs, visit /docs endpoint.

More info at: https://github.com/Nusab19

Made using FastAPI with python3

""".strip()

    return {"message": welcomeMessage, "ok": True}


# 404 Exception
@app.exception_handler(404)
async def custom_404_handler(*_):
    say = {"ok": False, "message": " Invalid Endpoint.\nWebPage not found 404"}
    return JSONResponse(status_code=404, content=say)


# favicon.ico
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("Images/favicon.ico")


# Platform Names
@app.get("/platforms")
async def platformNames():
    return {
        "message": keyword_platforms.values(),
        "ok": True,
        "data": keyword_platforms.items()}


@app.get("/all")
async def allPlatformContests():
    data = {"ok": True}
    x = [i(HTTPX_CLIENT) for i in platform_funcs.values()]
    x = await asyncio.gather(*x)
    y = keyword_platforms.values()

    data.update(dict(zip(y, x)))

    try:
        return data
    finally:
        del data["ok"]
        cachedData.update(data)


@app.get("/atcoder")
@app.get("/1")
async def atcoderContests():
    try:
        data = await atcoder.getContests(HTTPX_CLIENT)
        try:
            return data
        finally:
            cachedData["atcoder"] = data

    except Exception as e:
        return {
            "ok": False,
            "message": "Failed to fetch contests",
            "error": str(e)}


@app.get("/codeforces")
@app.get("/2")
async def codeforcesContests():
    try:
        data = await codeforces.getContests(HTTPX_CLIENT)
        try:
            return data
        finally:
            cachedData["codeforces"] = data

    except Exception as e:
        return {
            "ok": False,
            "message": "Failed to fetch contests",
            "error": str(e)}


@app.get("/hackerearth")
@app.get("/3")
async def hackerEarthContests():
    try:
        data = await hackerearth.getContests(HTTPX_CLIENT)
        try:
            return data
        finally:
            cachedData["hackerearth"] = data

    except Exception as e:
        return {
            "ok": False,
            "message": "Failed to fetch contests",
            "error": str(e)}


@app.get("/cached/all")
async def all_cached():
    data = cachedData.copy()
    data.update({"ok": True})
    return cachedData


@app.get("/cached/{platform}")
async def cached_result(platform: str):
    if platform in keyword_platforms:
        platform = keyword_platforms.get(platform)

    if platform not in keyword_platforms.values():
        return {
            "ok": False,
            "message": f"`{platform}` is not in the available platform list.\nCheck the spelling or visit github.com/Nusab19/ContestsAPI"}

    platform_id = {j: i for (i, j) in keyword_platforms.items()}.get(platform)

    func = platform_funcs.get(platform_id)

    try:
        data = await func(HTTPX_CLIENT)
        cachedData[platform] = data
        return data
    except Exception as e:
        return {
            "ok": False,
            "message": "Failed to fetch contests",
            "error": str(e)}


if __name__ == "__main__":
    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=8080,
        reload=True
    )

    server = uvicorn.Server(config=config)
    server.run()
