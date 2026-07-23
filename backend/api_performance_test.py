import requests
import time
import statistics
import concurrent.futures

API_URL = "http://127.0.0.1:8000/api/analyze"
PAYLOAD = {"text": "teri toh main goli maar dunga raste pe tu chutiya hai"}
HEADERS = {"Content-Type": "application/json"}

TOTAL_REQUESTS = 500
CONCURRENCY = 10

def make_request():
    start_time = time.time()
    response = requests.post(API_URL, json=PAYLOAD, headers=HEADERS)
    end_time = time.time()
    
    if response.status_code == 200:
        return (end_time - start_time) * 1000 # Convert to milliseconds
    return None

print(f"Starting API Load Test: {TOTAL_REQUESTS} requests with concurrency {CONCURRENCY}...")

latencies = []
start_total = time.time()

with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
    futures = [executor.submit(make_request) for _ in range(TOTAL_REQUESTS)]
    
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result is not None:
            latencies.append(result)

end_total = time.time()
total_time = end_total - start_total

if latencies:
    print("\n=== API PERFORMANCE RESULTS ===")
    print(f"Total Requests Processed: {len(latencies)} / {TOTAL_REQUESTS}")
    print(f"Total Time Taken: {total_time:.2f} seconds")
    print(f"Throughput (Requests/sec): {len(latencies) / total_time:.2f} req/s")
    print(f"Average Latency: {statistics.mean(latencies):.2f} ms")
    print(f"Median Latency: {statistics.median(latencies):.2f} ms")
    print(f"Min Latency: {min(latencies):.2f} ms")
    print(f"Max Latency: {max(latencies):.2f} ms")
else:
    print("API Test Failed: Could not connect to backend.")
