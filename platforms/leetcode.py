import asyncio
import httpx
import json

from bs4 import BeautifulSoup
from datetime import datetime
try:
    from helpers.format_time import secondsToTime, timeToSeconds
except ImportError:
    from .helpers.format_time import secondsToTime, timeToSeconds


def extract_data(r):
    # use `lxml` instead of `html.parser`
    soup = BeautifulSoup(r, "html.parser")
    # I used `html5lib` for its wide range of device support.

    a = soup.find("script", id="__NEXT_DATA__")
    data = json.loads(a.text)[
        "props"]["pageProps"]["dehydratedState"]["queries"][-1]["state"]["data"]["topTwoContests"]

    return data


async def getContests(ses: httpx.AsyncClient):
    r = (await ses.get("https://leetcode.com/contest/"))

    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, extract_data, r.text)

    allContests = []

    for i in data:
        name = i["title"]
        url = "https://leetcode.com/contest/" + i["titleSlug"]

        startSec = i["startTime"]
        startTime = datetime.strftime(
            datetime.utcfromtimestamp(startSec),
            "%d-%m-%Y %H:%M:%S") + " UTC"
        durationSec = i["duration"]
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
