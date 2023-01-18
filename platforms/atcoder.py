from bs4 import BeautifulSoup
import httpx
from datetime import datetime
from pytz import timezone


async def getContests(ses: httpx.AsyncClient):
    r = await ses.get("https://atcoder.jp/contests/")
    allContests = []
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html5lib")
        contests = soup.select("#contest-table-upcoming tbody tr")

        for con in contests:
            ele = con.find_all("td")
            plat = "AtCoder"

            contestName = ele[1].text.strip()[
                ele[1].text.strip().index("\n") + 1:]

            url = "https://atcoder.jp" + ele[1].select("a")[0].get("href")

            startTime = datetime.strptime(
                ele[0].text.replace(
                    " ", "T"), '%Y-%m-%dT%H:%M:%S%z').astimezone(
                timezone('Asia/Kolkata')).strftime('%Y-%m-%dT%H:%M:%S%z')

            duration = ele[2].text + " hours."

            contest = {
                "contestName": contestName,
                "contestUrl": url,
                "startTime": startTime,
                "duration": duration
            }

            allContests.append(contest)
    return allContests
