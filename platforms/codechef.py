import pytz
import httpx
import asyncio

from datetime import datetime
try:
    from helpers.format_time import secondsToTime, timeToSeconds
except ImportError:
    from .helpers.format_time import secondsToTime, timeToSeconds


async def getContests(ses: httpx.AsyncClient):
    r = (await ses.get('https://www.codechef.com/api/list/contests/all')).json()

    if r.get("status") != "success":
        return []

    allContests = []
    contests = r["future_contests"]

    for i in contests:
        name = i["contest_name"]
        url = f"https://www.codechef.com/{i['contest_code']}"
        startIso = i["contest_start_date_iso"]
        startTime = datetime.fromisoformat(startIso).astimezone(
            pytz.utc).strftime("%d-%m-%Y %H:%M:%S UTC")
        durationMin = i["contest_duration"] + " minutes"
        durationSec = timeToSeconds(durationMin)
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
