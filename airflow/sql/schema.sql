CREATE SCHEMA IF NOT EXISTS analytics;


CREATE TABLE IF NOT EXISTS analytics.product_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);


CREATE TABLE IF NOT EXISTS analytics.orders (
    id SERIAL PRIMARY KEY,
    client_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL,
    product_type_id INTEGER NOT NULL REFERENCES analytics.product_types(id)
);


CREATE TABLE IF NOT EXISTS analytics.materials (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    unit VARCHAR(20) NOT NULL
);


CREATE TABLE IF NOT EXISTS analytics.consumption_standards (
    id SERIAL PRIMARY KEY,
    product_type_id INTEGER NOT NULL REFERENCES analytics.product_types(id) ON DELETE CASCADE,
    material_id INTEGER NOT NULL REFERENCES analytics.materials(id) ON DELETE CASCADE,
    quantity NUMERIC(10, 2) NOT NULL,
    CONSTRAINT unique_product_material UNIQUE (product_type_id, material_id)
);


CREATE TABLE IF NOT EXISTS analytics.material_consumption (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES analytics.orders(id) ON DELETE CASCADE,
    material_id INTEGER NOT NULL REFERENCES analytics.materials(id) ON DELETE CASCADE,
    quantity NUMERIC(10, 2) NOT NULL
);


INSERT INTO analytics.product_types (name) VALUES
('small'),
('medium'),
('large')
ON CONFLICT DO NOTHING;


INSERT INTO analytics.materials (name, unit) VALUES
('Glossy Paper', 'pcs'),
('Cover Board', 'pcs'),
('Glue', 'ml'),
('Cardboard Insert', 'pcs'),
('Lamination Film', 'cm2')
ON CONFLICT DO NOTHING;


INSERT INTO analytics.consumption_standards (product_type_id, material_id, quantity) VALUES
(1, 1, 20),
(1, 2, 1),
(1, 3, 10),
(1, 4, 1),
(1, 5, 1500)
ON CONFLICT ON CONSTRAINT unique_product_material DO NOTHING;


INSERT INTO analytics.consumption_standards (product_type_id, material_id, quantity) VALUES
(2, 1, 30),
(2, 2, 1),
(2, 3, 15),
(2, 4, 1),
(2, 5, 2000)
ON CONFLICT ON CONSTRAINT unique_product_material DO NOTHING;


INSERT INTO analytics.consumption_standards (product_type_id, material_id, quantity) VALUES
(3, 1, 40),
(3, 2, 1),
(3, 3, 20),
(3, 4, 1),
(3, 5, 3000)
ON CONFLICT ON CONSTRAINT unique_product_material DO NOTHING;
