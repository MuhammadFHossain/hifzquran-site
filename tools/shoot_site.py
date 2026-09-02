#!/usr/bin/env python3
"""Photographs the site with headless Chrome over the DevTools protocol.
usage: shoot_site.py <outdir> <spec>... where spec = name|url|width|height|mobile|y0,y1,...
"""
import sys, os, json, time, base64, subprocess, urllib.request
from websocket import create_connection

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9333
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
prof = os.path.join(out, "cdp-profile")
proc = subprocess.Popen([CHROME, "--headless=new", "--no-first-run", "--disable-gpu", "--hide-scrollbars",
                         f"--remote-debugging-port={PORT}", f"--user-data-dir={prof}", "--window-size=1440,900", "about:blank"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(50):
        try:
            tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json")); break
        except Exception: time.sleep(0.2)
    page = [t for t in tabs if t["type"] == "page"][0]
    ws = create_connection(page["webSocketDebuggerUrl"], suppress_origin=True)
    mid = [0]
    def send(method, **params):
        mid[0] += 1
        ws.send(json.dumps({"id": mid[0], "method": method, "params": params}))
        while True:
            r = json.loads(ws.recv())
            if r.get("id") == mid[0]:
                if "error" in r: raise RuntimeError(r["error"])
                return r.get("result", {})
    send("Page.enable"); send("Runtime.enable")
    for spec in sys.argv[2:]:
        name, url, w, h, mobile, ys = spec.split("|")
        w, h = int(w), int(h); mobile = mobile == "1"
        send("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=2 if mobile else 1, mobile=mobile)
        if mobile: send("Emulation.setTouchEmulationEnabled", enabled=True)
        send("Page.navigate", url=url)
        time.sleep(3.0)
        for y in ys.split(","):
            send("Runtime.evaluate", expression=f"window.scrollTo({{top:{int(y)}, left:0, behavior:'instant'}})")
            time.sleep(1.4)  # long enough for the reveal to finish
            shot = send("Page.captureScreenshot", format="png")
            path = os.path.join(out, f"{name}-{int(y):05d}.png")
            open(path, "wb").write(base64.b64decode(shot["data"]))
            print(f"{path} {os.path.getsize(path)//1024} KB")
        hgt = send("Runtime.evaluate", expression="document.documentElement.scrollHeight")["result"]["value"]
        print(f"  {name}: page height {hgt}")
    ws.close()
finally:
    proc.terminate()
