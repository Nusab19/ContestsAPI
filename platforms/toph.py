import httpx
import asyncio

from bs4 import BeautifulSoup
from datetime import datetime
try:
    from helpers.format_time import secondsToTime, timeToSeconds
except ImportError:
    from .helpers.format_time import secondsToTime, timeToSeconds


def extract_data(r):
    soup = BeautifulSoup(r.content, "html5lib")
    x = soup.findAll("div", attrs={"class": "flow"})

    allContests = []
    for i in x[::-1]:
        status = i.find("span", attrs={"class": "text"})
        anchor = i.find("a")
        name = anchor.text
        endpoint = anchor["href"]
        time = i.find("span", attrs={"class": "timestamp"})
        if not time:
            continue
        status = status.text
        if not status.startswith("in"):
            continue

        startSec = int(time["data-timestamp"])
        startTime = datetime.strftime(
            datetime.utcfromtimestamp(startSec),
            "%d-%m-%Y %H:%M:%S") + " UTC"
        url = f"https://toph.co{endpoint}"
        contest = {
            "name": name,
            "url": url,
            "startTime": startTime,
        }
        allContests.append(contest)
    return allContests


def extractTime(r):
    a = BeautifulSoup(
        r.content, "html5lib").find(
        "div", attrs={
            "class": "panel__body artifact"}).findAll("p")

    for s in a:
        if "will run for" in str(s).lower():
            duration = s.findAll("strong")[-1].text
            durationSec = timeToSeconds(duration)

            return (duration, durationSec)


async def getContests(ses: httpx.AsyncClient):
    r = await ses.get("https://toph.co/contests/all", follow_redirects=True)

    loop = asyncio.get_event_loop()
    allContests = await loop.run_in_executor(None, extract_data, r)
    urls = [i["url"] for i in allContests]

    url_data = await asyncio.gather(*[ses.get(i, follow_redirects=True) for i in urls])
    durations = [await loop.run_in_executor(None, extractTime, r) for r in url_data]
    for i, e in enumerate(durations):
        allContests[i]["duration"] = e[0]
        allContests[i]["durationSeconds"] = e[1]

    return allContests


if __name__ == "__main__":
    print("Only running one file.\n")
    p = asyncio.run(getContests(httpx.AsyncClient(timeout=13)))
    for j in p:
        print(j)
