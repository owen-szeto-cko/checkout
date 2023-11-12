import requests
import csv
import random
import threading
import time

ENDPOINT = 'https://api.sandbox.checkout.com/payments'
SK = 'Bearer sk_sbox_nrjsogdxuxflto2t2oqr6elxbaw'

# Number of threads to create (e.g., 1000 threads for 1000 requests).
num_threads = 3

headers = {
    'Accept-Encoding': '*',
    'Content-Type': 'application/json; charset=utf-8',
    'Authorization': SK,
    'Connection': 'keep-alive',
    # 'Cko-Idempotency-Key': 'a2',
    'User-Agent': 'PostmanRuntime/7.35.0'
}

output_list = None

def payment_request_task():
    data = {
        "source": {
            "type": "card",
            "number": "4242424242424242",
            "expiry_month": "01",
            "expiry_year": "2030"
        },
        "amount": random.randint(1,1000),
        "currency": "HKD",
        "success_url": "https://www.example.com",
        "failure_url": "https://www.checkout.com",
        "processing_channel_id": "pc_rsy5oljjxabezin4pd6v2l7qfy"
    }
    try:
        response = requests.post(ENDPOINT, headers=headers, json=data)
        # print(response.status_code)
        print(response.headers)
        if response.status_code == 201:
            output_list.write(response.json()['id'] + '\n')
        else:
            print(f"Request failed with status code {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"An error occurred: {e}")

# Create and start threads to send POST requests.
def invoke_thread_pool(task):
    cnt = 0 
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=task)
        threads.append(thread)
        thread.start()
        # print(f"DBG: Thread {cnt} started")
        cnt += 1
        # time.sleep(0.01)

    # Wait for all threads to finish.
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    output_list = open('pay_id.csv', 'w+')
    invoke_thread_pool(payment_request_task)
    output_list.close()
