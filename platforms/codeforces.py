import httpx
import json
from datetime import datetime


async def getContests(ses: httpx.AsyncClient):
    r = await ses.get("https://codeforces.com/api/contest.list")
    allContests = []

    if r.status_code == 200:
        jr = json.loads(r.text)
        contests = jr.get("result")
        for con in contests:
            if con.get("phase") == "BEFORE":
                plat = "CodeForces"
                name = con["name"]
                url = "https://codeforces.com/contests/" + str(con["id"])
                startSec = con["startTimeSeconds"]
                startTime = datetime.strftime(
                    datetime.utcfromtimestamp(startSec),
                    "%d-%m-%Y %H:%M:%S") + " UTC"

                duration = f"0{con.get('durationSeconds') // 3600 }:00 hours."
                contest = {
                    "name": name,
                    "contestUrl": url,
                    "startTime": startTime,
                    "duration": duration
                }
                allContests.append(contest)

    return allContests
