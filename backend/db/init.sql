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

-- 13. categories (hierarchical tree for recursive CTEs)
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_id INT REFERENCES categories(id),
    depth INT NOT NULL DEFAULT 0,
    sort_order INT NOT NULL DEFAULT 0
);

-- 14. transactions (financial ledger)
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    account_id INT NOT NULL,
    txn_type VARCHAR(20) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    balance_after NUMERIC(10, 2) NOT NULL,
    category VARCHAR(50),
    description VARCHAR(200),
    txn_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 15. user_profiles (JSONB + arrays)
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    settings JSONB NOT NULL DEFAULT '{}',
    tags TEXT[] DEFAULT '{}',
    scores INT[] DEFAULT '{}',
    bio TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 16. tickets (support tickets with duplicates)
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    ticket_ref VARCHAR(20) NOT NULL,
    customer_id INT REFERENCES customers(id),
    subject VARCHAR(200) NOT NULL,
    priority VARCHAR(10) NOT NULL,
    status VARCHAR(20) NOT NULL,
    assigned_to VARCHAR(50),
    satisfaction_score INT,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 17. sensor_readings (time-series with gaps)
CREATE TABLE sensor_readings (
    id SERIAL PRIMARY KEY,
    sensor_id INT NOT NULL,
    metric VARCHAR(30) NOT NULL,
    value NUMERIC(8, 2) NOT NULL,
    is_anomaly BOOLEAN DEFAULT FALSE,
    recorded_at TIMESTAMP NOT NULL
);

-- 18. event_log (sequential events with JSONB)
CREATE TABLE event_log (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB DEFAULT '{}',
    seq_num INT NOT NULL,
    session_id VARCHAR(36),
    created_at TIMESTAMP NOT NULL
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

-- categories (20 rows, 4-level hierarchy)
INSERT INTO categories (id, name, parent_id, depth, sort_order) VALUES
(1, 'Electronics', NULL, 0, 1),
(2, 'Furniture', NULL, 0, 2),
(3, 'Clothing', NULL, 0, 3),
(4, 'Computers', 1, 1, 1),
(5, 'Audio', 1, 1, 2),
(6, 'Phones', 1, 1, 3),
(7, 'Living Room', 2, 1, 1),
(8, 'Office', 2, 1, 2),
(9, 'Men', 3, 1, 1),
(10, 'Women', 3, 1, 2),
(11, 'Laptops', 4, 2, 1),
(12, 'Desktops', 4, 2, 2),
(13, 'Headphones', 5, 2, 1),
(14, 'Speakers', 5, 2, 2),
(15, 'Smartphones', 6, 2, 1),
(16, 'Sofas', 7, 2, 1),
(17, 'Desks', 8, 2, 1),
(18, 'Chairs', 8, 2, 2),
(19, 'Gaming Laptops', 11, 3, 1),
(20, 'Ultrabooks', 11, 3, 2);
SELECT setval('categories_id_seq', 20);

-- transactions (40 rows, 4 accounts, Jan-Apr 2024, with gaps and near-duplicates)
INSERT INTO transactions (account_id, txn_type, amount, balance_after, category, description, txn_date) VALUES
(1, 'credit', 5000.00, 5000.00, 'salary', 'January salary', '2024-01-05'),
(1, 'debit', 1200.00, 3800.00, 'rent', 'Monthly rent', '2024-01-07'),
(1, 'debit', 85.50, 3714.50, 'groceries', 'Weekly groceries', '2024-01-10'),
(1, 'debit', 45.00, 3669.50, 'utilities', 'Electric bill', '2024-01-15'),
(1, 'credit', 200.00, 3869.50, 'transfer', 'Transfer from savings', '2024-01-20'),
(1, 'debit', 85.50, 3784.00, 'groceries', 'Weekly groceries', '2024-01-10'),
(1, 'credit', 5000.00, 8784.00, 'salary', 'February salary', '2024-02-05'),
(1, 'debit', 1200.00, 7584.00, 'rent', 'Monthly rent', '2024-02-07'),
(1, 'debit', 92.30, 7491.70, 'groceries', 'Weekly groceries', '2024-02-14'),
(1, 'debit', 150.00, 7341.70, 'entertainment', 'Concert tickets', '2024-02-22'),
(2, 'credit', 7500.00, 7500.00, 'salary', 'January salary', '2024-01-03'),
(2, 'debit', 1800.00, 5700.00, 'rent', 'Monthly rent', '2024-01-06'),
(2, 'debit', 120.00, 5580.00, 'groceries', 'Weekly groceries', '2024-01-12'),
(2, 'debit', 350.00, 5230.00, 'insurance', 'Car insurance', '2024-01-18'),
(2, 'credit', 7500.00, 12730.00, 'salary', 'February salary', '2024-02-03'),
(2, 'debit', 1800.00, 10930.00, 'rent', 'Monthly rent', '2024-02-06'),
(2, 'debit', 65.00, 10865.00, 'utilities', 'Internet bill', '2024-02-15'),
(2, 'debit', 500.00, 10365.00, 'travel', 'Flight booking', '2024-02-28'),
(2, 'credit', 7500.00, 17865.00, 'salary', 'March salary', '2024-03-04'),
(2, 'debit', 1800.00, 16065.00, 'rent', 'Monthly rent', '2024-03-06'),
(3, 'credit', 4200.00, 4200.00, 'salary', 'January salary', '2024-01-08'),
(3, 'debit', 950.00, 3250.00, 'rent', 'Monthly rent', '2024-01-10'),
(3, 'debit', 78.00, 3172.00, 'groceries', 'Weekly groceries', '2024-01-15'),
(3, 'credit', 150.00, 3322.00, 'freelance', 'Side project payment', '2024-01-25'),
(3, 'credit', 4200.00, 7522.00, 'salary', 'February salary', '2024-02-08'),
(3, 'debit', 950.00, 6572.00, 'rent', 'Monthly rent', '2024-02-10'),
(3, 'debit', 210.00, 6362.00, 'shopping', 'New headphones', '2024-02-18'),
(3, 'credit', 4200.00, 10562.00, 'salary', 'March salary', '2024-03-08'),
(3, 'debit', 950.00, 9612.00, 'rent', 'Monthly rent', '2024-03-10'),
(3, 'debit', 78.00, 9534.00, 'groceries', 'Weekly groceries', '2024-03-22'),
(4, 'credit', 6000.00, 6000.00, 'salary', 'January salary', '2024-01-04'),
(4, 'debit', 1500.00, 4500.00, 'rent', 'Monthly rent', '2024-01-08'),
(4, 'debit', 200.00, 4300.00, 'utilities', 'Gas and electric', '2024-01-16'),
(4, 'debit', 15.00, 4285.00, 'fee', 'ATM withdrawal fee', '2024-01-22'),
(4, 'credit', 6000.00, 10285.00, 'salary', 'February salary', '2024-02-04'),
(4, 'debit', 1500.00, 8785.00, 'rent', 'Monthly rent', '2024-02-08'),
(4, 'debit', 15.00, 8770.00, 'fee', 'ATM withdrawal fee', '2024-02-22'),
(4, 'credit', 6000.00, 14770.00, 'salary', 'March salary', '2024-03-04'),
(4, 'debit', 1500.00, 13270.00, 'rent', 'Monthly rent', '2024-03-08'),
(4, 'debit', 320.00, 12950.00, 'shopping', 'Spring wardrobe', '2024-03-25');

-- user_profiles (25 rows, varied JSONB settings, diverse tags and scores)
INSERT INTO user_profiles (username, email, settings, tags, scores, bio) VALUES
('alex_dev', 'alex@example.com', '{"theme": "dark", "notifications": {"email": true, "push": false}, "plan": "premium", "language": "en"}', ARRAY['python', 'sql', 'backend'], ARRAY[88, 92, 75, 95], 'Full-stack developer focused on data systems'),
('maria_data', 'maria@example.com', '{"theme": "light", "notifications": {"email": true, "push": true}, "plan": "free", "language": "es"}', ARRAY['analytics', 'sql', 'tableau'], ARRAY[95, 88, 91], 'Data analyst with 5 years experience'),
('john_ops', 'john@example.com', '{"theme": "dark", "notifications": {"email": false, "push": true}, "plan": "premium", "language": "en"}', ARRAY['devops', 'aws', 'docker'], ARRAY[72, 80, 68], 'DevOps engineer and cloud enthusiast'),
('sara_ml', 'sara@example.com', '{"theme": "auto", "notifications": {"email": true, "push": true}, "plan": "enterprise", "language": "en"}', ARRAY['python', 'ml', 'tensorflow'], ARRAY[98, 95, 92, 88, 96], 'Machine learning researcher'),
('tom_front', 'tom@example.com', '{"theme": "light", "notifications": {"email": false, "push": false}, "plan": "free", "language": "en"}', ARRAY['react', 'typescript', 'css'], ARRAY[82, 78, 90], 'Frontend developer building accessible UIs'),
('lisa_sec', 'lisa@example.com', '{"theme": "dark", "notifications": {"email": true, "push": true}, "plan": "premium", "language": "en"}', ARRAY['security', 'python', 'networking'], ARRAY[90, 85, 88, 92], 'Cybersecurity specialist'),
('mike_db', 'mike@example.com', '{"theme": "dark", "notifications": {"email": true, "push": false}, "plan": "premium", "language": "en"}', ARRAY['postgresql', 'sql', 'redis'], ARRAY[96, 94, 90], 'Database administrator and query optimizer'),
('emma_pm', 'emma@example.com', '{"theme": "light", "notifications": {"email": true, "push": true}, "plan": "enterprise", "language": "fr"}', ARRAY['agile', 'scrum', 'leadership'], ARRAY[85, 80, 78], 'Product manager bridging tech and business'),
('dave_mobile', 'dave@example.com', '{"theme": "auto", "notifications": {"email": false, "push": true}, "plan": "free", "language": "en"}', ARRAY['swift', 'kotlin', 'flutter'], ARRAY[76, 82, 70, 88], 'Mobile developer for iOS and Android'),
('nina_qa', 'nina@example.com', '{"theme": "light", "notifications": {"email": true, "push": false}, "plan": "free", "language": "de"}', ARRAY['testing', 'selenium', 'qa'], ARRAY[88, 84, 91], 'QA engineer passionate about test automation'),
('chris_arch', 'chris@example.com', '{"theme": "dark", "notifications": {"email": true, "push": true}, "plan": "enterprise", "language": "en"}', ARRAY['architecture', 'microservices', 'sql'], ARRAY[92, 95, 89, 94], 'Solutions architect designing scalable systems'),
('amy_design', 'amy@example.com', '{"theme": "light", "notifications": {"email": false, "push": true}, "plan": "premium", "language": "en"}', ARRAY['figma', 'ux', 'css'], ARRAY[80, 75, 85], 'UX designer creating intuitive interfaces'),
('ryan_data', 'ryan@example.com', '{"theme": "dark", "notifications": {"email": true, "push": false}, "plan": "premium", "language": "en"}', ARRAY['sql', 'python', 'spark'], ARRAY[91, 87, 93, 85], 'Data engineer building ETL pipelines'),
('kate_cloud', 'kate@example.com', '{"theme": "auto", "notifications": {"email": true, "push": true}, "plan": "enterprise", "language": "en"}', ARRAY['aws', 'terraform', 'kubernetes'], ARRAY[88, 92, 86], 'Cloud infrastructure engineer'),
('pedro_game', 'pedro@example.com', '{"theme": "dark", "notifications": {"email": false, "push": false}, "plan": "free", "language": "pt"}', ARRAY['unity', 'csharp', 'gamedev'], ARRAY[74, 70, 82, 68], 'Indie game developer'),
('yuki_ai', 'yuki@example.com', '{"theme": "dark", "notifications": {"email": true, "push": true}, "plan": "enterprise", "language": "ja"}', ARRAY['python', 'pytorch', 'nlp'], ARRAY[97, 94, 96, 99], 'AI researcher specializing in NLP'),
('olivia_bi', 'olivia@example.com', '{"theme": "light", "notifications": {"email": true, "push": false}, "plan": "premium", "language": "en"}', ARRAY['sql', 'powerbi', 'analytics'], ARRAY[89, 86, 92], 'BI analyst turning data into insights'),
('james_sre', 'james@example.com', '{"theme": "dark", "notifications": {"email": true, "push": true}, "plan": "premium", "language": "en"}', ARRAY['sre', 'monitoring', 'linux'], ARRAY[83, 87, 79, 85], 'Site reliability engineer'),
('sophia_full', 'sophia@example.com', '{"theme": "auto", "notifications": {"email": false, "push": true}, "plan": "free", "language": "en"}', ARRAY['react', 'node', 'sql', 'python'], ARRAY[82, 78, 85, 80], 'Full-stack developer learning everything'),
('liam_embedded', 'liam@example.com', '{"theme": "dark", "notifications": {"email": false, "push": false}, "plan": "free", "language": "en"}', ARRAY['c', 'embedded', 'iot'], ARRAY[90, 86, 72], 'Embedded systems programmer'),
('zara_data', 'zara@example.com', '{"theme": "light", "notifications": {"email": true, "push": true}, "plan": "premium", "language": "en"}', ARRAY['r', 'statistics', 'sql'], ARRAY[93, 90, 88, 91], 'Statistician and data scientist'),
('ben_backend', 'ben@example.com', '{"theme": "dark", "notifications": {"email": true, "push": false}, "plan": "premium", "language": "en"}', ARRAY['java', 'spring', 'sql'], ARRAY[86, 82, 90], 'Backend developer building APIs'),
('clara_devrel', 'clara@example.com', '{"theme": "light", "notifications": {"email": true, "push": true}, "plan": "enterprise", "language": "en"}', ARRAY['writing', 'python', 'community'], ARRAY[78, 84, 88], 'Developer relations and tech writer'),
('oscar_net', 'oscar@example.com', '{"theme": "auto", "notifications": {"email": false, "push": false}, "plan": "free", "language": "en"}', ARRAY['networking', 'cisco', 'security'], ARRAY[81, 77, 85, 80], 'Network engineer'),
('iris_tic', 'iris@example.com', '{"theme": "dark", "notifications": {"email": true, "push": true}, "plan": "premium", "language": "en"}', ARRAY['sql', 'python', 'analytics', 'ml'], ARRAY[94, 91, 87, 93, 90], 'Analytics engineer bridging data and ML');

-- tickets (35 rows, with duplicate ticket_refs, NULLable satisfaction_score)
INSERT INTO tickets (ticket_ref, customer_id, subject, priority, status, assigned_to, satisfaction_score, created_at, updated_at) VALUES
('TK-1001', 1, 'Cannot login to dashboard', 'high', 'resolved', 'Agent Smith', 5, '2024-01-05 09:00:00', '2024-01-05 14:00:00'),
('TK-1002', 2, 'Billing discrepancy on invoice #42', 'medium', 'closed', 'Agent Jones', 4, '2024-01-06 10:30:00', '2024-01-08 11:00:00'),
('TK-1003', 3, 'Feature request: dark mode', 'low', 'open', NULL, NULL, '2024-01-08 14:00:00', '2024-01-08 14:00:00'),
('TK-1004', 1, 'API rate limit exceeded', 'critical', 'resolved', 'Agent Smith', 3, '2024-01-10 08:00:00', '2024-01-10 09:30:00'),
('TK-1005', 4, 'Data export not working', 'high', 'in_progress', 'Agent Brown', NULL, '2024-01-12 11:00:00', '2024-01-13 09:00:00'),
('TK-1001', 1, 'Cannot login to dashboard', 'high', 'reopened', 'Agent Smith', 2, '2024-01-14 09:00:00', '2024-01-15 16:00:00'),
('TK-1006', 5, 'Password reset email not received', 'medium', 'resolved', 'Agent Jones', 5, '2024-01-15 13:00:00', '2024-01-15 15:00:00'),
('TK-1007', 6, 'Slow page load on reports', 'medium', 'resolved', 'Agent Brown', 4, '2024-01-18 10:00:00', '2024-01-20 11:00:00'),
('TK-1008', 2, 'Integration with Slack broken', 'high', 'closed', 'Agent Smith', NULL, '2024-01-20 08:30:00', '2024-01-22 14:00:00'),
('TK-1002', 2, 'Billing discrepancy on invoice #42', 'medium', 'reopened', 'Agent Jones', 3, '2024-01-22 09:00:00', '2024-01-24 10:00:00'),
('TK-1009', 7, 'Cannot upload files larger than 10MB', 'medium', 'resolved', 'Agent Brown', 4, '2024-01-25 14:00:00', '2024-01-26 11:00:00'),
('TK-1010', 3, 'Mobile app crashes on startup', 'critical', 'resolved', 'Agent Smith', 5, '2024-01-28 07:00:00', '2024-01-28 12:00:00'),
('TK-1011', 8, 'Incorrect timezone in reports', 'low', 'open', NULL, NULL, '2024-01-30 16:00:00', '2024-01-30 16:00:00'),
('TK-1012', 4, 'SSO configuration not saving', 'high', 'in_progress', 'Agent Jones', NULL, '2024-02-01 09:00:00', '2024-02-02 10:00:00'),
('TK-1005', 4, 'Data export not working', 'high', 'resolved', 'Agent Brown', 4, '2024-02-03 11:00:00', '2024-02-05 14:00:00'),
('TK-1013', 5, 'Webhook delivery failures', 'high', 'resolved', 'Agent Smith', NULL, '2024-02-05 08:00:00', '2024-02-06 09:00:00'),
('TK-1014', 1, 'CSV import parsing errors', 'medium', 'closed', 'Agent Jones', 5, '2024-02-08 10:00:00', '2024-02-09 15:00:00'),
('TK-1015', 6, 'Dashboard widgets not loading', 'high', 'resolved', 'Agent Brown', 3, '2024-02-10 11:30:00', '2024-02-12 09:00:00'),
('TK-1010', 3, 'Mobile app crashes on startup', 'critical', 'reopened', 'Agent Smith', 2, '2024-02-12 07:00:00', '2024-02-14 12:00:00'),
('TK-1016', 7, 'Search results not relevant', 'low', 'open', NULL, NULL, '2024-02-15 14:00:00', '2024-02-15 14:00:00'),
('TK-1017', 8, 'Email notifications delayed', 'medium', 'resolved', 'Agent Jones', 4, '2024-02-18 09:00:00', '2024-02-19 11:00:00'),
('TK-1018', 2, 'API documentation outdated', 'low', 'closed', 'Agent Brown', NULL, '2024-02-20 13:00:00', '2024-02-25 10:00:00'),
('TK-1019', 5, 'Two-factor auth not working', 'critical', 'resolved', 'Agent Smith', 5, '2024-02-22 08:00:00', '2024-02-22 10:00:00'),
('TK-1015', 6, 'Dashboard widgets not loading', 'high', 'reopened', 'Agent Brown', 2, '2024-02-25 11:30:00', '2024-02-27 09:00:00'),
('TK-1020', 3, 'Bulk delete not working', 'medium', 'in_progress', 'Agent Jones', NULL, '2024-02-28 10:00:00', '2024-03-01 09:00:00'),
('TK-1021', 1, 'Report scheduling fails silently', 'high', 'resolved', 'Agent Smith', 4, '2024-03-01 09:00:00', '2024-03-03 14:00:00'),
('TK-1022', 4, 'Permission denied on admin panel', 'critical', 'resolved', 'Agent Jones', 5, '2024-03-04 08:00:00', '2024-03-04 11:00:00'),
('TK-1023', 7, 'Charts not rendering in Safari', 'medium', 'closed', 'Agent Brown', 3, '2024-03-06 15:00:00', '2024-03-08 10:00:00'),
('TK-1024', 8, 'Data sync lag between services', 'high', 'in_progress', 'Agent Smith', NULL, '2024-03-10 09:00:00', '2024-03-11 10:00:00'),
('TK-1019', 5, 'Two-factor auth not working', 'critical', 'reopened', 'Agent Smith', 1, '2024-03-12 08:00:00', '2024-03-14 10:00:00'),
('TK-1025', 6, 'Custom field validation broken', 'medium', 'resolved', 'Agent Jones', 4, '2024-03-15 11:00:00', '2024-03-16 14:00:00'),
('TK-1026', 2, 'Audit log incomplete', 'high', 'open', NULL, NULL, '2024-03-18 10:00:00', '2024-03-18 10:00:00'),
('TK-1027', 3, 'PDF generation timeout', 'medium', 'resolved', 'Agent Brown', 3, '2024-03-20 14:00:00', '2024-03-22 09:00:00'),
('TK-1028', 1, 'Duplicate notifications received', 'low', 'closed', 'Agent Jones', 5, '2024-03-25 09:00:00', '2024-03-26 11:00:00'),
('TK-1029', 4, 'API response format changed', 'high', 'resolved', 'Agent Smith', 4, '2024-03-28 08:00:00', '2024-03-29 10:00:00');

-- sensor_readings (50 rows, 3 sensors, 6h intervals, with gaps and anomalies)
INSERT INTO sensor_readings (sensor_id, metric, value, is_anomaly, recorded_at) VALUES
-- Sensor 1: temperature, readings Jan 1-8, gap Jan 9-12, resumes Jan 13
(1, 'temperature', 22.50, FALSE, '2024-01-01 00:00:00'),
(1, 'temperature', 22.80, FALSE, '2024-01-01 06:00:00'),
(1, 'temperature', 23.10, FALSE, '2024-01-01 12:00:00'),
(1, 'temperature', 22.40, FALSE, '2024-01-01 18:00:00'),
(1, 'temperature', 22.60, FALSE, '2024-01-02 00:00:00'),
(1, 'temperature', 22.90, FALSE, '2024-01-02 06:00:00'),
(1, 'temperature', 23.50, FALSE, '2024-01-02 12:00:00'),
(1, 'temperature', 22.70, FALSE, '2024-01-02 18:00:00'),
(1, 'temperature', 35.20, TRUE, '2024-01-03 00:00:00'),
(1, 'temperature', 23.00, FALSE, '2024-01-03 06:00:00'),
(1, 'temperature', 23.30, FALSE, '2024-01-03 12:00:00'),
(1, 'temperature', 22.80, FALSE, '2024-01-03 18:00:00'),
-- gap: sensor 1 offline Jan 4-6
(1, 'temperature', 23.10, FALSE, '2024-01-07 00:00:00'),
(1, 'temperature', 22.90, FALSE, '2024-01-07 06:00:00'),
(1, 'temperature', 23.40, FALSE, '2024-01-07 12:00:00'),
(1, 'temperature', 22.60, FALSE, '2024-01-07 18:00:00'),
(1, 'temperature', 22.80, FALSE, '2024-01-08 00:00:00'),
-- Sensor 2: humidity, readings Jan 1-5, gap Jan 6-9, resumes Jan 10
(2, 'humidity', 45.00, FALSE, '2024-01-01 00:00:00'),
(2, 'humidity', 46.20, FALSE, '2024-01-01 06:00:00'),
(2, 'humidity', 47.80, FALSE, '2024-01-01 12:00:00'),
(2, 'humidity', 44.50, FALSE, '2024-01-01 18:00:00'),
(2, 'humidity', 45.30, FALSE, '2024-01-02 00:00:00'),
(2, 'humidity', 46.00, FALSE, '2024-01-02 06:00:00'),
(2, 'humidity', 85.90, TRUE, '2024-01-02 12:00:00'),
(2, 'humidity', 45.10, FALSE, '2024-01-02 18:00:00'),
(2, 'humidity', 44.80, FALSE, '2024-01-03 00:00:00'),
(2, 'humidity', 45.50, FALSE, '2024-01-03 06:00:00'),
(2, 'humidity', 46.30, FALSE, '2024-01-03 12:00:00'),
(2, 'humidity', 45.00, FALSE, '2024-01-03 18:00:00'),
-- gap: sensor 2 offline Jan 4-7
(2, 'humidity', 44.60, FALSE, '2024-01-08 00:00:00'),
(2, 'humidity', 45.20, FALSE, '2024-01-08 06:00:00'),
(2, 'humidity', 46.10, FALSE, '2024-01-08 12:00:00'),
(2, 'humidity', 44.90, FALSE, '2024-01-08 18:00:00'),
(2, 'humidity', 45.40, FALSE, '2024-01-09 00:00:00'),
-- Sensor 3: pressure, readings Jan 1-3, gap Jan 4-8, resumes Jan 9
(3, 'pressure', 1013.25, FALSE, '2024-01-01 00:00:00'),
(3, 'pressure', 1013.50, FALSE, '2024-01-01 06:00:00'),
(3, 'pressure', 1014.00, FALSE, '2024-01-01 12:00:00'),
(3, 'pressure', 1013.80, FALSE, '2024-01-01 18:00:00'),
(3, 'pressure', 1012.90, FALSE, '2024-01-02 00:00:00'),
(3, 'pressure', 1013.10, FALSE, '2024-01-02 06:00:00'),
(3, 'pressure', 980.50, TRUE, '2024-01-02 12:00:00'),
(3, 'pressure', 1013.40, FALSE, '2024-01-02 18:00:00'),
(3, 'pressure', 1013.60, FALSE, '2024-01-03 00:00:00'),
(3, 'pressure', 1013.20, FALSE, '2024-01-03 06:00:00'),
-- gap: sensor 3 offline Jan 3 12:00 - Jan 8
(3, 'pressure', 1014.10, FALSE, '2024-01-09 00:00:00'),
(3, 'pressure', 1013.70, FALSE, '2024-01-09 06:00:00'),
(3, 'pressure', 1013.90, FALSE, '2024-01-09 12:00:00'),
(3, 'pressure', 950.10, TRUE, '2024-01-09 18:00:00'),
(3, 'pressure', 1014.20, FALSE, '2024-01-10 00:00:00');

-- event_log (45 rows, 5 users, seq_num with gaps, duplicate entries, heterogeneous JSONB)
INSERT INTO event_log (user_id, event_type, event_data, seq_num, session_id, created_at) VALUES
-- User 1: login flow with gaps at seq 4,5 and duplicate at seq 6
(1, 'login', '{"method": "password", "ip": "192.168.1.10", "device": "Chrome/Win"}', 1, 'ses-aaa-001', '2024-01-10 08:00:00'),
(1, 'page_view', '{"url": "/dashboard", "load_time_ms": 320}', 2, 'ses-aaa-001', '2024-01-10 08:01:00'),
(1, 'page_view', '{"url": "/products", "load_time_ms": 450}', 3, 'ses-aaa-001', '2024-01-10 08:05:00'),
-- gap: seq 4, 5 missing
(1, 'purchase', '{"product_id": 1, "amount": 1299.99, "currency": "USD", "payment": "credit_card"}', 6, 'ses-aaa-001', '2024-01-10 08:20:00'),
(1, 'purchase', '{"product_id": 1, "amount": 1299.99, "currency": "USD", "payment": "credit_card"}', 6, 'ses-aaa-001', '2024-01-10 08:20:00'),
(1, 'page_view', '{"url": "/confirmation", "load_time_ms": 200}', 7, 'ses-aaa-001', '2024-01-10 08:21:00'),
(1, 'logout', '{"reason": "user_action"}', 8, 'ses-aaa-001', '2024-01-10 08:30:00'),
-- User 1, session 2
(1, 'login', '{"method": "oauth", "ip": "192.168.1.10", "device": "Chrome/Win"}', 9, 'ses-aaa-002', '2024-01-11 10:00:00'),
(1, 'page_view', '{"url": "/settings", "load_time_ms": 280}', 10, 'ses-aaa-002', '2024-01-11 10:05:00'),
-- User 2: has gap at seq 3, duplicate at seq 5
(2, 'login', '{"method": "password", "ip": "10.0.0.5", "device": "Firefox/Mac"}', 1, 'ses-bbb-001', '2024-01-10 09:00:00'),
(2, 'page_view', '{"url": "/dashboard", "load_time_ms": 410}', 2, 'ses-bbb-001', '2024-01-10 09:02:00'),
-- gap: seq 3 missing
(2, 'page_view', '{"url": "/reports", "load_time_ms": 680}', 4, 'ses-bbb-001', '2024-01-10 09:10:00'),
(2, 'error', '{"code": 500, "message": "Internal server error", "page": "/reports/export"}', 5, 'ses-bbb-001', '2024-01-10 09:12:00'),
(2, 'error', '{"code": 500, "message": "Internal server error", "page": "/reports/export"}', 5, 'ses-bbb-001', '2024-01-10 09:12:00'),
(2, 'page_view', '{"url": "/dashboard", "load_time_ms": 350}', 6, 'ses-bbb-001', '2024-01-10 09:15:00'),
(2, 'logout', '{"reason": "user_action"}', 7, 'ses-bbb-001', '2024-01-10 09:30:00'),
-- User 3: has gaps at seq 2,3 and duplicate at seq 7
(3, 'login', '{"method": "sso", "ip": "172.16.0.20", "device": "Safari/iOS"}', 1, 'ses-ccc-001', '2024-01-11 14:00:00'),
-- gap: seq 2, 3 missing
(3, 'page_view', '{"url": "/products", "load_time_ms": 520}', 4, 'ses-ccc-001', '2024-01-11 14:05:00'),
(3, 'page_view', '{"url": "/products/5", "load_time_ms": 310}', 5, 'ses-ccc-001', '2024-01-11 14:08:00'),
(3, 'purchase', '{"product_id": 5, "amount": 89.99, "currency": "USD", "payment": "paypal"}', 6, 'ses-ccc-001', '2024-01-11 14:15:00'),
(3, 'page_view', '{"url": "/orders", "load_time_ms": 290}', 7, 'ses-ccc-001', '2024-01-11 14:18:00'),
(3, 'page_view', '{"url": "/orders", "load_time_ms": 290}', 7, 'ses-ccc-001', '2024-01-11 14:18:00'),
(3, 'logout', '{"reason": "timeout"}', 8, 'ses-ccc-001', '2024-01-11 14:48:00'),
-- User 4: clean flow, then error session
(4, 'login', '{"method": "password", "ip": "192.168.2.30", "device": "Edge/Win"}', 1, 'ses-ddd-001', '2024-01-12 11:00:00'),
(4, 'page_view', '{"url": "/dashboard", "load_time_ms": 380}', 2, 'ses-ddd-001', '2024-01-12 11:01:00'),
(4, 'page_view', '{"url": "/billing", "load_time_ms": 420}', 3, 'ses-ddd-001', '2024-01-12 11:05:00'),
(4, 'purchase', '{"product_id": 3, "amount": 549.00, "currency": "USD", "payment": "credit_card"}', 4, 'ses-ddd-001', '2024-01-12 11:15:00'),
-- gap: seq 5 missing
(4, 'logout', '{"reason": "user_action"}', 6, 'ses-ddd-001', '2024-01-12 11:30:00'),
(4, 'login', '{"method": "password", "ip": "192.168.2.30", "device": "Edge/Win"}', 7, 'ses-ddd-002', '2024-01-13 09:00:00'),
(4, 'error', '{"code": 403, "message": "Forbidden", "page": "/admin"}', 8, 'ses-ddd-002', '2024-01-13 09:02:00'),
(4, 'logout', '{"reason": "user_action"}', 9, 'ses-ddd-002', '2024-01-13 09:05:00'),
-- User 5: browsing with gap at seq 3,4 and duplicate at seq 8
(5, 'login', '{"method": "oauth", "ip": "10.10.0.15", "device": "Chrome/Linux"}', 1, 'ses-eee-001', '2024-01-13 16:00:00'),
(5, 'page_view', '{"url": "/dashboard", "load_time_ms": 290}', 2, 'ses-eee-001', '2024-01-13 16:01:00'),
-- gap: seq 3, 4 missing
(5, 'page_view', '{"url": "/products", "load_time_ms": 470}', 5, 'ses-eee-001', '2024-01-13 16:10:00'),
(5, 'page_view', '{"url": "/products/2", "load_time_ms": 330}', 6, 'ses-eee-001', '2024-01-13 16:12:00'),
(5, 'purchase', '{"product_id": 2, "amount": 29.99, "currency": "USD", "payment": "debit_card"}', 7, 'ses-eee-001', '2024-01-13 16:20:00'),
(5, 'page_view', '{"url": "/cart", "load_time_ms": 250}', 8, 'ses-eee-001', '2024-01-13 16:22:00'),
(5, 'page_view', '{"url": "/cart", "load_time_ms": 250}', 8, 'ses-eee-001', '2024-01-13 16:22:00'),
(5, 'logout', '{"reason": "user_action"}', 9, 'ses-eee-001', '2024-01-13 16:30:00'),
-- User 5, session 2
(5, 'login', '{"method": "oauth", "ip": "10.10.0.15", "device": "Chrome/Linux"}', 10, 'ses-eee-002', '2024-01-14 10:00:00'),
(5, 'page_view', '{"url": "/orders", "load_time_ms": 310}', 11, 'ses-eee-002', '2024-01-14 10:02:00'),
(5, 'error', '{"code": 404, "message": "Not found", "page": "/orders/999"}', 12, 'ses-eee-002', '2024-01-14 10:05:00'),
(5, 'logout', '{"reason": "user_action"}', 13, 'ses-eee-002', '2024-01-14 10:10:00');
