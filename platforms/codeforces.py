import json
import httpx
import asyncio

from datetime import datetime
try:
    from helpers.format_time import secondsToTime, timeToSeconds
except ImportError:
    from .helpers.format_time import secondsToTime, timeToSeconds


async def getContests(ses: httpx.AsyncClient):
    r = await ses.get("https://codeforces.com/api/contest.list")
    allContests = []

    if r.status_code == 200:
        jr = json.loads(r.text)
        contests = jr.get("result")
        for con in contests:
            if con.get("phase") == "BEFORE":
                name = con["name"]
                url = "https://codeforces.com/contests/" + str(con["id"])
                startSec = con["startTimeSeconds"]
                startTime = datetime.strftime(
                    datetime.utcfromtimestamp(startSec),
                    "%d-%m-%Y %H:%M:%S UTC")

                durationSec = con.get('durationSeconds')
                duration = secondsToTime(durationSec)
                contest = {
                    "name": name,
                    "url": url,
                    "startTime": startTime,
                    "duration": duration,
                    "durationSeconds": durationSec
                }
                allContests.append(contest)

    return allContests[::-1]


if __name__ == "__main__":
    print("Only running one file.\n")
    a = asyncio.run(getContests(httpx.AsyncClient(timeout=13)))
    for j in a:
        print(j)
