import json
import pytz
import httpx
import asyncio

from datetime import datetime
try:
    from helpers.format_time import secondsToTime, timeToSeconds
except ImportError:
    from .helpers.format_time import secondsToTime, timeToSeconds


async def getContests(ses: httpx.AsyncClient):
    r = await ses.get(
        "https://www.hackerearth.com/chrome-extension/events/")
    allContests = []
    if r.status_code == 200:
        jr = json.loads(r.text)
        contests = jr.get("response")
        for con in contests:
            plat = "HackerEarth"
            if con["status"] == "UPCOMING":
                name = con["title"]
                url = con["url"]
                start = con["start_tz"][: con["start_tz"].rindex(
                    ':')] + con["start_tz"][con["start_tz"].rindex(':') + 1:]
                start = start.replace(" ", "T")
                end = con["end_tz"].replace(" ", "T")
                try:
                    startTime = datetime.strptime(
                        start, '%Y-%m-%dT%H:%M:%S%z').astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S%z')
                    td = datetime.strptime(
                        end, '%Y-%m-%dT%H:%M:%S%z') - datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
                    durationSec = int(td.total_seconds())
                    duration = secondsToTime(durationSec)

                    startTime = datetime.strptime(startTime.replace(
                        'T', ' ')[:-5], "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y %H:%M:%S UTC")

                    contest = {
                        "name": name,
                        "url": url,
                        "startTime": startTime,
                        "duration": duration,
                        "durationSeconds": durationSec
                    }

                    allContests.append(contest)

                except Exception as e:
                    print(e)
                    continue

    return allContests


if __name__ == "__main__":
    print("Only running one file.\n")
    a = asyncio.run(getContests(httpx.AsyncClient(timeout=13)))
    for j in a:
        print(j)
