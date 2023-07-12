import httpx, time


ses = httpx.Client(timeout=30, follow_redirects=1)
while 1:
    try:
        r = ses.get("https://contestsapi.onrender.com/status")
        print("Self Check:", r.status_code, end="\r")
        time.sleep(10)
    except:pass