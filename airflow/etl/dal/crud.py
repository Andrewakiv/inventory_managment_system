from .base import get_db_cursor


def get_product_type_id(product_type_name):
    with get_db_cursor() as cur:
        cur.execute(
            "SELECT id FROM analytics.product_types WHERE name = %s;", (product_type_name,)
        )
        result = cur.fetchone()
    return result[0] if result else None


def get_order_id(id):
    with get_db_cursor() as cur:
        cur.execute(
            "SELECT id FROM analytics.orders WHERE id = %s;", (id,)
        )
        result = cur.fetchone()
    return result[0] if result else None


def insert_order(order_id, client_name, created_at, status, product_type_id):
    with get_db_cursor() as cur:
        cur.execute(
            """
            INSERT INTO analytics.orders (id, client_name, created_at, status, product_type_id)
            VALUES ( %s, %s, %s, %s, %s);
            """,
            (order_id, client_name, created_at, status, product_type_id),
        )


def insert_material_consumption():
    with get_db_cursor() as cur:
        cur.execute(
            """
            INSERT INTO analytics.material_consumption (order_id, material_id, quantity)
            SELECT
                o.id AS order_id,
                cs.material_id,
                cs.quantity
            FROM
                analytics.orders o
            JOIN
                analytics.product_types pt ON o.product_type_id = pt.id
            JOIN
                analytics.consumption_standards cs ON cs.product_type_id = pt.id
            LEFT JOIN
                analytics.material_consumption mc ON mc.order_id = o.id AND mc.material_id = cs.material_id
            WHERE
                mc.id IS NULL;
            """
        )
