import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path


RAW_DIR = Path("storage/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

RAW_FILE = RAW_DIR / "events.jsonl"


class SyslogProtocol(asyncio.DatagramProtocol):

    def datagram_received(self, data, addr):
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_ip": addr[0],
            "source_port": addr[1],
            "protocol": "UDP_SYSLOG", 
            "raw": data.decode("utf-8", errors="replace")
        }

        with RAW_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event, ensure_ascii=False) + "\n")

        print(f"[SYSLOG] Event received from {addr[0]}")


async def main():
    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        SyslogProtocol,
        local_addr=("0.0.0.0", 5140)
    )

    print("[SYSLOG] Listening on UDP port 5140")

    try:
        await asyncio.Future()
    finally:
        transport.close()


if __name__ == "__main__":
    asyncio.run(main())
