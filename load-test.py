import requests
import time
from multiprocessing import Pool

url = "http://0.0.0.0:4000/chat/completions"

headers = {
     "Content-Type": "application/json; charset=utf-8",
     "Authorization": 'Bearer sk-1234'
}

data = {
    "model": "mistral7b",
    "temperature": 0.1,
    "max_tokens": 1000,
    "messages": [{"role": "user", "content": "Tell me something about large language models."}]
}

num_requests = 50
latencies = []
tokens = []
def send_request(_):
    start_time = time.time()
    response = requests.post(url, headers=headers, json=data).json()
    #print(response.get('usage').get('completion_tokens'))
    end_time = time.time()
    latency = end_time - start_time
    latencies.append(latency)
    token_count = response.get('usage').get('completion_tokens')
    tokens.append(token_count)
    return latency, token_count

if __name__ == "__main__":
    num_requests = 10
    with Pool(processes=num_requests) as pool:
        results = pool.map(send_request, range(num_requests))
    latencies, tokens = zip(*results)
    average_latency = sum(latencies) / num_requests
    print(f"Average Latency: {average_latency} seconds")
    average_tokens_per_second = sum(tokens) / sum(latencies)
    print(f"Average Tokens per Second: {average_tokens_per_second}")
