import os
import time
import requests
import redis
from flask import Flask, request, jsonify

app = Flask(__name__)

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
BACKEND_URL = os.getenv('BACKEND_URL', 'https://httpbin.org/anything')
RATE_LIMIT = int(os.getenv('RATE_LIMIT', '5'))  # Max requests
WINDOW_SIZE = int(os.getenv('WINDOW_SIZE', '60'))  # Time window in seconds

cache = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

def is_rate_limited(ip_address: str) -> bool:
    key = f"rate_limit:{ip_address}"
    current_time = time.time()
    pipeline = cache.pipeline()
    
    # Sliding window log implementation
    pipeline.zremrangebyscore(key, 0, current_time - WINDOW_SIZE)
    pipeline.zadd(key, {str(current_time): current_time})
    pipeline.zcard(key)
    pipeline.expire(key, WINDOW_SIZE)
    results = pipeline.execute()
    
    request_count = results[2]
    return request_count > RATE_LIMIT

@app.route('/proxy', methods=['GET', 'POST'])
def proxy_request():
    client_ip = request.remote_addr or "unknown_client"
    
    if is_rate_limited(client_ip):
        return jsonify({
            "error": "Too Many Requests",
            "message": f"Rate limit exceeded. Allowed: {RATE_LIMIT} requests per {WINDOW_SIZE}s."
        }), 429

    # Forward payload to external/mock backend
    payload = request.get_json() if request.is_json else None
    response = requests.request(
        method=request.method,
        url=BACKEND_URL,
        json=payload,
        timeout=5
    )
    
    return jsonify({
        "status": "Forwarded",
        "backend_response": response.json() if response.headers.get('content-type') == 'application/json' else response.text
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)