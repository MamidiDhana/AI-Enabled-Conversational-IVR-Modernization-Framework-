import argparse
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


def timed_request(url: str, payload: dict, timeout: float) -> tuple[bool, float]:
    start = time.perf_counter()
    try:
        resp = requests.post(url, json=payload, timeout=timeout)
        ok = resp.status_code == 200
    except Exception:
        ok = False
    elapsed_ms = (time.perf_counter() - start) * 1000
    return ok, elapsed_ms


def run_load(base_url: str, total_requests: int, concurrency: int, timeout: float) -> None:
    endpoint = f"{base_url.rstrip('/')}/ai/message"
    payload = {"message": "doctor availability", "session_id": "perf-seed"}

    latencies = []
    success = 0

    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = [
            pool.submit(timed_request, endpoint, payload, timeout)
            for _ in range(total_requests)
        ]
        for fut in as_completed(futures):
            ok, latency = fut.result()
            latencies.append(latency)
            if ok:
                success += 1

    failed = total_requests - success
    sorted_latencies = sorted(latencies)
    p95_index = max(0, int(0.95 * len(sorted_latencies)) - 1)

    print("=== Performance Test Result ===")
    print(f"Endpoint: {endpoint}")
    print(f"Total requests: {total_requests}")
    print(f"Concurrency: {concurrency}")
    print(f"Success: {success}")
    print(f"Failed: {failed}")
    print(f"Success rate: {(success / total_requests) * 100:.2f}%")
    print(f"Average latency: {statistics.mean(latencies):.2f} ms")
    print(f"Min latency: {min(latencies):.2f} ms")
    print(f"Max latency: {max(latencies):.2f} ms")
    print(f"P95 latency: {sorted_latencies[p95_index]:.2f} ms")


def main() -> None:
    parser = argparse.ArgumentParser(description="Load test for Conversational IVR backend")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--requests", type=int, default=200)
    parser.add_argument("--concurrency", type=int, default=20)
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args()

    run_load(
        base_url=args.base_url,
        total_requests=args.requests,
        concurrency=args.concurrency,
        timeout=args.timeout,
    )


if __name__ == "__main__":
    main()
