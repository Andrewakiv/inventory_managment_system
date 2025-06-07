from datetime import datetime, timezone
from dateutil import parser

import requests
import requests.exceptions as requests_exceptions
from decouple import config
from psycopg2 import OperationalError

from dal import crud
from .test_data import orders


def get_orders_data():
    try:
        for order in orders['results']:
            product_type_name = order['product_type']
            product_type_id = crud.get_product_type_id(product_type_name)
            if not product_type_id:
                raise ValueError(f"Unknown product_type: {product_type_name}")
            client_name = order['client']
            created_at = parser.parse(order['created_at'])
            status = order['status']

            order_id = crud.get_order_id(order['order_id'])
            if order_id is None:
                crud.insert_order(
                    order_id=order['order_id'],
                    client_name=client_name,
                    created_at=created_at,
                    status=status,
                    product_type_id=product_type_id
                )
        print(f"Data inserted successfully.")
    except requests_exceptions.ConnectionError:
        print(f"Could not connect to.")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error: {err}")
    except OperationalError as db_err:
        print(f"Database error: {db_err}")