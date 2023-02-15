import asyncio
import httpx
import json

from datetime import datetime
try:
    from helpers.format_time import secondsToTime, timeToSeconds
except ImportError:
    from .helpers.format_time import secondsToTime, timeToSeconds


async def getContests(ses: httpx.AsyncClient):
    # Codechef gives access to their API to limited users
    # Had to use this API as web-scrapping didn't work in CodeChef either
    # They need to run js to ensure their Webpage
    # But I'll fetch the js file and figure out the hidden API soon... :3
    # For now, this is the alternative
    r = await ses.get("https://kontests.net/api/v1/code_chef")
    allContests = []

    if r.status_code == 200:
        contests = json.loads(r.text)
        for con in contests:
            name = con["name"]
            url = con["url"]
            startTime = con["start_time"]
            startTime = datetime.strptime(
                startTime, "%Y-%m-%d %H:%M:%S %Z").strftime("%d-%m-%y %H:%M:%S %Z") + "UTC"

            durationSec = int(con['duration'])
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
