import pytz
import httpx
import asyncio

from datetime import datetime
try:
    from helpers.format_time import secondsToTime, timeToSeconds
except ImportError:
    from .helpers.format_time import secondsToTime, timeToSeconds


async def getContests(ses: httpx.AsyncClient):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}
    r = (await ses.get("https://www.hackerrank.com/rest/contests/upcoming", headers=headers)).json()
    contests = [i for i in r["models"] if i["ended"]
                == False and i["started"] == False]
    allContests = []

    for i in contests:
        name = i["name"]
        url = f"" + i["slug"]
        startIso = i["get_starttimeiso"]
        endIso = i["get_endtimeiso"]
        startTime = datetime.fromisoformat(startIso).astimezone(
            pytz.utc).strftime("%d-%m-%Y %H:%M:%S UTC")
        durationSec = int((datetime.fromisoformat(endIso).astimezone(
            pytz.utc) - datetime.fromisoformat(startIso).astimezone(
            pytz.utc)).total_seconds())

        duration = secondsToTime(durationSec)
        contest = {
            "name": name,
            "url": url,
            "startTime": startTime,
            "duration": duration,
            "durationSeconds": durationSec
        }

        allContests.append(contest)

    return allContests


if __name__ == "__main__":
    print("Only running one file.\n")
    a = asyncio.run(getContests(httpx.AsyncClient(timeout=13)))
    for j in a:
        print(j)
