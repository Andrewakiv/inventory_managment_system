from datetime import datetime, timedelta
import random


product_types = ['small', 'medium', 'large']
statuses = ['pending', 'in_progress', 'completed']


orders = []
start_date = datetime(2024, 1, 1)

for i in range(1, 101):
    order = {
        "order_id": i,
        "client": f"Client {random.randint(1, 30)}",
        "created_at": (start_date + timedelta(days=random.randint(0, 180))).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": random.choice(statuses),
        "product_type": random.choice(product_types)
    }
    orders.append(order)


api_response = {
    "count": len(orders),
    "results": orders
}

print(api_response)
print(type(api_response))
