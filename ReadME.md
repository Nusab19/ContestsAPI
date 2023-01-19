<h3 align="center">An <i>asynchronous</i> API made with FastAPI to grab contests' information from different platforms.</h3>

<h1>Available Platforms</h1>

<ol>
<li>Atcoder</li>
<li>Codeforces</li>
<li>HackerEarth</li>
</ol>

<p align="center">
<img height="100px" src="https://te.legra.ph/file/8f3c11d29137158c58e6a.png">
<img height="100px" src="https://te.legra.ph/file/fd1d40f90734a028a1e76.png">
<img height="100px" src="https://te.legra.ph/file/90ab43168f2152a1ea0e0.png">
</p>

<h1>Endpoints</h1>

<code>/docs</code> - Documentation.
<code>/platforms</code> - All available Platforms

<p>As this API needs to make http requests fetches data, there <i>will</i> be some delay. So, I made a solution for that.

<code>/cached</code> endpoint will give you instant response.</p>

<p>Every <b><i>7</i></b> minutes, it fetches data from all the platforms and stores it locally.</p>

<h4>It is highly recommended to use <code>/cached</code> endpoint. Use the direct endpoints if you feel the necessity.</h4>

The structure is like:

<code>example.api.com/cached/&lt;method&gt;</code> <br><br>

Example:

https://api.nusab.repl.co/cached/all
Just put the method's name after <code>/cached/</code>.


<h1>Direct Endpoints (methods):</h1>

<code>/all</code> - Contests from all Platforms

<b>Note:</b> The response will be very slow as this method makes http requests to all the platforms. Use <code>/cached/all</code> instead.

<code>/atcoder</code> or <code>/1</code> - Contests of <b>Atcoder</b>

<code>/codeforces</code> or <code>/2</code> - Contests of <b>Codeforces</b>

<code>/hackerearth</code> or <code>/3</code> - Contests of <b>HackerEarth</b>

<p>Live API: https://api.nusab.repl.co</p>
<h1>Installation</h1>


  <pre>git clone https://github.com/Nusab19/ContestsAPI
cd ContestsAPI
pip install -r requirements.txt
python main.py</pre>