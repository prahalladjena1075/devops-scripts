import sys
import time
import urllib.request
import urllib.error
from datetime import datetime

LOG_FILE = "health.log"


def check_app(url, timeout=5):
    """Return (status, detail). status is 'UP' or 'DOWN'."""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            code = response.status
            if 200 <= code < 400:
                return "UP", f"HTTP {code}"
            return "DOWN", f"HTTP {code}"
    except urllib.error.HTTPError as e:      # 4xx and 5xx errors
        return "DOWN", f"HTTP {e.code}"
    except urllib.error.URLError as e:       # app is off or wrong address
        return "DOWN", f"Connection failed: {e.reason}"
    except Exception as e:                   # timeout or anything else
        return "DOWN", f"Error: {e}"


def write_log(message):
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python health_checker.py <url> [interval_seconds]")
        sys.exit(1)

    url = sys.argv[1]
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    while True:
        status, detail = check_app(url)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{now}] {url} is {status} ({detail})"
        print(message)
        write_log(message)

        if interval == 0:
            sys.exit(0 if status == "UP" else 1)
        time.sleep(interval)


if __name__ == "__main__":
    main()