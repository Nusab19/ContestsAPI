import pytz
import httpx
import asyncio

from bs4 import BeautifulSoup
from datetime import datetime
try:
    from helpers.format_time import secondsToTime, timeToSeconds
except ImportError:
    from .helpers.format_time import secondsToTime, timeToSeconds


def extract_data(r):
    soup = BeautifulSoup(r, "lxml")
    return soup.select("#contest-table-upcoming tbody tr")


async def getContests(ses: httpx.AsyncClient):
    r = await ses.get("https://atcoder.jp/contests/")
    allContests = []
    loop = asyncio.get_event_loop()
    if r.status_code == 200:
        contests = await loop.run_in_executor(None, extract_data, r.content)

        for con in contests:
            ele = con.find_all("td")
            name = " ".join(
                ele[1].text.strip()[
                    ele[1].text.strip().index("\n") +
                    1:].strip().split()[
                    1:])

            url = "https://atcoder.jp" + ele[1].select("a")[0].get("href")

            startTime = datetime.strptime(
                ele[0].text.replace(
                    " ", "T"), '%Y-%m-%dT%H:%M:%S%z').astimezone(
                pytz.utc).strftime("%d-%m-%Y %H:%M:%S") + " UTC"

            h, m = ele[2].text.split(':')
            durationSec = int(h) * 3600 + int(m) * 60
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
