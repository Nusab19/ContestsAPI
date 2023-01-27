import json
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, FileResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime


import time
import httpx
import asyncio
import uvicorn


# Local Assets
from platforms import atcoder, codechef, codeforces, hackerearth, toph


HTTPX_CLIENT = httpx.AsyncClient(timeout=300)


description = """
<h1>A simple asynchronous API made with FastAPI that gives you the contests' details from different platforms. 🚀</h1>

<h2>Made by: Nusab Taha ( @Nusab19 )</h2>

Website: <a href="https://nusab19.github.io">nusab19.github.io</a>
<br>
Email: <a href="mailto:nusabtaha33@gmail.com">Nusab Taha</a>

"""

app = FastAPI(
    title="Contests API",
    description=description,
    version="1.0",
    license_info={
        "name": "MIT license",
        "url": "https://github.com/Nusab19/ContestsAPI/blob/main/LICENSE.md",
    }
)

scheduler = AsyncIOScheduler()

cachedData = {}


keyword_platforms = {
    "1": "atcoder",
    "2": "codechef",
    "3": "codeforces",
    "4": "hackerearth",
    "5": "toph"
}


platform_funcs = {
    "1": atcoder.getContests,
    "2": codechef.getContests,
    "3": codeforces.getContests,
    "4": hackerearth.getContests,
    "5": toph.getContests
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

    data = {"ok": True, "message": welcomeMessage}
    return Response(content=json.dumps(data, indent=4, default=str), media_type='application/json')


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
    data = {
        "ok": True,
        "message": list(keyword_platforms.values()),
        "data": dict(keyword_platforms.items())}

    return Response(content=json.dumps(data, indent=4, default=str), media_type='application/json')


@app.get("/all")
async def allPlatformContests():
    data = {"ok": True}
    x = [i(HTTPX_CLIENT) for i in platform_funcs.values()]
    x = await asyncio.gather(*x)
    y = keyword_platforms.values()

    data.update(dict(zip(y, x)))

    try:
        return Response(content=json.dumps(data, indent=4, default=str), media_type='application/json')
    finally:
        del data["ok"]
        cachedData.update(data)


def formatError(e: Exception):
    return {
        "ok": False,
        "message": "Failed to fetch contests",
        "error": str(e)}


@app.get("/1")
@app.get("/atcoder")
async def atcoderContests():
    try:
        data = {"ok": True}
        x = await atcoder.getContests(HTTPX_CLIENT)
        data.update({"data": x})
        try:
            return Response(content=json.dumps(data, indent=4, default=str), media_type='application/json')
        finally:
            cachedData["atcoder"] = data

    except Exception as e:
        data = formatError(e)
        return Response(content=json.dumps(data, indent=4, default=str),
                        media_type='application/json')


@app.get("/2")
@app.get("/codechef")
async def codechefContests():
    try:
        data = {"ok": True}
        x = await codechef.getContests(HTTPX_CLIENT)
        data.update({"data": x})
        try:
            return Response(content=json.dumps(data, indent=4, default=str), media_type='application/json')
        finally:
            cachedData["codechef"] = data

    except Exception as e:
        data = formatError(e)
        return Response(content=json.dumps(data, indent=4, default=str),
                        media_type='application/json')


@app.get("/3")
@app.get("/codeforces")
async def codeforcesContests():
    try:
        data = {"ok": True}
        x = await codeforces.getContests(HTTPX_CLIENT)
        data.update({"data": x})
        try:
            return Response(content=json.dumps(data, indent=4, default=str), media_type='application/json')
        finally:
            cachedData["codeforces"] = data

    except Exception as e:
        data = formatError(e)
        return Response(content=json.dumps(data, indent=4, default=str),
                        media_type='application/json')


@app.get("/4")
@app.get("/hackerearth")
async def hackerEarthContests():
    try:
        data = {"ok": True}
        x = await hackerearth.getContests(HTTPX_CLIENT)
        data.update({"data": x})
        try:
            return Response(content=json.dumps(data, indent=4, default=str), media_type='application/json')
        finally:
            cachedData["hackerearth"] = data

    except Exception as e:
        data = formatError(e)
        return Response(content=json.dumps(data, indent=4, default=str),
                        media_type='application/json')


@app.get("/5")
@app.get("/toph")
async def tophContests():
    try:
        data = {"ok": True}
        x = await toph.getContests(HTTPX_CLIENT)
        data.update({"data": x})
        try:
            return Response(content=json.dumps(data, indent=4, default=str), media_type='application/json')
        finally:
            cachedData["toph"] = data

    except Exception as e:
        data = formatError(e)
        return Response(content=json.dumps(data, indent=4, default=str),
                        media_type='application/json')


@app.get("/cached/all")
async def all_cached():
    data = {"ok": True}
    data.update(cachedData.copy())
    return Response(content=json.dumps(data, indent=4, default=str), media_type='application/json')


@app.get("/cached/1")
@app.get("/cached/atcoder")
async def CachedAtcoderContests():
    data = {"ok": True, "data": cachedData.get("atcoder")}
    return Response(content=json.dumps(data, indent=4, default=str), media_type='application/json')


@app.get("/cached/2")
@app.get("/cached/codechef")
async def CachedCodechef():
    data = {"ok": True, "data": cachedData.get("codechef")}
    return Response(content=json.dumps(data, indent=4, default=str), media_type='application/json')


@app.get("/cached/3")
@app.get("/cached/codeforces")
async def CachedCodeforces():
    data = {"ok": True, "data": cachedData.get("codeforces")}
    return Response(content=json.dumps(data, indent=4, default=str), media_type='application/json')


@app.get("/cached/3")
@app.get("/cached/codeforces")
async def CachedCodeforces():
    data = {"ok": True, "data": cachedData.get("codeforces")}
    return Response(content=json.dumps(data, indent=4, default=str), media_type='application/json')


@app.get("/cached/4")
@app.get("/cached/hackerearth")
async def CachedHackerearth():
    data = {"ok": True, "data": cachedData.get("hackerearth")}
    return Response(content=json.dumps(data, indent=4, default=str), media_type='application/json')


@app.get("/cached/5")
@app.get("/cached/toph")
async def CachedToph():
    data = {"ok": True, "data": cachedData.get("toph")}
    return Response(content=json.dumps(data, indent=4, default=str), media_type='application/json')


# For some unknown reason (to me), the code below is having slow response problem.
# It should NOT take long. But it does. So, commenting it.
# And adding a lot of manual function declaration to make the response faster.
# :")

"""
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
        data = {"ok": True}
        x = await func(HTTPX_CLIENT)
        data.update({"data": x})
        try:
            return Response(content=json.dumps(data, indent=4, default=str), media_type='application/json')
        finally:
            del data["ok"]
            cachedData[platform] = data
    except Exception as e:
        data = formatError(e)
        return Response(content=json.dumps(data, indent=4, default=str),
                        media_type='application/json')

"""

# Just to get the overall status of the API

_tempData = {"count": 0, "startTime": time.time()}


@app.get("/status")
async def api_status():
    uptime = (time.time() - _tempData["startTime"])/3600
    reqCount = _tempData["count"]
    data = {
        "uptime": f"{uptime:.2f} hours.",
        "requestsCount": reqCount
    }
    return Response(content=json.dumps(data, indent=4, default=str), media_type='application/json')


@app.middleware("http")
async def add_process_time_header(request, func):
    response = await func(request)
    try:
        return response
    finally:
        _tempData["count"] += 1


if __name__ == "__main__":
    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=5000,
        reload=True
    )

    server = uvicorn.Server(config=config)
    server.run()
