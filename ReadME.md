<h3 align="center">An <i>asynchronous</i> API made with FastAPI to grab contests' information from different platforms.</h3>

<p align="center">
<img height="300px" src="https://te.legra.ph/file/46a2556c0bb2e9ad90e94.jpg">
</p>

<a target="_blank" href="https://github.com/Nusab19/ContestsAPI"><img src="https://img.shields.io/github/stars/Nusab19/ContestsAPI"/></a>
<a target="_blank" href="https://github.com/Nusab19/ContestsAPI"><img src="https://img.shields.io/github/last-commit/Nusab19/ContestsAPI" />
</a>


<h1>Available Platforms</h1>

<ol>
<li>Atcoder</li>
<li>CodeChef</li>
<li>Codeforces</li>
<li>HackerEarth</li>
</ol>

<p align="center">
<img height="100px" src="https://te.legra.ph/file/8f3c11d29137158c58e6a.png">
<img height="100px" src="https://te.legra.ph/file/fd1d40f90734a028a1e76.png">
<br>
<img height="100px" src="https://telegra.ph/file/bf1b768d37b0d2dabb049.png">
<img height="100px" src="https://te.legra.ph/file/90ab43168f2152a1ea0e0.png">

</p>


<h1>Endpoints</h1>

<code>/docs</code> - Documentation.

<b>Note</b>: All responses are in <i>json</i> and beautified.

<code>/platforms</code> - All available Platforms

<p>As this API needs to make http requests fetches data, there <i>will</i> be some delay. So, I made a solution for that.

<code>/cached</code> endpoint will give you instant response.</p>

<p>Every <b><i>7</i></b> minutes, it fetches data from all the platforms and stores it locally.</p>

<h4>It is highly recommended to use <code>/cached</code> endpoint. Use the direct endpoints if you feel the necessity.</h4>

The structure is like:

<code>example.api.com/cached/&lt;method&gt;</code> <br><br>

Example:

https://api.nusab.repl.co/cached/2

Response:
<pre>
[
    {
        "name": "Starters 79",
        "contestUrl": "https://www.codechef.com/START79",
        "startTime": "2023-02-22 02:30:00 UTC",
        "duration": "3 hours."
    },
    {
        "name": "Starters 78",
        "contestUrl": "https://www.codechef.com/START78",
        "startTime": "2023-02-15 02:30:00 UTC",
        "duration": "3 hours."
    }
]
</pre>


Just put the method's name after <code>/cached/</code>.



<h1>Direct Endpoints (methods):</h1>

<code>/all</code> - Contests from all Platforms

<b>Note:</b> The response will be very slow as this method makes http requests to all the platforms. Use <code>/cached/all</code> instead.

<code>/atcoder</code> or <code>/1</code> - Contests of <b>Atcoder</b>

<code>/codeforces</code> or <code>/2</code> - Contests of <b>Codeforces</b>

<code>/codechef</code> or <code>/3</code> - Contests of <b>CodeChef</b>
<code>/hackerearth</code> or <code>/4</code> - Contests of <b>HackerEarth</b>

<p>Live API: https://api.nusab.repl.co</p>

<h1>Installation</h1>


```
git clone https://github.com/Nusab19/ContestsAPI
cd ContestsAPI
pip install -r requirements.txt
python main.py
```

Visit <code>localhost:5000</code> after running.
