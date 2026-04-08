from playwright.sync_api import sync_playwright
import subprocess, time, os

server = subprocess.Popen(
    ["python", "-m", "http.server", "4567", "--directory", "out"],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
time.sleep(2)

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Dark mode
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto("http://localhost:4567/docs.html", wait_until="networkidle")
        page.evaluate("document.documentElement.classList.add('dark')")
        page.wait_for_timeout(500)

        for scroll, name in [(0, "top"), (500, "why"), (900, "table"), (1500, "quick")]:
            page.evaluate(f"window.scrollTo(0, {scroll})")
            page.wait_for_timeout(200)
            page.screenshot(path=f"/tmp/v4_dark_{name}.png")
            print(f"dark {name}")
        page.close()

        # Light mode
        page2 = browser.new_page(viewport={"width": 1440, "height": 900})
        page2.goto("http://localhost:4567/docs.html", wait_until="networkidle")
        page2.evaluate("document.documentElement.classList.remove('dark')")
        page2.wait_for_timeout(500)

        for scroll, name in [(0, "top"), (900, "table")]:
            page2.evaluate(f"window.scrollTo(0, {scroll})")
            page2.wait_for_timeout(200)
            page2.screenshot(path=f"/tmp/v4_light_{name}.png")
            print(f"light {name}")
        page2.close()

        # Also check getting-started for inline code
        page3 = browser.new_page(viewport={"width": 1440, "height": 900})
        page3.goto("http://localhost:4567/docs/getting-started.html", wait_until="networkidle")
        page3.evaluate("document.documentElement.classList.add('dark')")
        page3.wait_for_timeout(500)
        page3.evaluate("window.scrollTo(0, 600)")
        page3.wait_for_timeout(200)
        page3.screenshot(path="/tmp/v4_dark_inline.png")
        print("dark inline code")
        page3.close()

        browser.close()
        print("Done.")
finally:
    server.terminate()
    server.wait()
