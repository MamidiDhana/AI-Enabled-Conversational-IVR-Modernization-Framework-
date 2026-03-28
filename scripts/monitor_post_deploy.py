import argparse
import datetime as dt
import time

import requests


def monitor(base_url: str, interval_sec: int, max_checks: int, latency_threshold_ms: float) -> None:
    url = f"{base_url.rstrip('/')}/"
    failures = 0
    alerts = 0

    print("=== Post-Deployment Monitor Started ===")
    print(f"Health endpoint: {url}")

    for check_num in range(1, max_checks + 1):
        now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start = time.perf_counter()
        try:
            resp = requests.get(url, timeout=5)
            elapsed_ms = (time.perf_counter() - start) * 1000
            healthy = resp.status_code == 200
        except Exception:
            elapsed_ms = (time.perf_counter() - start) * 1000
            healthy = False

        if not healthy:
            failures += 1
            print(f"[{now}] Check {check_num}: FAIL | latency={elapsed_ms:.2f} ms")
        else:
            status = "OK"
            if elapsed_ms > latency_threshold_ms:
                alerts += 1
                status = "SLOW"
            print(f"[{now}] Check {check_num}: {status} | latency={elapsed_ms:.2f} ms")

        if check_num < max_checks:
            time.sleep(interval_sec)

    print("=== Post-Deployment Monitor Summary ===")
    print(f"Total checks: {max_checks}")
    print(f"Failures: {failures}")
    print(f"Latency alerts: {alerts}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Monitor IVR service after deployment")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--interval", type=int, default=10, help="Seconds between checks")
    parser.add_argument("--checks", type=int, default=30, help="Number of checks")
    parser.add_argument("--latency-threshold", type=float, default=300.0)
    args = parser.parse_args()

    monitor(
        base_url=args.base_url,
        interval_sec=args.interval,
        max_checks=args.checks,
        latency_threshold_ms=args.latency_threshold,
    )


if __name__ == "__main__":
    main()
