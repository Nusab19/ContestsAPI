import httpx
import json
import pytz
from datetime import datetime


async def getContests(ses: httpx.AsyncClient, limit: int = None):
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
                    if td.days and td.seconds:
                        duration = f" {td.days} Days & {td.seconds//3600} hours."
                    elif td.days:
                        duration = f"{td.days} Days"
                    elif td.seconds and td.seconds > 3600:
                        hours = ""
                        mins = ""
                        if (td.seconds) // 3600 < 10:
                            hours = "0" + str((td.seconds) // 3600)

                        else:
                            hours = td.seconds // 3600

                        if (td.seconds // 60) % 60 < 10:
                            mins = "0" + str((td.seconds // 60) % 60)
                        else:
                            mins = (td.seconds // 60) % 60
                        duration = f"{hours} : {mins} hours."

                    startTime = startTime.replace('T', ' ')[:-5] + " UTC"

                    contest = {
                        "name": name,
                        "url": url,
                        "startTime": startTime,
                        "duration": duration.strip()
                    }

                    if contest.get("duration"):
                        allContests.append(contest)

                except Exception as e:
                    print(e)
                    continue

    return allContests
