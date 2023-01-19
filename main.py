
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler


# Local Helpers
from platforms import atcoder, codeforces, hackerearth

import httpx
import asyncio
import uvicorn


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
    cachedData["atcoder"] = await atcoder.getContests(HTTPX_CLIENT)

    cachedData["codeforces"] = await codeforces.getContests(HTTPX_CLIENT)

    cachedData["hackerearth"] = await hackerearth.getContests(HTTPX_CLIENT)
    print("Cached")


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

    except BaseException:
        data["ok"] = False

    try:
        data["codeforces"] = await codeforces.getContests(ses)
    except BaseException:
        data["ok"] = False

    try:
        data["hackerearth"] = await hackerearth.getContests(ses)
    except BaseException:
        data["ok"] = False

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
    cachedData.update({"ok": True})
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
