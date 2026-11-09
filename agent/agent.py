import argparse
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def send_event(server_url, data):
    request = Request(
        server_url,
        data=data,
        headers={"Content-Type": "application/octet-stream"},
        method="POST"
    )

    with urlopen(request, timeout=10) as response:
        return 200 <= response.status < 300
def main():
    parser = argparse.ArgumentParser(
        description="Collector File Agent"
    )

    parser.add_argument(
        "--file",
        required=True,
        help="Path to log file"
    )

    parser.add_argument(
        "--server",
        default="http://127.0.0.1:8000/ingest"
    )
parser.add_argument(
        "--interval",
        type=float,
        default=2
    )

    args = parser.parse_args()

    log_file = Path(args.file)
    checkpoint = Path(str(log_file) + ".offset")

    if not log_file.is_file():
        print(f"[ERROR] Log file not found: {log_file}")
        return
       offset = 0

    if checkpoint.exists():
        try:
            offset = int(checkpoint.read_text().strip())
        except ValueError:
            offset = 0

    print("[AGENT] Collector Agent started")
    print(f"[AGENT] Watching: {log_file}")
    print(f"[AGENT] Server: {args.server}")

    while True:
        try:
            with log_file.open("rb") as file:
                file.seek(offset)
               while True:
                    line = file.readline()

                    if not line:
                        break

                    new_offset = file.tell()

                    try:
                        send_event(args.server, line)
                        offset = new_offset
                        checkpoint.write_text(str(offset))

                        print("[AGENT] Event sent successfully")

                    except (HTTPError, URLError, TimeoutError) as error:
                        print(f"[ERROR] Sending failed: {error}")
                        break
                      except OSError as error:
            print(f"[ERROR] File read failed: {error}")

        time.sleep(args.interval)


if __name__ == "__main__":
    main()
