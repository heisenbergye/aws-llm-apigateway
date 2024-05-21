import aiohttp
import asyncio
import time
import argparse
from tqdm import tqdm

async def fetch(session, url, model, token):
    start_time = time.time()
    
    headers = {
     "Content-Type": "application/json; charset=utf-8",
     "Authorization": 'Bearer '+token
    }
    
    body  = {
        "model": model,
        "temperature": 0.7,
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": "Tell me something about large language models."}],
        "stream": False
    }
    
    async with session.post(url, json=body, headers=headers) as response:
        response_json = await response.json()
        end_time = time.time()
        response_time = end_time - start_time
        completion_tokens = response_json.get('usage').get('completion_tokens')
        return completion_tokens, response_time


async def bound_fetch(sem, session, url, model, token, pbar):
    async with sem:
        result = await fetch(session, url, model, token)
        pbar.update(1)
        return result
        
        
async def run(load_url, load_model, token, max_concurrent_requests, total_requests):    
    
    sem = asyncio.Semaphore(max_concurrent_requests)
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        with tqdm(total=total_requests) as pbar:
            for _ in range(total_requests):
                task = asyncio.ensure_future(bound_fetch(sem, session, load_url, load_model, token, pbar))
                tasks.append(task)
        
            results = await asyncio.gather(*tasks)
            
            completion_tokens = sum(result[0] for result in results)
            response_times = [result[1] for result in results]
        
            return completion_tokens, response_times
        


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://0.0.0.0:4000/chat/completions", type=str, help="api url")
    parser.add_argument("--model", default="llama3", type=str, help="model name")
    parser.add_argument("--token", default="sk-1234", type=str, help="api token")
    parser.add_argument("--concurrent", '-c', default=1, type=int, help="max concurrent requests")
    parser.add_argument("--number", '-n', default=1, type=int, help="requests number")

    args = parser.parse_args()
    
    
    start_time = time.time()
    completion_tokens, response_times = asyncio.run(run(args.url, args.model, args.token ,args.concurrent, args.number))
    end_time = time.time()
    
    
    total_time = end_time - start_time
    avg_latency_per_request = sum(response_times)/len(response_times)
    avg_tokens_per_second = completion_tokens/total_time
    
    print(f'Performance Results:')
    print(f'    Total Requests: {args.number}')
    print(f'    Max Concurrent: {args.concurrent}')
    print(f'    Total Time: {total_time:.2f} seconds')
    print(f'    Average Latency per request: {avg_latency_per_request:.2f} seconds')
    print(f'    Average Tokens per second: {avg_tokens_per_second:.2f}')
