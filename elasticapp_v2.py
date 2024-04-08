import sqlite3
import random
import time
from datetime import datetime
from elasticsearch import Elasticsearch
import ssl
import json

# Setup Elasticsearch connection
certificate_path = '/Users/bhargavsutapalli/elasticsearch-8.13.1/config/certs/http_ca.crt'
context = ssl.create_default_context(cafile=certificate_path)
api_key = 'UVpnT3I0NEJlZUtib2FZS2pMQVg6b1NXMlJFMXJSZ1NLVWFTTlZ0U01EUQ=='

es = Elasticsearch(
    ["https://localhost:9200"],
    ssl_context=context,
    api_key=api_key
)

# Create or connect to SQLite database
conn = sqlite3.connect('example.db')

def log_to_elasticsearch(event_type, message, service_name, **kwargs):
    doc = {
        'timestamp': datetime.utcnow().isoformat(),
        'service_name': service_name,
        'event_type': event_type,
        'message': message,
    }
    doc.update(kwargs)  # Include additional keyword arguments in the log
    es.index(index="elasticdemonew-logs", document=doc)

def simulate_user_action():
    service_name = "elasticdemonew"
    users = ["Alice", "Bob", "Charlie", "Dana"]
    actions = [
        {"action": "login", "success_rate": 0.9},
        {"action": "purchase", "success_rate": 0.75},
        {"action": "notification", "success_rate": 0.85}
    ]

    user = random.choice(users)
    action = random.choice(actions)
    success = random.random() < action["success_rate"]
    status_code = 200 if success else random.choice([400, 403, 500])
    response_time = random.randint(50, 300) if success else random.randint(300, 500)
    endpoint_name = f"/api/{action['action']}"
    request_body = {"user": user}
    response_body = {}

    if action["action"] == "login":
        message = "User login successful" if success else "Login failed - Incorrect credentials"
    elif action["action"] == "purchase":
        if success:
            message = "Purchase successful"
            response_body = {"items": ["item1", "item2"], "total": random.randint(100, 500)}
        else:
            message = random.choice(["Purchase failed - Item out of stock", "Purchase failed - Payment declined"])
    elif action["action"] == "notification":
        message = "Notification sent successfully" if success else "Notification failed - Service unavailable"

    log_to_elasticsearch(
        event_type="HTTP_STATUS" if success else "HTTP_ERROR",
        message=message,
        service_name=service_name,
        endpoint_name=endpoint_name,
        status_code=status_code,
        response_time=response_time,
        request_body=json.dumps(request_body),
        response_body=json.dumps(response_body)
    )

# Main loop
try:
    while True:
        simulate_user_action()
        time.sleep(random.uniform(0.5, 2))  # Random sleep to simulate varied traffic
except KeyboardInterrupt:
    pass
finally:
    conn.close()
