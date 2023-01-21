from bs4 import BeautifulSoup
from datetime import datetime
import httpx
import asyncio


def extract_data(r):
    soup = BeautifulSoup(r.content, "html5lib")
    a = soup.findAll("div", attrs={"class": "flow"})

    allContests = []
    for i in a[::-1]:
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
        url = f"https://toph.co/{endpoint}"
        contest = {
            "name": name,
            "url": url,
            "startTime": startTime,
        }
        allContests.append(contest)
    return allContests


def extractTime(r):
    soup = BeautifulSoup(r.content, "html5lib")
    a = soup.find(
        "div", attrs={"class": "panel__body artifact"}).findAll("strong")

    # date, when, duration = [i.text for i in a]
    duration = a[-1].text
    return duration


async def getContests(ses: httpx.AsyncClient):
    r = await ses.get("https://toph.co/contests/all", follow_redirects=True)

    loop = asyncio.get_event_loop()
    allContests = await loop.run_in_executor(None, extract_data, r)
    urls = [i["url"] for i in allContests]

    url_data = await asyncio.gather(*[ses.get(i, follow_redirects=True) for i in urls])
    durations = [await loop.run_in_executor(None, extractTime, r) for r in url_data]
    for i, e in enumerate(durations):
        allContests[i]["duration"] = e

    return allContests
