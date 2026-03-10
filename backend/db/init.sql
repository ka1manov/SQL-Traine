-- SQL Trainer - Database Schema & Seed Data

-- 1. departments
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    budget NUMERIC(12, 2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- 2. employees
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department_id INT REFERENCES departments(id),
    salary NUMERIC(10, 2),
    hire_date DATE,
    is_active BOOLEAN DEFAULT TRUE
);

-- 3. customers
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    registered_at TIMESTAMP DEFAULT NOW()
);

-- 4. products
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(50),
    price NUMERIC(10, 2) NOT NULL,
    stock INT DEFAULT 0
);

-- 5. orders
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    product_id INT REFERENCES products(id),
    quantity INT NOT NULL DEFAULT 1,
    total NUMERIC(10, 2),
    status VARCHAR(20) DEFAULT 'pending',
    ordered_at TIMESTAMP DEFAULT NOW()
);

-- 6. invoices
CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id),
    amount NUMERIC(10, 2) NOT NULL,
    paid BOOLEAN DEFAULT FALSE,
    issued_at TIMESTAMP DEFAULT NOW()
);

-- 7. salaries_log
CREATE TABLE salaries_log (
    id SERIAL PRIMARY KEY,
    employee_id INT REFERENCES employees(id),
    old_salary NUMERIC(10, 2),
    new_salary NUMERIC(10, 2),
    changed_at TIMESTAMP DEFAULT NOW()
);

-- 8. subscriptions
CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    plan VARCHAR(20) NOT NULL,
    price NUMERIC(8, 2) NOT NULL,
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- 9. streams
CREATE TABLE streams (
    id SERIAL PRIMARY KEY,
    user_id INT,
    song VARCHAR(200) NOT NULL,
    artist VARCHAR(100),
    genre VARCHAR(50),
    duration_sec INT,
    streamed_at TIMESTAMP DEFAULT NOW()
);

-- 10. bookings
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    guest_name VARCHAR(100) NOT NULL,
    room_type VARCHAR(50),
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    price_per_night NUMERIC(8, 2),
    city VARCHAR(100)
);

-- 11. ab_tests
CREATE TABLE ab_tests (
    id SERIAL PRIMARY KEY,
    user_id INT,
    test_name VARCHAR(100) NOT NULL,
    variant CHAR(1) NOT NULL,
    converted BOOLEAN DEFAULT FALSE,
    revenue NUMERIC(8, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 12. clickstream
CREATE TABLE clickstream (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(36),
    user_id INT,
    page VARCHAR(200),
    action VARCHAR(50),
    duration_sec INT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- APP TABLES (auth, progress, history, etc.)
-- ============================================================

CREATE TABLE app_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    token VARCHAR(64) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_progress (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES app_users(id) ON DELETE CASCADE,
    task_id INT NOT NULL,
    solved BOOLEAN DEFAULT FALSE,
    best_match_pct FLOAT DEFAULT 0,
    attempts INT DEFAULT 0,
    last_attempt_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, task_id)
);

CREATE TABLE query_history (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES app_users(id) ON DELETE CASCADE,
    sql_text TEXT NOT NULL,
    execution_time_ms INT,
    row_count INT DEFAULT 0,
    had_error BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_bookmarks (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES app_users(id) ON DELETE CASCADE,
    task_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, task_id)
);

CREATE TABLE flashcard_progress (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES app_users(id) ON DELETE CASCADE,
    card_id INT NOT NULL,
    ease_factor FLOAT DEFAULT 2.5,
    interval_days INT DEFAULT 1,
    repetitions INT DEFAULT 0,
    next_review TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, card_id)
);

CREATE TABLE daily_streaks (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES app_users(id) ON DELETE CASCADE,
    completed_date DATE NOT NULL,
    task_id INT NOT NULL,
    UNIQUE(user_id, completed_date)
);

-- ============================================================
-- SEED DATA
-- ============================================================

-- departments (5)
INSERT INTO departments (name, budget) VALUES
('Engineering', 500000),
('Marketing', 200000),
('Sales', 300000),
('HR', 150000),
('Finance', 250000);

-- employees (12)
INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date) VALUES
('Alice', 'Johnson', 'alice@company.com', 1, 95000, '2020-03-15'),
('Bob', 'Smith', 'bob@company.com', 1, 105000, '2019-07-01'),
('Carol', 'Williams', 'carol@company.com', 2, 72000, '2021-01-10'),
('Dave', 'Brown', 'dave@company.com', 3, 68000, '2021-06-20'),
('Eve', 'Davis', 'eve@company.com', 1, 115000, '2018-11-05'),
('Frank', 'Miller', 'frank@company.com', 4, 62000, '2022-02-14'),
('Grace', 'Wilson', 'grace@company.com', 2, 78000, '2020-09-01'),
('Hank', 'Moore', 'hank@company.com', 3, 71000, '2021-03-22'),
('Ivy', 'Taylor', 'ivy@company.com', 5, 88000, '2019-12-01'),
('Jack', 'Anderson', 'jack@company.com', 1, 99000, '2020-06-15'),
('Karen', 'Thomas', 'karen@company.com', 5, 92000, '2018-08-20'),
('Leo', 'Jackson', 'leo@company.com', 3, 65000, '2022-04-10');

-- customers (8)
INSERT INTO customers (name, email, city, country, registered_at) VALUES
('Acme Corp', 'acme@example.com', 'New York', 'USA', '2023-01-15 10:00:00'),
('Globex Inc', 'globex@example.com', 'London', 'UK', '2023-02-20 14:30:00'),
('Initech', 'initech@example.com', 'San Francisco', 'USA', '2023-03-10 09:15:00'),
('Umbrella LLC', 'umbrella@example.com', 'Tokyo', 'Japan', '2023-04-05 16:45:00'),
('Stark Industries', 'stark@example.com', 'New York', 'USA', '2023-05-12 11:00:00'),
('Wayne Enterprises', 'wayne@example.com', 'Chicago', 'USA', '2023-06-18 13:20:00'),
('Oscorp', 'oscorp@example.com', 'Berlin', 'Germany', '2023-07-22 08:30:00'),
('LexCorp', 'lexcorp@example.com', 'London', 'UK', '2023-08-30 15:10:00');

-- products (7)
INSERT INTO products (name, category, price, stock) VALUES
('Laptop Pro', 'Electronics', 1299.99, 50),
('Wireless Mouse', 'Electronics', 29.99, 200),
('Standing Desk', 'Furniture', 549.00, 30),
('Monitor 27"', 'Electronics', 399.99, 75),
('Keyboard Mech', 'Electronics', 89.99, 150),
('Office Chair', 'Furniture', 349.00, 40),
('USB-C Hub', 'Electronics', 59.99, 100);

-- orders (20)
INSERT INTO orders (customer_id, product_id, quantity, total, status, ordered_at) VALUES
(1, 1, 2, 2599.98, 'completed', '2024-01-10 10:00:00'),
(1, 3, 1, 549.00, 'completed', '2024-01-15 11:30:00'),
(2, 2, 5, 149.95, 'completed', '2024-01-20 14:00:00'),
(3, 4, 3, 1199.97, 'shipped', '2024-02-01 09:00:00'),
(4, 1, 1, 1299.99, 'completed', '2024-02-05 16:00:00'),
(5, 5, 10, 899.90, 'completed', '2024-02-10 11:15:00'),
(2, 6, 2, 698.00, 'pending', '2024-02-14 13:45:00'),
(6, 7, 4, 239.96, 'completed', '2024-02-20 08:30:00'),
(3, 1, 1, 1299.99, 'shipped', '2024-03-01 10:00:00'),
(7, 3, 1, 549.00, 'completed', '2024-03-05 15:20:00'),
(1, 5, 3, 269.97, 'completed', '2024-03-10 12:00:00'),
(8, 4, 2, 799.98, 'pending', '2024-03-15 09:30:00'),
(4, 2, 10, 299.90, 'completed', '2024-03-20 14:10:00'),
(5, 6, 1, 349.00, 'shipped', '2024-03-25 11:00:00'),
(6, 1, 1, 1299.99, 'completed', '2024-04-01 16:30:00'),
(7, 7, 2, 119.98, 'completed', '2024-04-05 08:00:00'),
(8, 3, 2, 1098.00, 'pending', '2024-04-10 13:15:00'),
(3, 5, 5, 449.95, 'completed', '2024-04-15 10:45:00'),
(1, 4, 1, 399.99, 'completed', '2024-04-20 15:00:00'),
(2, 1, 1, 1299.99, 'shipped', '2024-04-25 09:30:00');

-- invoices (8)
INSERT INTO invoices (order_id, amount, paid, issued_at) VALUES
(1, 2599.98, TRUE, '2024-01-11 10:00:00'),
(2, 549.00, TRUE, '2024-01-16 10:00:00'),
(3, 149.95, TRUE, '2024-01-21 10:00:00'),
(5, 1299.99, TRUE, '2024-02-06 10:00:00'),
(6, 899.90, TRUE, '2024-02-11 10:00:00'),
(8, 239.96, TRUE, '2024-02-21 10:00:00'),
(10, 549.00, FALSE, '2024-03-06 10:00:00'),
(15, 1299.99, FALSE, '2024-04-02 10:00:00');

-- salaries_log (8)
INSERT INTO salaries_log (employee_id, old_salary, new_salary, changed_at) VALUES
(1, 85000, 95000, '2022-01-01 00:00:00'),
(2, 95000, 105000, '2021-06-01 00:00:00'),
(5, 100000, 115000, '2021-01-01 00:00:00'),
(3, 65000, 72000, '2023-03-01 00:00:00'),
(9, 80000, 88000, '2022-06-01 00:00:00'),
(11, 85000, 92000, '2021-09-01 00:00:00'),
(7, 70000, 78000, '2023-01-01 00:00:00'),
(10, 90000, 99000, '2022-07-01 00:00:00');

-- subscriptions (9)
INSERT INTO subscriptions (customer_id, plan, price, started_at, ended_at, is_active) VALUES
(1, 'premium', 49.99, '2023-01-15 00:00:00', NULL, TRUE),
(2, 'basic', 9.99, '2023-02-20 00:00:00', NULL, TRUE),
(3, 'premium', 49.99, '2023-03-10 00:00:00', '2023-09-10 00:00:00', FALSE),
(4, 'enterprise', 199.99, '2023-04-05 00:00:00', NULL, TRUE),
(5, 'basic', 9.99, '2023-05-12 00:00:00', '2023-11-12 00:00:00', FALSE),
(6, 'premium', 49.99, '2023-06-18 00:00:00', NULL, TRUE),
(7, 'basic', 9.99, '2023-07-22 00:00:00', NULL, TRUE),
(8, 'enterprise', 199.99, '2023-08-30 00:00:00', NULL, TRUE),
(1, 'enterprise', 199.99, '2024-01-01 00:00:00', NULL, TRUE);

-- streams (15)
INSERT INTO streams (user_id, song, artist, genre, duration_sec, streamed_at) VALUES
(1, 'Bohemian Rhapsody', 'Queen', 'Rock', 354, '2024-01-10 08:00:00'),
(1, 'Stairway to Heaven', 'Led Zeppelin', 'Rock', 482, '2024-01-10 09:00:00'),
(2, 'Blinding Lights', 'The Weeknd', 'Pop', 200, '2024-01-11 10:30:00'),
(3, 'Shape of You', 'Ed Sheeran', 'Pop', 233, '2024-01-12 14:00:00'),
(2, 'Smells Like Teen Spirit', 'Nirvana', 'Rock', 301, '2024-01-13 16:00:00'),
(4, 'Lose Yourself', 'Eminem', 'Hip-Hop', 326, '2024-01-14 11:00:00'),
(1, 'Hotel California', 'Eagles', 'Rock', 391, '2024-01-15 08:30:00'),
(5, 'Rolling in the Deep', 'Adele', 'Pop', 228, '2024-01-16 13:00:00'),
(3, 'Wonderwall', 'Oasis', 'Rock', 258, '2024-01-17 15:00:00'),
(4, 'Billie Jean', 'Michael Jackson', 'Pop', 294, '2024-01-18 09:45:00'),
(5, 'Sweet Child O Mine', 'Guns N Roses', 'Rock', 356, '2024-01-19 17:00:00'),
(2, 'Bad Guy', 'Billie Eilish', 'Pop', 194, '2024-01-20 12:00:00'),
(1, 'Imagine', 'John Lennon', 'Rock', 183, '2024-01-21 10:00:00'),
(3, 'Uptown Funk', 'Bruno Mars', 'Pop', 270, '2024-01-22 14:30:00'),
(4, 'Sicko Mode', 'Travis Scott', 'Hip-Hop', 312, '2024-01-23 20:00:00');

-- bookings (12)
INSERT INTO bookings (guest_name, room_type, check_in, check_out, price_per_night, city) VALUES
('John Doe', 'deluxe', '2024-03-01', '2024-03-05', 250.00, 'Paris'),
('Jane Smith', 'standard', '2024-03-02', '2024-03-04', 120.00, 'London'),
('Bob Lee', 'suite', '2024-03-05', '2024-03-10', 450.00, 'New York'),
('Alice Chen', 'deluxe', '2024-03-08', '2024-03-12', 280.00, 'Tokyo'),
('Tom Brown', 'standard', '2024-03-10', '2024-03-13', 130.00, 'Paris'),
('Sara Wilson', 'suite', '2024-03-15', '2024-03-18', 500.00, 'London'),
('Mike Davis', 'deluxe', '2024-03-20', '2024-03-23', 260.00, 'Berlin'),
('Lisa Wang', 'standard', '2024-03-22', '2024-03-25', 110.00, 'Tokyo'),
('Chris Martin', 'suite', '2024-04-01', '2024-04-05', 480.00, 'New York'),
('Amy Taylor', 'deluxe', '2024-04-03', '2024-04-07', 270.00, 'Paris'),
('Dan Kim', 'standard', '2024-04-10', '2024-04-12', 140.00, 'Berlin'),
('Eva Garcia', 'suite', '2024-04-15', '2024-04-20', 520.00, 'London');

-- ab_tests (20)
INSERT INTO ab_tests (user_id, test_name, variant, converted, revenue, created_at) VALUES
(1, 'checkout_flow', 'A', TRUE, 49.99, '2024-01-01 10:00:00'),
(2, 'checkout_flow', 'B', TRUE, 79.99, '2024-01-01 10:05:00'),
(3, 'checkout_flow', 'A', FALSE, 0, '2024-01-01 10:10:00'),
(4, 'checkout_flow', 'B', TRUE, 29.99, '2024-01-01 10:15:00'),
(5, 'checkout_flow', 'A', TRUE, 99.99, '2024-01-01 10:20:00'),
(6, 'homepage_hero', 'A', FALSE, 0, '2024-01-02 11:00:00'),
(7, 'homepage_hero', 'B', TRUE, 59.99, '2024-01-02 11:05:00'),
(8, 'homepage_hero', 'A', TRUE, 39.99, '2024-01-02 11:10:00'),
(9, 'homepage_hero', 'B', FALSE, 0, '2024-01-02 11:15:00'),
(10, 'homepage_hero', 'A', TRUE, 149.99, '2024-01-02 11:20:00'),
(1, 'pricing_page', 'A', TRUE, 199.99, '2024-01-03 12:00:00'),
(2, 'pricing_page', 'B', FALSE, 0, '2024-01-03 12:05:00'),
(3, 'pricing_page', 'A', FALSE, 0, '2024-01-03 12:10:00'),
(4, 'pricing_page', 'B', TRUE, 89.99, '2024-01-03 12:15:00'),
(5, 'pricing_page', 'A', TRUE, 59.99, '2024-01-03 12:20:00'),
(6, 'checkout_flow', 'A', TRUE, 119.99, '2024-01-04 13:00:00'),
(7, 'checkout_flow', 'B', FALSE, 0, '2024-01-04 13:05:00'),
(8, 'checkout_flow', 'B', TRUE, 69.99, '2024-01-04 13:10:00'),
(9, 'homepage_hero', 'A', FALSE, 0, '2024-01-04 13:15:00'),
(10, 'pricing_page', 'B', TRUE, 299.99, '2024-01-04 13:20:00');

-- clickstream (20)
INSERT INTO clickstream (session_id, user_id, page, action, duration_sec, created_at) VALUES
('sess-001', 1, '/home', 'view', 15, '2024-01-10 10:00:00'),
('sess-001', 1, '/products', 'view', 45, '2024-01-10 10:00:15'),
('sess-001', 1, '/products/1', 'click', 30, '2024-01-10 10:01:00'),
('sess-001', 1, '/cart', 'add_to_cart', 10, '2024-01-10 10:01:30'),
('sess-001', 1, '/checkout', 'purchase', 60, '2024-01-10 10:01:40'),
('sess-002', 2, '/home', 'view', 20, '2024-01-10 11:00:00'),
('sess-002', 2, '/products', 'view', 35, '2024-01-10 11:00:20'),
('sess-002', 2, '/products/3', 'click', 25, '2024-01-10 11:00:55'),
('sess-002', 2, '/home', 'view', 10, '2024-01-10 11:01:20'),
('sess-003', 3, '/home', 'view', 8, '2024-01-11 09:00:00'),
('sess-003', 3, '/pricing', 'view', 50, '2024-01-11 09:00:08'),
('sess-003', 3, '/signup', 'click', 40, '2024-01-11 09:00:58'),
('sess-003', 3, '/signup', 'submit', 5, '2024-01-11 09:01:38'),
('sess-004', 4, '/home', 'view', 12, '2024-01-12 14:00:00'),
('sess-004', 4, '/blog', 'view', 120, '2024-01-12 14:00:12'),
('sess-004', 4, '/blog/post-1', 'click', 180, '2024-01-12 14:02:12'),
('sess-005', 5, '/home', 'view', 5, '2024-01-13 16:00:00'),
('sess-005', 5, '/products', 'view', 60, '2024-01-13 16:00:05'),
('sess-005', 5, '/products/2', 'click', 45, '2024-01-13 16:01:05'),
('sess-005', 5, '/cart', 'add_to_cart', 8, '2024-01-13 16:01:50');
