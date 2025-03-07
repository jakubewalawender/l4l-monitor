import asyncio

from monitor.luxuryforless_monitor import LuxuryForLessMonitor

if __name__ == "__main__":
    monitor = LuxuryForLessMonitor()
    asyncio.run(monitor.check_for_updates())
