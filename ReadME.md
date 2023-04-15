<h3 align="center">A <b>totally</b> <i>asynchronous</i> API made with FastAPI and WebScrapping to grab upcoming contests' information from different platforms.</h3>

<p align="center">
<img height="300px" src="https://te.legra.ph/file/46a2556c0bb2e9ad90e94.jpg">
</p>

<a target="_blank" href="https://github.com/Nusab19/ContestsAPI"><img src="https://img.shields.io/github/stars/Nusab19/ContestsAPI"/></a>
<a target="_blank" href="https://github.com/Nusab19/ContestsAPI"><img src="https://img.shields.io/github/last-commit/Nusab19/ContestsAPI" />
</a>

<h1>Warning</h1>
<p>
<b>If you want to use this API in production, it is highly recommended to <i>fork</i> this repository.</b>
<br>
Beacause I am adding new platforms regularly and code is improving continuously.
<br>
There will come new versions of this API soon. <b>(After May 23, 2023)</b>
<br>
So, fork this repo so your project doesn't get hampered by new changes.
</p>

<h1>7 Available Platforms</h1>

<ol>
<li>Atcoder</li>
<li>CodeChef</li>
<li>Codeforces</li>
<li>HackerEarth</li>
<li>HackerRank</li>
<li>LeetCode</li>
<li>Toph</li>
</ol>

<p align="center">
<img height="300px" src="https://te.legra.ph/file/1b5b3f8fe4da2fca9f223.jpg">
<br>
</p>


<h1>Endpoints</h1>

<code>/docs</code> - Documentation.

<b>Note</b>: All responses are in <b>pretty <i>JSON</i></b> format.

<code>/platforms</code> - All available Platforms

<p>As this API needs to make http requests fetches data, there <i>will</i> be some delay. So, I made a solution for that.

<code>/cached</code> endpoint will give you instant response.</p>

<p>Every <b><i>7</i></b> minutes, it fetches data from all the platforms and stores it locally.</p>

<h4>It is highly recommended to use <code>/cached</code> endpoint. Use the direct endpoints if you feel the necessity.</h4>

The structure is like:

<code>example.api.com/cached/&lt;method&gt;</code> <br><br>

Example:

https://contestsapi.onrender.com/cached/2   <code> 2 == codechef</code>

See <code>/platforms</code> for numeric names of each platform.

Sample Response:
<pre>
{
    "ok": true,
    "data": [
        {
            "name": "Starters 78",
            "url": "https://www.codechef.com/START78",
            "startTime": "22-02-2023 14:30:00 UTC",
            "duration": "3 hours",
            "durationSeconds": 10800
        },
        {
            "name": "Starters 79",
            "url": "https://www.codechef.com/START79",
            "startTime": "01-03-2023 14:30:00 UTC",
            "duration": "3 hours",
            "durationSeconds": 10800
        }
    ]
}
</pre>


Just put the method's name after <code>/cached/</code>.



<h1>Direct Endpoints (methods):</h1>

<code>/all</code> - Contests from all Platforms

<b>Note:</b> The response will be very slow as this method makes http requests to all the platforms. Use <code>/cached/all</code> instead.

<code>/atcoder</code> or <code>/1</code> - Contests of <b>Atcoder</b>

<code>/codeforces</code> or <code>/2</code> - Contests of <b>Codeforces</b>

<code>/codechef</code> or <code>/3</code> - Contests of <b>CodeChef</b>

<code>/hackerearth</code> or <code>/4</code> - Contests of <b>HackerEarth</b>

<code>/toph</code> or <code>/5</code> - Contests of <b>Toph</b>

<code>/status</code> - A brief status of the API. 

<br>
<h2>Live API</h2>
<a href=""https://contestsapi.onrender.com/>contestsapi.onrender.com</a>

<h1>Installation</h1>

```
git clone https://github.com/Nusab19/ContestsAPI
cd ContestsAPI
pip install -r requirements.txt
python main.py
```

You may also use <code>uvicorn main:app --reload --port 5000 --host 0.0.0.0</code> instead of <code>python main.py</code>

Visit <code>localhost:5000</code> after running locally.

Make sure to give a star if you like it! :D

Made with ❤ and effort by <a href="https://github.com/Nusab19">@Nusab19</a>
