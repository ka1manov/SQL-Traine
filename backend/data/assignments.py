from dataclasses import dataclass


@dataclass
class AssignmentStep:
    step: int
    title: str
    description: str
    hint: str
    solution_sql: str | None = None


@dataclass
class Assignment:
    id: int
    title: str
    company: str
    description: str
    tables: list[str]
    steps: list[AssignmentStep]


ASSIGNMENTS: list[Assignment] = [
    Assignment(
        id=1,
        title="Spotify Streaming Analytics",
        company="Spotify",
        description="Analyze user listening patterns, find top artists, and identify genre trends.",
        tables=["streams"],
        steps=[
            AssignmentStep(1, "Top 3 Artists", "Find the top 3 artists by total stream count.",
                           "GROUP BY artist, ORDER BY count DESC, LIMIT 3",
                           "SELECT artist, COUNT(*) AS stream_count FROM streams GROUP BY artist ORDER BY stream_count DESC LIMIT 3"),
            AssignmentStep(2, "Genre Distribution", "Calculate the percentage of streams per genre.",
                           "Use COUNT and window function or subquery for total",
                           "SELECT genre, COUNT(*) AS cnt, ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM streams), 1) AS pct FROM streams GROUP BY genre ORDER BY pct DESC"),
            AssignmentStep(3, "Power Listeners", "Find users who listened to more than 3 unique artists.",
                           "GROUP BY user_id, HAVING COUNT(DISTINCT artist) > 3",
                           "SELECT user_id, COUNT(DISTINCT artist) AS artists FROM streams GROUP BY user_id HAVING COUNT(DISTINCT artist) > 3"),
            AssignmentStep(4, "Average Session Length", "Calculate average listening session length per user in minutes.",
                           "SUM(duration_sec) / 60.0, GROUP BY user_id",
                           "SELECT user_id, ROUND(AVG(duration_sec) / 60.0, 2) AS avg_minutes FROM streams GROUP BY user_id"),
        ],
    ),
    Assignment(
        id=2,
        title="Airbnb Booking Insights",
        company="Airbnb",
        description="Analyze booking patterns, revenue per city, and room type popularity.",
        tables=["bookings"],
        steps=[
            AssignmentStep(1, "Revenue by City", "Calculate total revenue per city (nights x price_per_night).",
                           "Use check_out - check_in for nights",
                           "SELECT city, SUM((check_out - check_in) * price_per_night) AS total_revenue FROM bookings GROUP BY city ORDER BY total_revenue DESC"),
            AssignmentStep(2, "Average Stay Duration", "Find average number of nights per room type.",
                           "GROUP BY room_type, AVG of date difference",
                           "SELECT room_type, ROUND(AVG(check_out - check_in), 1) AS avg_nights FROM bookings GROUP BY room_type"),
            AssignmentStep(3, "Most Profitable Room Type", "Which room type generates the most revenue overall?",
                           "SUM revenue, GROUP BY room_type, ORDER DESC",
                           "SELECT room_type, SUM((check_out - check_in) * price_per_night) AS revenue FROM bookings GROUP BY room_type ORDER BY revenue DESC LIMIT 1"),
            AssignmentStep(4, "Peak Booking Month", "Find the month with the most bookings.",
                           "DATE_TRUNC('month', check_in), COUNT, ORDER BY count DESC",
                           "SELECT DATE_TRUNC('month', check_in) AS month, COUNT(*) AS bookings FROM bookings GROUP BY month ORDER BY bookings DESC LIMIT 1"),
        ],
    ),
    Assignment(
        id=3,
        title="E-Commerce Dashboard",
        company="E-Commerce",
        description="Build key metrics for an online store: sales, customers, and product performance.",
        tables=["orders", "customers", "products"],
        steps=[
            AssignmentStep(1, "Monthly Revenue", "Calculate total revenue per month.",
                           "DATE_TRUNC on ordered_at, SUM(total)",
                           "SELECT DATE_TRUNC('month', ordered_at) AS month, SUM(total) AS revenue FROM orders GROUP BY month ORDER BY month"),
            AssignmentStep(2, "Best-Selling Products", "Find top 5 products by quantity sold.",
                           "JOIN products, SUM(quantity), LIMIT 5",
                           "SELECT p.name, SUM(o.quantity) AS total_qty FROM orders o JOIN products p ON o.product_id = p.id GROUP BY p.name ORDER BY total_qty DESC LIMIT 5"),
            AssignmentStep(3, "Customer Segments", "Categorize customers by total spend: Bronze (<500), Silver (500-2000), Gold (>2000).",
                           "Use CASE with SUM of order totals",
                           "SELECT c.name, SUM(o.total) AS total_spent, CASE WHEN SUM(o.total) > 2000 THEN 'Gold' WHEN SUM(o.total) >= 500 THEN 'Silver' ELSE 'Bronze' END AS segment FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.name"),
            AssignmentStep(4, "Repeat Customers", "Find customers who ordered more than 2 times.",
                           "GROUP BY customer_id, HAVING COUNT(*) > 2",
                           "SELECT c.name, COUNT(*) AS order_count FROM orders o JOIN customers c ON o.customer_id = c.id GROUP BY c.name HAVING COUNT(*) > 2"),
        ],
    ),
]
