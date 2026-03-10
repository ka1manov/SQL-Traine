from dataclasses import dataclass


@dataclass
class InterviewQuestion:
    id: int
    title: str
    description: str
    company_tags: list[str]
    pattern: str
    difficulty: str
    tables: list[str]
    solution_sql: str
    hint: str | None = None
    explanation: str = ""


# ============================================================
# 1-4: Top-N per group
# ============================================================

q1 = InterviewQuestion(
    id=1,
    title="Top 2 Earners per Department",
    description=(
        "For each department, find the top 2 employees by salary. "
        "Return the department name, employee full name, and salary. "
        "Order by department name, then salary descending."
    ),
    company_tags=["Google", "Meta"],
    pattern="Top-N per group",
    difficulty="medium",
    tables=["employees", "departments"],
    solution_sql="""\
WITH ranked AS (
    SELECT
        d.name AS department,
        e.first_name || ' ' || e.last_name AS employee_name,
        e.salary,
        ROW_NUMBER() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) AS rn
    FROM employees e
    JOIN departments d ON d.id = e.department_id
)
SELECT department, employee_name, salary
FROM ranked
WHERE rn <= 2
ORDER BY department, salary DESC;\
""",
    hint="Use ROW_NUMBER() partitioned by department_id and ordered by salary DESC, then filter rn <= 2.",
    explanation=(
        "We join employees with departments to get department names. "
        "A CTE with ROW_NUMBER() partitioned by department_id assigns a rank per department. "
        "Filtering rn <= 2 keeps only the top 2 earners in each department. "
        "The final ORDER BY ensures results are grouped by department and sorted by salary."
    ),
)

q2 = InterviewQuestion(
    id=2,
    title="Largest Order per Customer",
    description=(
        "For each customer, find their single largest order by total amount. "
        "Return the customer name, order id, total, and ordered_at. "
        "If a customer has no orders, exclude them."
    ),
    company_tags=["Amazon", "Stripe"],
    pattern="Top-N per group",
    difficulty="easy",
    tables=["orders", "customers"],
    solution_sql="""\
WITH ranked AS (
    SELECT
        c.name AS customer_name,
        o.id AS order_id,
        o.total,
        o.ordered_at,
        ROW_NUMBER() OVER (PARTITION BY o.customer_id ORDER BY o.total DESC) AS rn
    FROM orders o
    JOIN customers c ON c.id = o.customer_id
)
SELECT customer_name, order_id, total, ordered_at
FROM ranked
WHERE rn = 1
ORDER BY total DESC;\
""",
    hint="Use ROW_NUMBER() partitioned by customer_id, ordered by total DESC, then pick rn = 1.",
    explanation=(
        "We join orders and customers to get customer names. "
        "ROW_NUMBER() partitioned by customer_id with ORDER BY total DESC assigns rank 1 to the largest order. "
        "Filtering rn = 1 gives exactly one row per customer. "
        "Customers with no orders are excluded by the inner join."
    ),
)

q3 = InterviewQuestion(
    id=3,
    title="Most Streamed Song per Genre",
    description=(
        "Find the most-streamed song in each genre (by count of streams). "
        "Return genre, song, artist, and stream_count. "
        "Break ties alphabetically by song name."
    ),
    company_tags=["Netflix", "Apple"],
    pattern="Top-N per group",
    difficulty="easy",
    tables=["streams"],
    solution_sql="""\
WITH song_counts AS (
    SELECT
        genre,
        song,
        artist,
        COUNT(*) AS stream_count,
        ROW_NUMBER() OVER (
            PARTITION BY genre
            ORDER BY COUNT(*) DESC, song ASC
        ) AS rn
    FROM streams
    GROUP BY genre, song, artist
)
SELECT genre, song, artist, stream_count
FROM song_counts
WHERE rn = 1
ORDER BY genre;\
""",
    hint="GROUP BY genre, song, artist first to get counts, then use ROW_NUMBER() partitioned by genre.",
    explanation=(
        "First we aggregate streams by genre, song, and artist to get the stream_count. "
        "Then ROW_NUMBER() partitioned by genre with ORDER BY count DESC and song ASC ranks songs within each genre. "
        "Filtering rn = 1 keeps only the top song per genre. "
        "Ties are broken alphabetically by song name as specified."
    ),
)

q4 = InterviewQuestion(
    id=4,
    title="Most Expensive Booking per City",
    description=(
        "For each city, find the booking with the highest total cost "
        "(price_per_night * number of nights). Return city, guest_name, room_type, "
        "total_cost, and nights_stayed. Order by total_cost descending."
    ),
    company_tags=["Airbnb", "Uber"],
    pattern="Top-N per group",
    difficulty="medium",
    tables=["bookings"],
    solution_sql="""\
WITH booking_costs AS (
    SELECT
        city,
        guest_name,
        room_type,
        (check_out - check_in) AS nights_stayed,
        price_per_night * (check_out - check_in) AS total_cost,
        ROW_NUMBER() OVER (
            PARTITION BY city
            ORDER BY price_per_night * (check_out - check_in) DESC
        ) AS rn
    FROM bookings
)
SELECT city, guest_name, room_type, total_cost, nights_stayed
FROM booking_costs
WHERE rn = 1
ORDER BY total_cost DESC;\
""",
    hint="Calculate total_cost as price_per_night * (check_out - check_in), then rank per city.",
    explanation=(
        "In PostgreSQL, subtracting two DATE columns yields an integer number of days. "
        "We compute total_cost as price_per_night multiplied by nights_stayed. "
        "ROW_NUMBER() partitioned by city and ordered by total_cost DESC ranks bookings within each city. "
        "Filtering rn = 1 gives the most expensive booking per city."
    ),
)

# ============================================================
# 5-8: Running totals / Cumulative sums
# ============================================================

q5 = InterviewQuestion(
    id=5,
    title="Cumulative Order Revenue",
    description=(
        "Calculate a running total of order revenue (total column) over time. "
        "Return order_id, ordered_at, total, and cumulative_revenue. "
        "Order by ordered_at ascending."
    ),
    company_tags=["Stripe", "Amazon"],
    pattern="Running totals / Cumulative sums",
    difficulty="easy",
    tables=["orders"],
    solution_sql="""\
SELECT
    id AS order_id,
    ordered_at,
    total,
    SUM(total) OVER (ORDER BY ordered_at, id) AS cumulative_revenue
FROM orders
ORDER BY ordered_at, id;\
""",
    hint="Use SUM() as a window function with ORDER BY ordered_at to get a running total.",
    explanation=(
        "SUM(total) OVER (ORDER BY ordered_at, id) computes a cumulative sum over all preceding rows. "
        "The default window frame is RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW. "
        "We include id in the ORDER BY to break ties for orders at the same timestamp. "
        "This gives a monotonically increasing running total of revenue."
    ),
)

q6 = InterviewQuestion(
    id=6,
    title="Cumulative Salary Increases per Employee",
    description=(
        "For each salary change, compute the cumulative salary increase amount for that employee. "
        "Return employee_id, changed_at, old_salary, new_salary, raise_amount, "
        "and cumulative_raise. Order by employee_id, changed_at."
    ),
    company_tags=["Google", "LinkedIn"],
    pattern="Running totals / Cumulative sums",
    difficulty="medium",
    tables=["salaries_log"],
    solution_sql="""\
SELECT
    employee_id,
    changed_at,
    old_salary,
    new_salary,
    (new_salary - old_salary) AS raise_amount,
    SUM(new_salary - old_salary) OVER (
        PARTITION BY employee_id
        ORDER BY changed_at
    ) AS cumulative_raise
FROM salaries_log
ORDER BY employee_id, changed_at;\
""",
    hint="Compute the raise_amount as new_salary - old_salary, then use SUM() OVER partitioned by employee_id.",
    explanation=(
        "Each row in salaries_log represents a salary change event. "
        "We compute raise_amount as new_salary minus old_salary for each change. "
        "SUM() OVER (PARTITION BY employee_id ORDER BY changed_at) accumulates raises per employee over time. "
        "This shows how each employee's total raise has grown with each salary adjustment."
    ),
)

q7 = InterviewQuestion(
    id=7,
    title="Running Subscription Revenue by Plan",
    description=(
        "For each subscription plan, calculate the running total of subscription price as new "
        "subscriptions are added over time. Return plan, started_at, price, "
        "and running_plan_revenue. Order by plan, started_at."
    ),
    company_tags=["Netflix", "Uber"],
    pattern="Running totals / Cumulative sums",
    difficulty="easy",
    tables=["subscriptions"],
    solution_sql="""\
SELECT
    plan,
    started_at,
    price,
    SUM(price) OVER (
        PARTITION BY plan
        ORDER BY started_at
    ) AS running_plan_revenue
FROM subscriptions
ORDER BY plan, started_at;\
""",
    hint="Use SUM(price) OVER partitioned by plan, ordered by started_at.",
    explanation=(
        "We partition the window by plan so that each plan type has its own running total. "
        "ORDER BY started_at within each partition ensures chronological accumulation. "
        "Each row shows the cumulative revenue from that plan up to and including the current subscription. "
        "This reveals how each plan's revenue grows over time as new subscribers join."
    ),
)

q8 = InterviewQuestion(
    id=8,
    title="Cumulative Listening Time per User",
    description=(
        "For each user, compute a cumulative total of duration_sec as they stream songs over time. "
        "Return user_id, streamed_at, song, duration_sec, and cumulative_listen_sec. "
        "Order by user_id, streamed_at."
    ),
    company_tags=["Apple", "Twitter/X"],
    pattern="Running totals / Cumulative sums",
    difficulty="easy",
    tables=["streams"],
    solution_sql="""\
SELECT
    user_id,
    streamed_at,
    song,
    duration_sec,
    SUM(duration_sec) OVER (
        PARTITION BY user_id
        ORDER BY streamed_at
    ) AS cumulative_listen_sec
FROM streams
ORDER BY user_id, streamed_at;\
""",
    hint="Use SUM(duration_sec) OVER partitioned by user_id, ordered by streamed_at.",
    explanation=(
        "We partition the window by user_id so each user gets their own running total. "
        "ORDER BY streamed_at ensures streams are accumulated in chronological order. "
        "The cumulative_listen_sec column shows total listening time up to and including each stream. "
        "This is useful for tracking user engagement over time."
    ),
)

# ============================================================
# 9-12: Gap & Island analysis
# ============================================================

q9 = InterviewQuestion(
    id=9,
    title="Identify User Activity Gaps in Clickstream",
    description=(
        "Find gaps in user activity where a user had no clickstream events for more than "
        "24 hours between consecutive events. Return user_id, previous_event_time, "
        "next_event_time, and gap_hours. Order by gap_hours descending."
    ),
    company_tags=["Meta", "Twitter/X"],
    pattern="Gap & Island analysis",
    difficulty="medium",
    tables=["clickstream"],
    solution_sql="""\
WITH ordered_events AS (
    SELECT
        user_id,
        created_at,
        LEAD(created_at) OVER (PARTITION BY user_id ORDER BY created_at) AS next_event_time
    FROM clickstream
)
SELECT
    user_id,
    created_at AS previous_event_time,
    next_event_time,
    EXTRACT(EPOCH FROM (next_event_time - created_at)) / 3600.0 AS gap_hours
FROM ordered_events
WHERE next_event_time IS NOT NULL
  AND EXTRACT(EPOCH FROM (next_event_time - created_at)) / 3600.0 > 24
ORDER BY gap_hours DESC;\
""",
    hint="Use LEAD() to get the next event timestamp per user, then compute the time difference.",
    explanation=(
        "LEAD(created_at) OVER (PARTITION BY user_id ORDER BY created_at) gets the next event time for each user. "
        "We compute the gap in hours using EXTRACT(EPOCH FROM ...) to get seconds, then divide by 3600. "
        "Filtering for gaps > 24 hours identifies significant activity pauses. "
        "The last event per user has a NULL next_event_time and is excluded."
    ),
)

q10 = InterviewQuestion(
    id=10,
    title="Consecutive Streaming Days (Islands)",
    description=(
        "Find 'islands' of consecutive streaming days for each user. A consecutive streak "
        "is a series of days with no gaps. Return user_id, streak_start, streak_end, "
        "and streak_days. Order by streak_days descending."
    ),
    company_tags=["Google", "Amazon"],
    pattern="Gap & Island analysis",
    difficulty="hard",
    tables=["streams"],
    solution_sql="""\
WITH daily_streams AS (
    SELECT DISTINCT
        user_id,
        streamed_at::date AS stream_date
    FROM streams
),
grouped AS (
    SELECT
        user_id,
        stream_date,
        stream_date - (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY stream_date))::int AS grp
    FROM daily_streams
)
SELECT
    user_id,
    MIN(stream_date) AS streak_start,
    MAX(stream_date) AS streak_end,
    COUNT(*) AS streak_days
FROM grouped
GROUP BY user_id, grp
ORDER BY streak_days DESC, user_id;\
""",
    hint="Cast streamed_at to date, deduplicate, then use the ROW_NUMBER() subtraction trick to identify islands.",
    explanation=(
        "First we extract distinct streaming dates per user. "
        "The classic gap-and-island trick subtracts ROW_NUMBER() from the date: "
        "consecutive dates produce the same group value (grp). "
        "Grouping by user_id and grp, we get the start, end, and length of each streak. "
        "Longer streaks indicate more engaged users."
    ),
)

q11 = InterviewQuestion(
    id=11,
    title="Order Gaps per Customer",
    description=(
        "For each customer, find gaps between consecutive orders that exceed 30 days. "
        "Return customer_id, customer name, previous_order_date, next_order_date, "
        "and gap_days. Order by gap_days descending."
    ),
    company_tags=["Amazon", "Uber"],
    pattern="Gap & Island analysis",
    difficulty="hard",
    tables=["orders", "customers"],
    solution_sql="""\
WITH ordered AS (
    SELECT
        o.customer_id,
        c.name AS customer_name,
        o.ordered_at,
        LEAD(o.ordered_at) OVER (PARTITION BY o.customer_id ORDER BY o.ordered_at) AS next_order_at
    FROM orders o
    JOIN customers c ON c.id = o.customer_id
)
SELECT
    customer_id,
    customer_name,
    ordered_at AS previous_order_date,
    next_order_at AS next_order_date,
    EXTRACT(DAY FROM (next_order_at - ordered_at))::int AS gap_days
FROM ordered
WHERE next_order_at IS NOT NULL
  AND EXTRACT(DAY FROM (next_order_at - ordered_at)) > 30
ORDER BY gap_days DESC;\
""",
    hint="Use LEAD() to get the next order timestamp per customer, then filter where the gap exceeds 30 days.",
    explanation=(
        "LEAD() gets each customer's next order date. "
        "EXTRACT(DAY FROM ...) computes the number of days between consecutive orders. "
        "We filter for gaps exceeding 30 days to find lapsed purchase patterns. "
        "This is useful for identifying at-risk customers who may need re-engagement campaigns."
    ),
)

q12 = InterviewQuestion(
    id=12,
    title="Active Subscription Periods (Islands)",
    description=(
        "Identify continuous periods where each customer had at least one active subscription. "
        "Overlapping or adjacent subscriptions should be merged into a single period. "
        "Return customer_id, period_start, and period_end."
    ),
    company_tags=["Stripe", "LinkedIn"],
    pattern="Gap & Island analysis",
    difficulty="expert",
    tables=["subscriptions"],
    solution_sql="""\
WITH sub_periods AS (
    SELECT
        customer_id,
        started_at,
        COALESCE(ended_at, CURRENT_DATE::TIMESTAMP) AS ended_at
    FROM subscriptions
),
with_prev AS (
    SELECT
        customer_id,
        started_at,
        ended_at,
        LAG(ended_at) OVER (PARTITION BY customer_id ORDER BY started_at) AS prev_ended
    FROM sub_periods
),
islands AS (
    SELECT
        customer_id,
        started_at,
        ended_at,
        CASE
            WHEN prev_ended IS NULL OR started_at > prev_ended THEN 1
            ELSE 0
        END AS new_island
    FROM with_prev
),
grouped AS (
    SELECT
        customer_id,
        started_at,
        ended_at,
        SUM(new_island) OVER (PARTITION BY customer_id ORDER BY started_at) AS island_id
    FROM islands
)
SELECT
    customer_id,
    MIN(started_at) AS period_start,
    MAX(ended_at) AS period_end
FROM grouped
GROUP BY customer_id, island_id
ORDER BY customer_id, period_start;\
""",
    hint="Use LAG() to detect overlaps, flag new islands, then use a running SUM to assign island IDs.",
    explanation=(
        "First, we treat NULL ended_at as NOW() for active subscriptions. "
        "LAG(ended_at) gives the previous subscription's end date per customer. "
        "If the current start is after the previous end, it begins a new island. "
        "A cumulative SUM of the new_island flag assigns a unique island_id. "
        "Finally, grouping by island_id and taking MIN/MAX gives the merged period boundaries."
    ),
)

# ============================================================
# 13-16: Funnel analysis
# ============================================================

q13 = InterviewQuestion(
    id=13,
    title="Clickstream Conversion Funnel",
    description=(
        "Build a conversion funnel from the clickstream data showing how many unique users "
        "reached each stage: home -> products -> cart -> checkout. "
        "Return step_name and user_count. Order by the funnel sequence."
    ),
    company_tags=["Meta", "Google"],
    pattern="Funnel analysis",
    difficulty="medium",
    tables=["clickstream"],
    solution_sql="""\
WITH funnel AS (
    SELECT
        COUNT(DISTINCT CASE WHEN page = '/home' THEN user_id END) AS home_users,
        COUNT(DISTINCT CASE WHEN page = '/products' THEN user_id END) AS products_users,
        COUNT(DISTINCT CASE WHEN page = '/cart' THEN user_id END) AS cart_users,
        COUNT(DISTINCT CASE WHEN page = '/checkout' THEN user_id END) AS checkout_users
    FROM clickstream
)
SELECT step_name, user_count
FROM (
    SELECT 1 AS step_order, 'home' AS step_name, home_users AS user_count FROM funnel
    UNION ALL
    SELECT 2, 'products', products_users FROM funnel
    UNION ALL
    SELECT 3, 'cart', cart_users FROM funnel
    UNION ALL
    SELECT 4, 'checkout', checkout_users FROM funnel
) steps
ORDER BY step_order;\
""",
    hint="Use conditional COUNT(DISTINCT) with CASE WHEN for each funnel step, then unpivot into rows.",
    explanation=(
        "We use conditional aggregation with COUNT(DISTINCT CASE WHEN ...) to count unique users at each funnel stage. "
        "Each page corresponds to a funnel step: /home, /products, /cart, /checkout. "
        "UNION ALL unpivots the columns into rows for a clean funnel representation. "
        "A step_order column ensures the funnel steps are displayed in the correct sequence."
    ),
)

q14 = InterviewQuestion(
    id=14,
    title="Order-to-Invoice Funnel",
    description=(
        "Analyze the order-to-payment funnel. Show how many orders were placed, "
        "how many received an invoice, and how many invoices were paid. "
        "Return step_name and order_count."
    ),
    company_tags=["Stripe", "Amazon"],
    pattern="Funnel analysis",
    difficulty="easy",
    tables=["orders", "invoices"],
    solution_sql="""\
SELECT step_name, order_count
FROM (
    SELECT 1 AS step_order, 'orders_placed' AS step_name, COUNT(*) AS order_count
    FROM orders
    UNION ALL
    SELECT 2, 'invoiced', COUNT(DISTINCT i.order_id)
    FROM invoices i
    UNION ALL
    SELECT 3, 'paid', COUNT(DISTINCT i.order_id)
    FROM invoices i
    WHERE i.paid = TRUE
) funnel
ORDER BY step_order;\
""",
    hint="Count orders at each stage: all orders, orders with invoices, orders with paid invoices.",
    explanation=(
        "The first step counts all placed orders. "
        "The second step counts distinct order_ids that appear in the invoices table. "
        "The third step further filters to only paid invoices. "
        "This gives a clear picture of drop-off from order placement to payment completion."
    ),
)

q15 = InterviewQuestion(
    id=15,
    title="A/B Test Conversion Funnel by Variant",
    description=(
        "For each test_name and variant, calculate the total users, converted users, "
        "conversion rate, and average revenue per converted user. "
        "Return test_name, variant, total_users, converted_users, conversion_rate, avg_revenue. "
        "Order by test_name, variant."
    ),
    company_tags=["Meta", "LinkedIn"],
    pattern="Funnel analysis",
    difficulty="medium",
    tables=["ab_tests"],
    solution_sql="""\
SELECT
    test_name,
    variant,
    COUNT(*) AS total_users,
    COUNT(*) FILTER (WHERE converted) AS converted_users,
    ROUND(COUNT(*) FILTER (WHERE converted)::numeric / COUNT(*), 4) AS conversion_rate,
    ROUND(AVG(revenue) FILTER (WHERE converted), 2) AS avg_revenue
FROM ab_tests
GROUP BY test_name, variant
ORDER BY test_name, variant;\
""",
    hint="Use FILTER (WHERE converted) clause with COUNT and AVG for clean conditional aggregation.",
    explanation=(
        "PostgreSQL's FILTER clause is a clean alternative to CASE WHEN for conditional aggregation. "
        "COUNT(*) FILTER (WHERE converted) counts only users who converted. "
        "Dividing by total COUNT(*) gives the conversion rate. "
        "AVG(revenue) FILTER (WHERE converted) computes average revenue only among converters."
    ),
)

q16 = InterviewQuestion(
    id=16,
    title="Subscription Plan Upgrade Funnel",
    description=(
        "Identify customers who started with a 'basic' plan and later upgraded to 'premium' or "
        "'enterprise'. Return customer_id, first_basic_start, upgrade_plan, upgrade_date. "
        "Order by upgrade_date."
    ),
    company_tags=["Uber", "Netflix"],
    pattern="Funnel analysis",
    difficulty="hard",
    tables=["subscriptions"],
    solution_sql="""\
WITH first_basic AS (
    SELECT
        customer_id,
        MIN(started_at) AS first_basic_start
    FROM subscriptions
    WHERE plan = 'basic'
    GROUP BY customer_id
),
upgrades AS (
    SELECT
        s.customer_id,
        fb.first_basic_start,
        s.plan AS upgrade_plan,
        s.started_at AS upgrade_date,
        ROW_NUMBER() OVER (PARTITION BY s.customer_id ORDER BY s.started_at) AS rn
    FROM subscriptions s
    JOIN first_basic fb ON fb.customer_id = s.customer_id
    WHERE s.plan IN ('premium', 'enterprise')
      AND s.started_at > fb.first_basic_start
)
SELECT customer_id, first_basic_start, upgrade_plan, upgrade_date
FROM upgrades
WHERE rn = 1
ORDER BY upgrade_date;\
""",
    hint="Find each customer's first basic subscription start, then look for later premium/enterprise subscriptions.",
    explanation=(
        "The first CTE finds the earliest basic subscription start date per customer. "
        "The second CTE joins subscriptions that are premium or enterprise and started after the basic plan. "
        "ROW_NUMBER() ensures we pick only the first upgrade event if multiple exist. "
        "This gives the conversion funnel from basic to upgraded plans."
    ),
)

# ============================================================
# 17-19: Cohort retention
# ============================================================

q17 = InterviewQuestion(
    id=17,
    title="Monthly Subscription Cohort Retention",
    description=(
        "Build a cohort retention table for subscribers. Define the cohort by the month a customer "
        "first subscribed. For each cohort, show how many customers placed an order in months 0, 1, 2, "
        "and 3 after their cohort month. Return cohort_month, month_offset, and retained_customers."
    ),
    company_tags=["Google", "Uber"],
    pattern="Cohort retention",
    difficulty="hard",
    tables=["subscriptions", "orders"],
    solution_sql="""\
WITH cohorts AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', MIN(started_at)) AS cohort_month
    FROM subscriptions
    GROUP BY customer_id
),
order_months AS (
    SELECT
        o.customer_id,
        DATE_TRUNC('month', o.ordered_at) AS order_month
    FROM orders o
)
SELECT
    c.cohort_month,
    EXTRACT(MONTH FROM AGE(om.order_month, c.cohort_month))::int
      + EXTRACT(YEAR FROM AGE(om.order_month, c.cohort_month))::int * 12 AS month_offset,
    COUNT(DISTINCT c.customer_id) AS retained_customers
FROM cohorts c
JOIN order_months om ON om.customer_id = c.customer_id
WHERE om.order_month >= c.cohort_month
GROUP BY c.cohort_month, month_offset
HAVING EXTRACT(MONTH FROM AGE(om.order_month, c.cohort_month))::int
      + EXTRACT(YEAR FROM AGE(om.order_month, c.cohort_month))::int * 12 <= 3
ORDER BY c.cohort_month, month_offset;\
""",
    hint="Define cohorts by MIN(started_at) month, then join with orders to compute month offsets.",
    explanation=(
        "The cohorts CTE assigns each customer to the month they first subscribed. "
        "order_months truncates order dates to month level. "
        "We join on customer_id and compute the month difference using AGE(). "
        "Grouping by cohort_month and month_offset with COUNT(DISTINCT customer_id) gives retention per cohort."
    ),
)

q18 = InterviewQuestion(
    id=18,
    title="Customer Registration Cohort Retention",
    description=(
        "Define customer cohorts by their registration month. For each cohort, count how many "
        "distinct customers placed at least one order in each subsequent month (month 0, 1, 2, 3). "
        "Return cohort_month, month_offset, and active_customers."
    ),
    company_tags=["Amazon", "Meta"],
    pattern="Cohort retention",
    difficulty="hard",
    tables=["customers", "orders"],
    solution_sql="""\
WITH cohorts AS (
    SELECT
        id AS customer_id,
        DATE_TRUNC('month', registered_at) AS cohort_month
    FROM customers
),
activity AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', ordered_at) AS activity_month
    FROM orders
)
SELECT
    c.cohort_month,
    (EXTRACT(YEAR FROM AGE(a.activity_month, c.cohort_month))::int * 12
     + EXTRACT(MONTH FROM AGE(a.activity_month, c.cohort_month))::int) AS month_offset,
    COUNT(DISTINCT c.customer_id) AS active_customers
FROM cohorts c
JOIN activity a ON a.customer_id = c.customer_id
WHERE a.activity_month >= c.cohort_month
GROUP BY c.cohort_month, month_offset
HAVING (EXTRACT(YEAR FROM AGE(a.activity_month, c.cohort_month))::int * 12
     + EXTRACT(MONTH FROM AGE(a.activity_month, c.cohort_month))::int) <= 3
ORDER BY c.cohort_month, month_offset;\
""",
    hint="Use DATE_TRUNC on registered_at for cohort month, then compute month offsets from order dates.",
    explanation=(
        "Customer cohorts are defined by truncating registered_at to month. "
        "We join with orders and truncate ordered_at to get the activity month. "
        "The month offset is calculated using AGE() to find the difference between activity and cohort months. "
        "Counting distinct customers per cohort and offset shows how retention decays over time."
    ),
)

q19 = InterviewQuestion(
    id=19,
    title="Clickstream Weekly Cohort Retention",
    description=(
        "Define user cohorts by the week of their first clickstream event. "
        "For each cohort, count users who returned in weeks 0, 1, and 2 after their first week. "
        "Return cohort_week, week_offset, and returning_users."
    ),
    company_tags=["Twitter/X", "Meta"],
    pattern="Cohort retention",
    difficulty="hard",
    tables=["clickstream"],
    solution_sql="""\
WITH cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('week', MIN(created_at)) AS cohort_week
    FROM clickstream
    GROUP BY user_id
),
weekly_activity AS (
    SELECT DISTINCT
        user_id,
        DATE_TRUNC('week', created_at) AS activity_week
    FROM clickstream
)
SELECT
    c.cohort_week,
    (EXTRACT(EPOCH FROM wa.activity_week - c.cohort_week) / 604800)::int AS week_offset,
    COUNT(DISTINCT c.user_id) AS returning_users
FROM cohorts c
JOIN weekly_activity wa ON wa.user_id = c.user_id
WHERE wa.activity_week >= c.cohort_week
  AND (EXTRACT(EPOCH FROM wa.activity_week - c.cohort_week) / 604800)::int <= 2
GROUP BY c.cohort_week, week_offset
ORDER BY c.cohort_week, week_offset;\
""",
    hint="Use DATE_TRUNC('week', ...) for weekly cohorts, then compute week offsets by dividing the day difference by 7.",
    explanation=(
        "The cohorts CTE finds each user's first week of activity. "
        "weekly_activity deduplicates user activity to distinct weeks. "
        "The week offset is computed by subtracting timestamps and dividing by 7 days. "
        "Grouping by cohort_week and week_offset with COUNT(DISTINCT user_id) gives weekly retention."
    ),
)

# ============================================================
# 20-23: Year-over-year / Period comparison
# ============================================================

q20 = InterviewQuestion(
    id=20,
    title="Month-over-Month Order Revenue Growth",
    description=(
        "Calculate monthly order revenue and the month-over-month growth percentage. "
        "Return month, monthly_revenue, prev_month_revenue, and growth_pct. "
        "Order by month."
    ),
    company_tags=["Amazon", "Stripe"],
    pattern="Year-over-year / Period comparison",
    difficulty="medium",
    tables=["orders"],
    solution_sql="""\
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', ordered_at) AS month,
        SUM(total) AS monthly_revenue
    FROM orders
    GROUP BY DATE_TRUNC('month', ordered_at)
)
SELECT
    month,
    monthly_revenue,
    LAG(monthly_revenue) OVER (ORDER BY month) AS prev_month_revenue,
    ROUND(
        (monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month))
        / LAG(monthly_revenue) OVER (ORDER BY month) * 100,
        2
    ) AS growth_pct
FROM monthly
ORDER BY month;\
""",
    hint="Aggregate by DATE_TRUNC('month', ordered_at), then use LAG() to get the previous month's revenue.",
    explanation=(
        "We first aggregate order totals into monthly revenue. "
        "LAG(monthly_revenue) OVER (ORDER BY month) retrieves the previous month's revenue. "
        "Growth percentage is computed as (current - previous) / previous * 100. "
        "The first month shows NULL for prev_month_revenue and growth_pct since there is no prior data."
    ),
)

q21 = InterviewQuestion(
    id=21,
    title="Salary Change Rate Comparison by Year",
    description=(
        "For each year, compute the average salary raise percentage from salary changes. "
        "Then compare each year's average raise with the previous year's. "
        "Return change_year, avg_raise_pct, prev_year_avg_raise_pct, and difference."
    ),
    company_tags=["LinkedIn", "Apple"],
    pattern="Year-over-year / Period comparison",
    difficulty="medium",
    tables=["salaries_log"],
    solution_sql="""\
WITH yearly AS (
    SELECT
        EXTRACT(YEAR FROM changed_at)::int AS change_year,
        ROUND(AVG((new_salary - old_salary) / old_salary * 100), 2) AS avg_raise_pct
    FROM salaries_log
    WHERE old_salary > 0
    GROUP BY EXTRACT(YEAR FROM changed_at)::int
)
SELECT
    change_year,
    avg_raise_pct,
    LAG(avg_raise_pct) OVER (ORDER BY change_year) AS prev_year_avg_raise_pct,
    ROUND(avg_raise_pct - LAG(avg_raise_pct) OVER (ORDER BY change_year), 2) AS difference
FROM yearly
ORDER BY change_year;\
""",
    hint="Aggregate raise percentages by year, then use LAG() to compare year-over-year.",
    explanation=(
        "We compute each raise as (new_salary - old_salary) / old_salary * 100 and average by year. "
        "LAG() retrieves the previous year's average raise percentage. "
        "The difference column shows whether raises are accelerating or decelerating. "
        "We guard against division by zero by filtering old_salary > 0."
    ),
)

q22 = InterviewQuestion(
    id=22,
    title="Subscription Revenue Period Comparison",
    description=(
        "Compare total active subscription revenue by quarter. For each quarter, show the total "
        "price of subscriptions that were active during that quarter, the previous quarter's total, "
        "and the change. Return quarter, quarterly_revenue, prev_quarter_revenue, and change_pct."
    ),
    company_tags=["Netflix", "Uber"],
    pattern="Year-over-year / Period comparison",
    difficulty="hard",
    tables=["subscriptions"],
    solution_sql="""\
WITH quarters AS (
    SELECT generate_series(
        DATE_TRUNC('quarter', '2023-01-01'::timestamp),
        DATE_TRUNC('quarter', '2024-06-01'::timestamp),
        '3 months'::interval
    ) AS quarter_start
),
quarterly_rev AS (
    SELECT
        q.quarter_start,
        COALESCE(SUM(s.price), 0) AS quarterly_revenue
    FROM quarters q
    LEFT JOIN subscriptions s
        ON s.started_at < q.quarter_start + INTERVAL '3 months'
        AND (s.ended_at IS NULL OR s.ended_at >= q.quarter_start)
    GROUP BY q.quarter_start
)
SELECT
    quarter_start AS quarter,
    quarterly_revenue,
    LAG(quarterly_revenue) OVER (ORDER BY quarter_start) AS prev_quarter_revenue,
    ROUND(
        CASE
            WHEN LAG(quarterly_revenue) OVER (ORDER BY quarter_start) > 0
            THEN (quarterly_revenue - LAG(quarterly_revenue) OVER (ORDER BY quarter_start))
                 / LAG(quarterly_revenue) OVER (ORDER BY quarter_start) * 100
        END,
        2
    ) AS change_pct
FROM quarterly_rev
ORDER BY quarter_start;\
""",
    hint="Use generate_series to create quarters, then join subscriptions that overlap each quarter.",
    explanation=(
        "generate_series creates a sequence of quarter start dates. "
        "We join subscriptions that overlap each quarter: started before quarter end and not ended before quarter start. "
        "LAG() compares each quarter to the previous one. "
        "The CASE guard prevents division by zero when the previous quarter has no revenue."
    ),
)

q23 = InterviewQuestion(
    id=23,
    title="Booking Revenue Month-over-Month by City",
    description=(
        "For each city and month, compute the total booking revenue (price_per_night * nights). "
        "Then show the month-over-month change. Return city, month, monthly_revenue, "
        "prev_month_revenue, and mom_change."
    ),
    company_tags=["Airbnb", "Google"],
    pattern="Year-over-year / Period comparison",
    difficulty="medium",
    tables=["bookings"],
    solution_sql="""\
WITH monthly_booking AS (
    SELECT
        city,
        DATE_TRUNC('month', check_in) AS month,
        SUM(price_per_night * (check_out - check_in)) AS monthly_revenue
    FROM bookings
    GROUP BY city, DATE_TRUNC('month', check_in)
)
SELECT
    city,
    month,
    monthly_revenue,
    LAG(monthly_revenue) OVER (PARTITION BY city ORDER BY month) AS prev_month_revenue,
    monthly_revenue - LAG(monthly_revenue) OVER (PARTITION BY city ORDER BY month) AS mom_change
FROM monthly_booking
ORDER BY city, month;\
""",
    hint="Aggregate booking revenue by city and month, then use LAG() partitioned by city.",
    explanation=(
        "Revenue per booking is price_per_night * (check_out - check_in) days. "
        "We aggregate by city and month using DATE_TRUNC on check_in. "
        "LAG() is partitioned by city so each city's trend is tracked independently. "
        "mom_change shows the absolute revenue change between consecutive months per city."
    ),
)

# ============================================================
# 24-26: Deduplication
# ============================================================

q24 = InterviewQuestion(
    id=24,
    title="Deduplicate Employees by Email",
    description=(
        "If employees had duplicate email entries (hypothetically), write a query that keeps "
        "only the row with the lowest id for each email. Return all columns of the surviving rows. "
        "Order by id."
    ),
    company_tags=["Google", "Amazon"],
    pattern="Deduplication",
    difficulty="easy",
    tables=["employees"],
    solution_sql="""\
WITH ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) AS rn
    FROM employees
)
SELECT id, first_name, last_name, email, department_id, salary, hire_date, is_active
FROM ranked
WHERE rn = 1
ORDER BY id;\
""",
    hint="Use ROW_NUMBER() partitioned by email, ordered by id, and keep rn = 1.",
    explanation=(
        "ROW_NUMBER() assigns a sequential number within each email partition. "
        "ORDER BY id ensures the earliest-created record gets rn = 1. "
        "Filtering rn = 1 effectively deduplicates by keeping one row per email. "
        "This is a standard deduplication pattern used in ETL and data cleaning pipelines."
    ),
)

q25 = InterviewQuestion(
    id=25,
    title="Remove Duplicate Clickstream Events",
    description=(
        "Identify and remove duplicate clickstream events where the same user visited the same "
        "page with the same action within the same session. Keep only the earliest event. "
        "Return id, session_id, user_id, page, action, and created_at of the surviving rows."
    ),
    company_tags=["Meta", "Twitter/X"],
    pattern="Deduplication",
    difficulty="easy",
    tables=["clickstream"],
    solution_sql="""\
WITH ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY session_id, user_id, page, action
            ORDER BY created_at
        ) AS rn
    FROM clickstream
)
SELECT id, session_id, user_id, page, action, created_at
FROM ranked
WHERE rn = 1
ORDER BY created_at;\
""",
    hint="Partition by session_id, user_id, page, and action; order by created_at; keep rn = 1.",
    explanation=(
        "We define duplicates as rows sharing the same session_id, user_id, page, and action. "
        "ROW_NUMBER() ordered by created_at assigns rn = 1 to the earliest occurrence. "
        "Filtering rn = 1 keeps only the first event of each duplicate group. "
        "This is essential for accurate funnel analysis where duplicate events can inflate counts."
    ),
)

q26 = InterviewQuestion(
    id=26,
    title="Deduplicate Streams Keeping Latest",
    description=(
        "Remove duplicate stream records where the same user listened to the same song by the "
        "same artist. Keep only the most recent stream. Return id, user_id, song, artist, "
        "and streamed_at."
    ),
    company_tags=["Netflix", "Uber"],
    pattern="Deduplication",
    difficulty="hard",
    tables=["streams"],
    solution_sql="""\
WITH ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY user_id, song, artist
            ORDER BY streamed_at DESC
        ) AS rn
    FROM streams
)
SELECT id, user_id, song, artist, streamed_at
FROM ranked
WHERE rn = 1
ORDER BY user_id, streamed_at DESC;\
""",
    hint="Partition by user_id, song, artist; order by streamed_at DESC; keep rn = 1.",
    explanation=(
        "Duplicates are defined as same user_id, song, and artist combinations. "
        "ROW_NUMBER() with ORDER BY streamed_at DESC ranks the most recent stream as rn = 1. "
        "Filtering rn = 1 keeps only the latest stream per unique combination. "
        "This is useful when building 'recently played' features."
    ),
)

# ============================================================
# 27-30: Pivot / Conditional aggregation
# ============================================================

q27 = InterviewQuestion(
    id=27,
    title="Order Status Pivot by Month",
    description=(
        "Create a pivot table showing the count of orders by status for each month. "
        "Columns should be: month, pending, shipped, completed. Order by month."
    ),
    company_tags=["Amazon", "Uber"],
    pattern="Pivot / Conditional aggregation",
    difficulty="medium",
    tables=["orders"],
    solution_sql="""\
SELECT
    DATE_TRUNC('month', ordered_at) AS month,
    COUNT(*) FILTER (WHERE status = 'pending') AS pending,
    COUNT(*) FILTER (WHERE status = 'shipped') AS shipped,
    COUNT(*) FILTER (WHERE status = 'completed') AS completed
FROM orders
GROUP BY DATE_TRUNC('month', ordered_at)
ORDER BY month;\
""",
    hint="Use COUNT(*) FILTER (WHERE status = '...') for each status column.",
    explanation=(
        "PostgreSQL's FILTER clause enables clean conditional aggregation without CASE WHEN. "
        "Each status becomes a separate column using COUNT(*) FILTER (WHERE status = ...). "
        "Grouping by DATE_TRUNC('month', ordered_at) aggregates by calendar month. "
        "This pivot table shows order fulfillment trends over time."
    ),
)

q28 = InterviewQuestion(
    id=28,
    title="A/B Test Results Pivot",
    description=(
        "Create a comparison table for each A/B test showing variant A vs B metrics side by side. "
        "Return test_name, a_users, b_users, a_conversions, b_conversions, a_revenue, b_revenue. "
        "Order by test_name."
    ),
    company_tags=["Meta", "LinkedIn"],
    pattern="Pivot / Conditional aggregation",
    difficulty="medium",
    tables=["ab_tests"],
    solution_sql="""\
SELECT
    test_name,
    COUNT(*) FILTER (WHERE variant = 'A') AS a_users,
    COUNT(*) FILTER (WHERE variant = 'B') AS b_users,
    COUNT(*) FILTER (WHERE variant = 'A' AND converted) AS a_conversions,
    COUNT(*) FILTER (WHERE variant = 'B' AND converted) AS b_conversions,
    COALESCE(SUM(revenue) FILTER (WHERE variant = 'A'), 0) AS a_revenue,
    COALESCE(SUM(revenue) FILTER (WHERE variant = 'B'), 0) AS b_revenue
FROM ab_tests
GROUP BY test_name
ORDER BY test_name;\
""",
    hint="Use FILTER (WHERE variant = 'A') and FILTER (WHERE variant = 'B') to split metrics by variant.",
    explanation=(
        "Each metric is split into A and B columns using the FILTER clause. "
        "COUNT with the converted flag gives conversion counts per variant. "
        "SUM(revenue) per variant shows total revenue generated. "
        "This side-by-side comparison makes it easy to evaluate which variant performs better."
    ),
)

q29 = InterviewQuestion(
    id=29,
    title="Employee Count Pivot by Department and Salary Band",
    description=(
        "Create a pivot table showing the number of employees in each department broken down by "
        "salary band: '<70k', '70k-100k', '>100k'. Return department_name and the three band columns. "
        "Order by department_name."
    ),
    company_tags=["Google", "Uber"],
    pattern="Pivot / Conditional aggregation",
    difficulty="medium",
    tables=["employees", "departments"],
    solution_sql="""\
SELECT
    d.name AS department_name,
    COUNT(*) FILTER (WHERE e.salary < 70000) AS "under_70k",
    COUNT(*) FILTER (WHERE e.salary >= 70000 AND e.salary <= 100000) AS "70k_to_100k",
    COUNT(*) FILTER (WHERE e.salary > 100000) AS "over_100k"
FROM employees e
JOIN departments d ON d.id = e.department_id
GROUP BY d.name
ORDER BY d.name;\
""",
    hint="Use FILTER with salary range conditions for each band column.",
    explanation=(
        "We join employees with departments to get department names. "
        "Three salary bands are defined: under 70k, 70k-100k, and over 100k. "
        "COUNT(*) FILTER with the appropriate range condition creates each band column. "
        "This gives a quick overview of salary distribution across departments."
    ),
)

q30 = InterviewQuestion(
    id=30,
    title="Booking Revenue Pivot by Room Type and City",
    description=(
        "Create a pivot table showing total booking revenue by city, with columns for each room type: "
        "standard, deluxe, suite. Revenue = price_per_night * nights. "
        "Return city, standard_revenue, deluxe_revenue, suite_revenue. Order by city."
    ),
    company_tags=["Airbnb", "Google"],
    pattern="Pivot / Conditional aggregation",
    difficulty="medium",
    tables=["bookings"],
    solution_sql="""\
SELECT
    city,
    COALESCE(SUM(price_per_night * (check_out - check_in))
        FILTER (WHERE room_type = 'standard'), 0) AS standard_revenue,
    COALESCE(SUM(price_per_night * (check_out - check_in))
        FILTER (WHERE room_type = 'deluxe'), 0) AS deluxe_revenue,
    COALESCE(SUM(price_per_night * (check_out - check_in))
        FILTER (WHERE room_type = 'suite'), 0) AS suite_revenue
FROM bookings
GROUP BY city
ORDER BY city;\
""",
    hint="Compute revenue as price_per_night * (check_out - check_in) inside SUM FILTER per room type.",
    explanation=(
        "Revenue per booking is price_per_night multiplied by the number of nights. "
        "SUM with FILTER splits the revenue by room_type into separate columns. "
        "COALESCE ensures 0 appears instead of NULL when a city has no bookings of a particular type. "
        "This pivot makes it easy to compare revenue contribution by room type across cities."
    ),
)

# ============================================================
# 31-33: Cumulative distribution / Percentiles
# ============================================================

q31 = InterviewQuestion(
    id=31,
    title="Employee Salary Percentile Ranks",
    description=(
        "Compute the percentile rank of each employee's salary within their department. "
        "Return department name, employee name, salary, and percentile_rank (0 to 1). "
        "Order by department name, percentile_rank descending."
    ),
    company_tags=["Google", "Meta"],
    pattern="Cumulative distribution / Percentiles",
    difficulty="hard",
    tables=["employees", "departments"],
    solution_sql="""\
SELECT
    d.name AS department,
    e.first_name || ' ' || e.last_name AS employee_name,
    e.salary,
    PERCENT_RANK() OVER (
        PARTITION BY e.department_id ORDER BY e.salary
    ) AS percentile_rank
FROM employees e
JOIN departments d ON d.id = e.department_id
ORDER BY d.name, percentile_rank DESC;\
""",
    hint="Use PERCENT_RANK() partitioned by department_id, ordered by salary.",
    explanation=(
        "PERCENT_RANK() computes the relative rank of each row as (rank - 1) / (total_rows - 1). "
        "Partitioning by department_id gives a percentile within each department. "
        "A value of 1.0 means the highest salary in that department. "
        "This is commonly used for compensation benchmarking."
    ),
)

q32 = InterviewQuestion(
    id=32,
    title="Order Value Distribution with NTILE",
    description=(
        "Divide all orders into 4 quartiles by total amount. For each quartile show the "
        "quartile number, min total, max total, and order count."
    ),
    company_tags=["Stripe", "Uber"],
    pattern="Cumulative distribution / Percentiles",
    difficulty="hard",
    tables=["orders"],
    solution_sql="""\
WITH quartiled AS (
    SELECT
        id AS order_id,
        total,
        NTILE(4) OVER (ORDER BY total) AS quartile
    FROM orders
)
SELECT
    quartile,
    MIN(total) AS min_total,
    MAX(total) AS max_total,
    COUNT(*) AS order_count
FROM quartiled
GROUP BY quartile
ORDER BY quartile;\
""",
    hint="Use NTILE(4) OVER (ORDER BY total) to assign quartiles, then aggregate per quartile.",
    explanation=(
        "NTILE(4) divides the ordered set of rows into 4 approximately equal groups. "
        "Orders are sorted by total amount, so quartile 1 has the lowest values. "
        "Aggregating by quartile shows the range and count in each bucket. "
        "This helps understand the distribution of order values."
    ),
)

q33 = InterviewQuestion(
    id=33,
    title="Booking Price Percentile by City",
    description=(
        "For each city, compute the median (50th percentile) and 90th percentile of "
        "price_per_night using PERCENTILE_CONT. Return city, median_price, and p90_price. "
        "Order by median_price descending."
    ),
    company_tags=["Airbnb", "Amazon"],
    pattern="Cumulative distribution / Percentiles",
    difficulty="hard",
    tables=["bookings"],
    solution_sql="""\
SELECT
    city,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price_per_night) AS median_price,
    PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY price_per_night) AS p90_price
FROM bookings
GROUP BY city
ORDER BY median_price DESC;\
""",
    hint="Use PERCENTILE_CONT() WITHIN GROUP as an ordered-set aggregate function, grouped by city.",
    explanation=(
        "PERCENTILE_CONT is an ordered-set aggregate that interpolates the exact percentile value. "
        "0.5 gives the median; 0.9 gives the 90th percentile. "
        "Grouping by city computes these statistics independently per city. "
        "This is useful for pricing strategy and understanding market segments."
    ),
)

# ============================================================
# 34-37: Moving averages
# ============================================================

q34 = InterviewQuestion(
    id=34,
    title="3-Order Moving Average of Revenue",
    description=(
        "Compute a 3-order moving average of the total column for each order, sorted by ordered_at. "
        "Return order_id, ordered_at, total, and moving_avg_3. "
        "The moving average should include the current row and the two preceding rows."
    ),
    company_tags=["Stripe", "Amazon"],
    pattern="Moving averages",
    difficulty="medium",
    tables=["orders"],
    solution_sql="""\
SELECT
    id AS order_id,
    ordered_at,
    total,
    ROUND(
        AVG(total) OVER (
            ORDER BY ordered_at, id
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS moving_avg_3
FROM orders
ORDER BY ordered_at, id;\
""",
    hint="Use AVG() OVER with ROWS BETWEEN 2 PRECEDING AND CURRENT ROW.",
    explanation=(
        "The window frame ROWS BETWEEN 2 PRECEDING AND CURRENT ROW includes three rows total. "
        "AVG(total) over this frame gives a trailing 3-order moving average. "
        "ORDER BY ordered_at, id ensures consistent ordering. "
        "For the first two rows, fewer than three rows are available, so the average uses what exists."
    ),
)

q35 = InterviewQuestion(
    id=35,
    title="7-Day Moving Average of Streams per User",
    description=(
        "For each user, compute a 7-day moving average of daily stream counts. "
        "Return user_id, stream_date, daily_count, and moving_avg_7d. "
        "Order by user_id, stream_date."
    ),
    company_tags=["Google", "Apple"],
    pattern="Moving averages",
    difficulty="hard",
    tables=["streams"],
    solution_sql="""\
WITH daily AS (
    SELECT
        user_id,
        streamed_at::date AS stream_date,
        COUNT(*) AS daily_count
    FROM streams
    GROUP BY user_id, streamed_at::date
)
SELECT
    user_id,
    stream_date,
    daily_count,
    ROUND(
        AVG(daily_count) OVER (
            PARTITION BY user_id
            ORDER BY stream_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS moving_avg_7d
FROM daily
ORDER BY user_id, stream_date;\
""",
    hint="First aggregate daily counts, then apply AVG() OVER with ROWS BETWEEN 6 PRECEDING AND CURRENT ROW.",
    explanation=(
        "We first aggregate streams to get daily_count per user per date. "
        "The window ROWS BETWEEN 6 PRECEDING AND CURRENT ROW covers 7 days. "
        "AVG over this frame gives the 7-day trailing moving average. "
        "Note: this uses row-based framing, so gaps in dates would affect the result. "
        "For exact calendar-day windows, RANGE-based framing would be needed."
    ),
)

q36 = InterviewQuestion(
    id=36,
    title="Moving Average of Booking Revenue by City",
    description=(
        "For each city, compute a 3-booking moving average of total booking revenue "
        "(price_per_night * nights). Return city, check_in, guest_name, booking_revenue, "
        "and moving_avg_3. Order by city, check_in."
    ),
    company_tags=["Uber", "Airbnb"],
    pattern="Moving averages",
    difficulty="medium",
    tables=["bookings"],
    solution_sql="""\
SELECT
    city,
    check_in,
    guest_name,
    price_per_night * (check_out - check_in) AS booking_revenue,
    ROUND(
        AVG(price_per_night * (check_out - check_in)) OVER (
            PARTITION BY city
            ORDER BY check_in
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS moving_avg_3
FROM bookings
ORDER BY city, check_in;\
""",
    hint="Compute revenue inline and use it in AVG() OVER with a 3-row window partitioned by city.",
    explanation=(
        "Booking revenue is calculated as price_per_night * (check_out - check_in). "
        "AVG() OVER with ROWS BETWEEN 2 PRECEDING AND CURRENT ROW computes a 3-booking trailing average. "
        "PARTITION BY city ensures each city's average is independent. "
        "This smooths out short-term fluctuations and reveals revenue trends per city."
    ),
)

q37 = InterviewQuestion(
    id=37,
    title="Subscription Revenue Moving Average by Plan",
    description=(
        "For each plan type, compute a 2-subscription moving average of subscription price "
        "as new subscriptions are added. Return plan, started_at, price, and moving_avg_2. "
        "Order by plan, started_at."
    ),
    company_tags=["LinkedIn", "Twitter/X"],
    pattern="Moving averages",
    difficulty="medium",
    tables=["subscriptions"],
    solution_sql="""\
SELECT
    plan,
    started_at,
    price,
    ROUND(
        AVG(price) OVER (
            PARTITION BY plan
            ORDER BY started_at
            ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS moving_avg_2
FROM subscriptions
ORDER BY plan, started_at;\
""",
    hint="Use AVG(price) OVER with ROWS BETWEEN 1 PRECEDING AND CURRENT ROW, partitioned by plan.",
    explanation=(
        "ROWS BETWEEN 1 PRECEDING AND CURRENT ROW creates a 2-row window. "
        "AVG(price) over this frame gives a simple trailing 2-period moving average. "
        "Partitioning by plan keeps each plan type's trend separate. "
        "For the first subscription of each plan, the average equals the price itself."
    ),
)

# ============================================================
# 38-40: Sessionization
# ============================================================

q38 = InterviewQuestion(
    id=38,
    title="Clickstream Session Duration and Depth",
    description=(
        "For each session in the clickstream, compute the session duration (time from first to last event) "
        "and session depth (number of distinct pages visited). "
        "Return session_id, user_id, session_start, session_end, session_duration_sec, and pages_visited. "
        "Order by session_duration_sec descending."
    ),
    company_tags=["Google", "Meta"],
    pattern="Sessionization",
    difficulty="medium",
    tables=["clickstream"],
    solution_sql="""\
SELECT
    session_id,
    MIN(user_id) AS user_id,
    MIN(created_at) AS session_start,
    MAX(created_at) AS session_end,
    EXTRACT(EPOCH FROM (MAX(created_at) - MIN(created_at)))::int AS session_duration_sec,
    COUNT(DISTINCT page) AS pages_visited
FROM clickstream
GROUP BY session_id
ORDER BY session_duration_sec DESC;\
""",
    hint="Group by session_id, then use MIN/MAX on created_at for duration, and COUNT(DISTINCT page) for depth.",
    explanation=(
        "Since clickstream already has session_id, we can group directly by it. "
        "MIN and MAX of created_at give the session boundaries. "
        "EXTRACT(EPOCH FROM ...) converts the interval to seconds. "
        "COUNT(DISTINCT page) measures how many unique pages the user visited in that session."
    ),
)

q39 = InterviewQuestion(
    id=39,
    title="Sessionize Streams by 30-Minute Gaps",
    description=(
        "Create sessions from the streams table where a new session starts when there is a gap of "
        "more than 30 minutes between consecutive streams for the same user. "
        "Return user_id, session_num, session_start, session_end, and songs_in_session. "
        "Order by user_id, session_num."
    ),
    company_tags=["Netflix", "Amazon"],
    pattern="Sessionization",
    difficulty="expert",
    tables=["streams"],
    solution_sql="""\
WITH with_prev AS (
    SELECT
        user_id,
        song,
        streamed_at,
        LAG(streamed_at) OVER (PARTITION BY user_id ORDER BY streamed_at) AS prev_at
    FROM streams
),
flagged AS (
    SELECT
        user_id,
        song,
        streamed_at,
        CASE
            WHEN prev_at IS NULL
                 OR EXTRACT(EPOCH FROM (streamed_at - prev_at)) > 1800
            THEN 1 ELSE 0
        END AS new_session
    FROM with_prev
),
sessioned AS (
    SELECT
        user_id,
        song,
        streamed_at,
        SUM(new_session) OVER (PARTITION BY user_id ORDER BY streamed_at) AS session_num
    FROM flagged
)
SELECT
    user_id,
    session_num,
    MIN(streamed_at) AS session_start,
    MAX(streamed_at) AS session_end,
    COUNT(*) AS songs_in_session
FROM sessioned
GROUP BY user_id, session_num
ORDER BY user_id, session_num;\
""",
    hint="Use LAG() to find the gap, flag new sessions when gap > 30 min, then use a running SUM to assign session numbers.",
    explanation=(
        "LAG(streamed_at) gives the previous stream time per user. "
        "If the gap exceeds 1800 seconds (30 minutes), we flag a new session. "
        "A cumulative SUM of the new_session flag assigns incrementing session numbers. "
        "Grouping by session_num and taking MIN/MAX of streamed_at gives session boundaries. "
        "COUNT(*) gives the number of songs in each session."
    ),
)

q40 = InterviewQuestion(
    id=40,
    title="Sessionize Orders by Customer with 7-Day Gap",
    description=(
        "Group orders into purchase sessions per customer, where a new session begins when "
        "there is a gap of more than 7 days between consecutive orders. "
        "Return customer_id, session_num, session_start, session_end, orders_in_session, "
        "and session_revenue. Order by customer_id, session_num."
    ),
    company_tags=["Amazon", "Uber"],
    pattern="Sessionization",
    difficulty="hard",
    tables=["orders"],
    solution_sql="""\
WITH with_prev AS (
    SELECT
        customer_id,
        ordered_at,
        total,
        LAG(ordered_at) OVER (PARTITION BY customer_id ORDER BY ordered_at) AS prev_ordered
    FROM orders
),
flagged AS (
    SELECT
        customer_id,
        ordered_at,
        total,
        CASE
            WHEN prev_ordered IS NULL
                 OR EXTRACT(EPOCH FROM (ordered_at - prev_ordered)) > 7 * 86400
            THEN 1 ELSE 0
        END AS new_session
    FROM with_prev
),
sessioned AS (
    SELECT
        customer_id,
        ordered_at,
        total,
        SUM(new_session) OVER (PARTITION BY customer_id ORDER BY ordered_at) AS session_num
    FROM flagged
)
SELECT
    customer_id,
    session_num,
    MIN(ordered_at) AS session_start,
    MAX(ordered_at) AS session_end,
    COUNT(*) AS orders_in_session,
    SUM(total) AS session_revenue
FROM sessioned
GROUP BY customer_id, session_num
ORDER BY customer_id, session_num;\
""",
    hint="Use the same sessionization pattern: LAG for gaps, flag new sessions at > 7 days, cumulative SUM for session IDs.",
    explanation=(
        "This uses the same sessionization technique as stream sessions. "
        "LAG(ordered_at) gives the previous order time per customer. "
        "A gap exceeding 7 days (604800 seconds) starts a new session. "
        "The cumulative SUM assigns session numbers, and final aggregation gives session metrics. "
        "This reveals customer buying patterns and burst purchasing behavior."
    ),
)

# ============================================================
# 41-44: Customer segmentation / RFM
# ============================================================

q41 = InterviewQuestion(
    id=41,
    title="RFM Segmentation for Customers",
    description=(
        "Perform RFM (Recency, Frequency, Monetary) analysis on customers. "
        "Compute days since last order as recency, total order count as frequency, "
        "and total spend as monetary. Assign each metric a score of 1-4 using NTILE. "
        "Return customer_id, customer name, recency_days, frequency, monetary, "
        "r_score, f_score, m_score. Order by monetary descending."
    ),
    company_tags=["Meta", "Uber"],
    pattern="Customer segmentation / RFM",
    difficulty="hard",
    tables=["customers", "orders"],
    solution_sql="""\
WITH rfm AS (
    SELECT
        c.id AS customer_id,
        c.name AS customer_name,
        EXTRACT(DAY FROM (NOW() - MAX(o.ordered_at)))::int AS recency_days,
        COUNT(o.id) AS frequency,
        COALESCE(SUM(o.total), 0) AS monetary
    FROM customers c
    LEFT JOIN orders o ON o.customer_id = c.id
    GROUP BY c.id, c.name
),
scored AS (
    SELECT
        customer_id,
        customer_name,
        recency_days,
        frequency,
        monetary,
        NTILE(4) OVER (ORDER BY recency_days DESC) AS r_score,
        NTILE(4) OVER (ORDER BY frequency) AS f_score,
        NTILE(4) OVER (ORDER BY monetary) AS m_score
    FROM rfm
)
SELECT *
FROM scored
ORDER BY monetary DESC;\
""",
    hint="Compute recency, frequency, monetary metrics, then use NTILE(4) to assign scores. Lower recency = better, so order DESC.",
    explanation=(
        "Recency: days since the last order (lower is better, so we reverse-sort for NTILE). "
        "Frequency: total number of orders per customer. "
        "Monetary: total spend across all orders. "
        "NTILE(4) divides customers into quartiles for each metric. "
        "High r_score, f_score, and m_score identify the best customers."
    ),
)

q42 = InterviewQuestion(
    id=42,
    title="A/B Test User Segments by Revenue",
    description=(
        "Segment A/B test users into 'high_value' (total revenue > 100), 'medium_value' "
        "(revenue between 1 and 100), and 'no_conversion' (revenue = 0). "
        "For each test_name and segment, count users. "
        "Return test_name, segment, user_count. Order by test_name, segment."
    ),
    company_tags=["Google", "LinkedIn"],
    pattern="Customer segmentation / RFM",
    difficulty="medium",
    tables=["ab_tests"],
    solution_sql="""\
WITH user_segments AS (
    SELECT
        test_name,
        user_id,
        SUM(revenue) AS total_revenue,
        CASE
            WHEN SUM(revenue) > 100 THEN 'high_value'
            WHEN SUM(revenue) > 0 THEN 'medium_value'
            ELSE 'no_conversion'
        END AS segment
    FROM ab_tests
    GROUP BY test_name, user_id
)
SELECT
    test_name,
    segment,
    COUNT(*) AS user_count
FROM user_segments
GROUP BY test_name, segment
ORDER BY test_name, segment;\
""",
    hint="Use CASE WHEN on SUM(revenue) to define segments, then count users per segment per test.",
    explanation=(
        "First we compute total revenue per user per test. "
        "CASE WHEN classifies each user into high_value, medium_value, or no_conversion. "
        "Grouping by test_name and segment gives the distribution of user types per test. "
        "This helps identify whether a test variant attracts higher-value users."
    ),
)

q43 = InterviewQuestion(
    id=43,
    title="Listener Engagement Segments",
    description=(
        "Segment stream users into engagement tiers based on total streams: "
        "'power_user' (10+ streams), 'regular' (5-9 streams), 'casual' (1-4 streams). "
        "Return segment, user_count, avg_total_duration_sec. Order by avg_total_duration_sec descending."
    ),
    company_tags=["Twitter/X", "Meta"],
    pattern="Customer segmentation / RFM",
    difficulty="expert",
    tables=["streams"],
    solution_sql="""\
WITH user_stats AS (
    SELECT
        user_id,
        COUNT(*) AS total_streams,
        SUM(duration_sec) AS total_duration_sec,
        CASE
            WHEN COUNT(*) >= 10 THEN 'power_user'
            WHEN COUNT(*) >= 5 THEN 'regular'
            ELSE 'casual'
        END AS segment
    FROM streams
    GROUP BY user_id
)
SELECT
    segment,
    COUNT(*) AS user_count,
    ROUND(AVG(total_duration_sec), 0) AS avg_total_duration_sec
FROM user_stats
GROUP BY segment
ORDER BY avg_total_duration_sec DESC;\
""",
    hint="Aggregate per user to get stream count, classify with CASE WHEN, then aggregate per segment.",
    explanation=(
        "First we compute total streams and duration per user. "
        "CASE WHEN classifies users into power_user, regular, or casual segments. "
        "A second aggregation counts users per segment and computes average total listening time. "
        "This reveals how different engagement levels correlate with total consumption."
    ),
)

q44 = InterviewQuestion(
    id=44,
    title="Customer Lifetime Value Segments",
    description=(
        "Compute a simplified customer lifetime value (CLV) as total order revenue plus "
        "total subscription payments. Segment customers into 'platinum' (CLV > 2000), "
        "'gold' (1000-2000), 'silver' (1-999), and 'inactive' (0). "
        "Return customer_name, order_revenue, subscription_revenue, clv, and segment."
    ),
    company_tags=["Stripe", "Uber"],
    pattern="Customer segmentation / RFM",
    difficulty="expert",
    tables=["customers", "orders", "subscriptions"],
    solution_sql="""\
WITH order_rev AS (
    SELECT
        customer_id,
        COALESCE(SUM(total), 0) AS order_revenue
    FROM orders
    GROUP BY customer_id
),
sub_rev AS (
    SELECT
        customer_id,
        COALESCE(SUM(price), 0) AS subscription_revenue
    FROM subscriptions
    GROUP BY customer_id
),
clv AS (
    SELECT
        c.id AS customer_id,
        c.name AS customer_name,
        COALESCE(o.order_revenue, 0) AS order_revenue,
        COALESCE(s.subscription_revenue, 0) AS subscription_revenue,
        COALESCE(o.order_revenue, 0) + COALESCE(s.subscription_revenue, 0) AS clv
    FROM customers c
    LEFT JOIN order_rev o ON o.customer_id = c.id
    LEFT JOIN sub_rev s ON s.customer_id = c.id
)
SELECT
    customer_name,
    order_revenue,
    subscription_revenue,
    clv,
    CASE
        WHEN clv > 2000 THEN 'platinum'
        WHEN clv >= 1000 THEN 'gold'
        WHEN clv > 0 THEN 'silver'
        ELSE 'inactive'
    END AS segment
FROM clv
ORDER BY clv DESC;\
""",
    hint="Compute order revenue and subscription revenue separately, join with customers, sum for CLV, then classify.",
    explanation=(
        "Two CTEs compute total order revenue and total subscription revenue per customer. "
        "LEFT JOINs from customers ensure every customer appears, even those with no orders or subscriptions. "
        "CLV is the sum of both revenue sources. "
        "CASE WHEN assigns a tier label based on CLV thresholds. "
        "This is a simplified but practical approach to customer lifetime value analysis."
    ),
)

# ============================================================
# 45-47: Self-joins & hierarchies
# ============================================================

q45 = InterviewQuestion(
    id=45,
    title="Employees Earning More Than Department Average",
    description=(
        "Find all employees whose salary is above the average salary in their department. "
        "Return department name, employee full name, salary, and dept_avg_salary. "
        "Order by department name, salary descending."
    ),
    company_tags=["Google", "Amazon"],
    pattern="Self-joins & hierarchies",
    difficulty="medium",
    tables=["employees", "departments"],
    solution_sql="""\
WITH dept_avg AS (
    SELECT
        department_id,
        AVG(salary) AS dept_avg_salary
    FROM employees
    GROUP BY department_id
)
SELECT
    d.name AS department,
    e.first_name || ' ' || e.last_name AS employee_name,
    e.salary,
    ROUND(da.dept_avg_salary, 2) AS dept_avg_salary
FROM employees e
JOIN departments d ON d.id = e.department_id
JOIN dept_avg da ON da.department_id = e.department_id
WHERE e.salary > da.dept_avg_salary
ORDER BY d.name, e.salary DESC;\
""",
    hint="Compute department averages in a CTE, then join and filter employees above average.",
    explanation=(
        "The CTE computes the average salary per department. "
        "We join this back to employees and departments. "
        "The WHERE clause filters to employees earning above their department's average. "
        "This is a classic self-referencing comparison pattern common in interviews."
    ),
)

q46 = InterviewQuestion(
    id=46,
    title="Employees with Multiple Salary Raises",
    description=(
        "Find employees who have had more than one salary change. For each such employee, "
        "show their name, number of raises, total cumulative raise amount, and the percentage "
        "increase from their earliest old_salary to their latest new_salary."
    ),
    company_tags=["LinkedIn", "Meta"],
    pattern="Self-joins & hierarchies",
    difficulty="hard",
    tables=["salaries_log", "employees"],
    solution_sql="""\
WITH raise_stats AS (
    SELECT
        employee_id,
        COUNT(*) AS raise_count,
        SUM(new_salary - old_salary) AS total_raise,
        MIN(changed_at) AS first_change,
        MAX(changed_at) AS last_change
    FROM salaries_log
    GROUP BY employee_id
    HAVING COUNT(*) > 1
),
first_last AS (
    SELECT
        rs.employee_id,
        rs.raise_count,
        rs.total_raise,
        sl_first.old_salary AS earliest_salary,
        sl_last.new_salary AS latest_salary
    FROM raise_stats rs
    JOIN salaries_log sl_first
        ON sl_first.employee_id = rs.employee_id AND sl_first.changed_at = rs.first_change
    JOIN salaries_log sl_last
        ON sl_last.employee_id = rs.employee_id AND sl_last.changed_at = rs.last_change
)
SELECT
    e.first_name || ' ' || e.last_name AS employee_name,
    fl.raise_count,
    fl.total_raise,
    ROUND((fl.latest_salary - fl.earliest_salary) / fl.earliest_salary * 100, 2) AS pct_increase
FROM first_last fl
JOIN employees e ON e.id = fl.employee_id
ORDER BY pct_increase DESC;\
""",
    hint="Aggregate salaries_log to find employees with multiple changes, then self-join to get first and last salary values.",
    explanation=(
        "The raise_stats CTE finds employees with more than one salary change and their first/last change dates. "
        "We self-join salaries_log to get the old_salary from the first change and new_salary from the last. "
        "The percentage increase is computed from earliest old to latest new salary. "
        "This reveals which employees have had the most career salary growth."
    ),
)

q47 = InterviewQuestion(
    id=47,
    title="Customers Who Ordered the Same Product Twice",
    description=(
        "Find all customers who ordered the same product more than once. "
        "Return customer_name, product_name, times_ordered, and total_quantity. "
        "Order by times_ordered descending."
    ),
    company_tags=["Amazon", "Meta"],
    pattern="Self-joins & hierarchies",
    difficulty="medium",
    tables=["orders", "customers", "products"],
    solution_sql="""\
SELECT
    c.name AS customer_name,
    p.name AS product_name,
    COUNT(*) AS times_ordered,
    SUM(o.quantity) AS total_quantity
FROM orders o
JOIN customers c ON c.id = o.customer_id
JOIN products p ON p.id = o.product_id
GROUP BY c.name, p.name
HAVING COUNT(*) > 1
ORDER BY times_ordered DESC;\
""",
    hint="Join orders with customers and products, group by customer and product, filter with HAVING COUNT(*) > 1.",
    explanation=(
        "We join orders, customers, and products to get names. "
        "Grouping by customer_name and product_name aggregates repeat purchases. "
        "HAVING COUNT(*) > 1 filters to products ordered more than once by the same customer. "
        "SUM(quantity) shows the total units purchased across all repeat orders."
    ),
)

# ============================================================
# 48-50: Complex multi-table analytics
# ============================================================

q48 = InterviewQuestion(
    id=48,
    title="Full Customer 360 Dashboard",
    description=(
        "Build a comprehensive customer profile combining data from multiple tables. "
        "For each customer, show: name, city, total orders, total revenue, "
        "active subscriptions count, last order date, and days since registration. "
        "Order by total_revenue descending."
    ),
    company_tags=["Google", "Stripe"],
    pattern="Complex multi-table analytics",
    difficulty="expert",
    tables=["customers", "orders", "subscriptions"],
    solution_sql="""\
WITH order_stats AS (
    SELECT
        customer_id,
        COUNT(*) AS total_orders,
        SUM(total) AS total_revenue,
        MAX(ordered_at) AS last_order_date
    FROM orders
    GROUP BY customer_id
),
sub_stats AS (
    SELECT
        customer_id,
        COUNT(*) FILTER (WHERE is_active) AS active_subs
    FROM subscriptions
    GROUP BY customer_id
)
SELECT
    c.name AS customer_name,
    c.city,
    COALESCE(os.total_orders, 0) AS total_orders,
    COALESCE(os.total_revenue, 0) AS total_revenue,
    COALESCE(ss.active_subs, 0) AS active_subscriptions,
    os.last_order_date,
    EXTRACT(DAY FROM (NOW() - c.registered_at))::int AS days_since_registration
FROM customers c
LEFT JOIN order_stats os ON os.customer_id = c.id
LEFT JOIN sub_stats ss ON ss.customer_id = c.id
ORDER BY total_revenue DESC;\
""",
    hint="Use CTEs for order stats and subscription stats, then LEFT JOIN everything to the customers table.",
    explanation=(
        "order_stats aggregates total orders, revenue, and last order date per customer. "
        "sub_stats counts active subscriptions per customer. "
        "LEFT JOINs from customers ensure all customers appear, even inactive ones. "
        "COALESCE handles NULLs for customers with no orders or subscriptions. "
        "This gives a complete customer profile suitable for a dashboard."
    ),
)

q49 = InterviewQuestion(
    id=49,
    title="Revenue Attribution: Orders, Invoices, and Subscriptions",
    description=(
        "Compute a monthly revenue summary combining order revenue, paid invoice amounts, "
        "and subscription revenue. Return month, order_revenue, invoice_paid_revenue, "
        "subscription_revenue, and total_revenue. Order by month."
    ),
    company_tags=["Uber", "Amazon"],
    pattern="Complex multi-table analytics",
    difficulty="expert",
    tables=["orders", "invoices", "subscriptions"],
    solution_sql="""\
WITH months AS (
    SELECT generate_series(
        '2024-01-01'::timestamp,
        '2024-04-01'::timestamp,
        '1 month'::interval
    ) AS month
),
order_rev AS (
    SELECT
        DATE_TRUNC('month', ordered_at) AS month,
        SUM(total) AS order_revenue
    FROM orders
    GROUP BY DATE_TRUNC('month', ordered_at)
),
invoice_rev AS (
    SELECT
        DATE_TRUNC('month', issued_at) AS month,
        SUM(amount) FILTER (WHERE paid) AS invoice_paid_revenue
    FROM invoices
    GROUP BY DATE_TRUNC('month', issued_at)
),
sub_rev AS (
    SELECT
        m.month,
        SUM(s.price) AS subscription_revenue
    FROM months m
    JOIN subscriptions s
        ON s.started_at < m.month + INTERVAL '1 month'
        AND (s.ended_at IS NULL OR s.ended_at >= m.month)
    GROUP BY m.month
)
SELECT
    m.month,
    COALESCE(o.order_revenue, 0) AS order_revenue,
    COALESCE(i.invoice_paid_revenue, 0) AS invoice_paid_revenue,
    COALESCE(sr.subscription_revenue, 0) AS subscription_revenue,
    COALESCE(o.order_revenue, 0)
      + COALESCE(i.invoice_paid_revenue, 0)
      + COALESCE(sr.subscription_revenue, 0) AS total_revenue
FROM months m
LEFT JOIN order_rev o ON o.month = m.month
LEFT JOIN invoice_rev i ON i.month = m.month
LEFT JOIN sub_rev sr ON sr.month = m.month
ORDER BY m.month;\
""",
    hint="Create separate CTEs for each revenue source by month, then join them all on the month column.",
    explanation=(
        "We use generate_series to create a complete set of months. "
        "Each revenue source is aggregated by month in its own CTE. "
        "Subscription revenue includes subscriptions active during each month. "
        "LEFT JOINs and COALESCE ensure every month appears with zeroes where no data exists. "
        "The total_revenue sums all three sources for a complete financial picture."
    ),
)

q50 = InterviewQuestion(
    id=50,
    title="Cross-Domain Engagement Score",
    description=(
        "Build a unified engagement score per user combining clickstream depth, stream activity, "
        "and A/B test conversions. Score = (distinct_pages * 10) + (total_streams * 5) + "
        "(conversions * 20). Return user_id, distinct_pages, total_streams, conversions, "
        "and engagement_score. Only include users present in at least two of the three tables. "
        "Order by engagement_score descending."
    ),
    company_tags=["Google", "Meta"],
    pattern="Complex multi-table analytics",
    difficulty="expert",
    tables=["clickstream", "streams", "ab_tests"],
    solution_sql="""\
WITH click_stats AS (
    SELECT
        user_id,
        COUNT(DISTINCT page) AS distinct_pages
    FROM clickstream
    GROUP BY user_id
),
stream_stats AS (
    SELECT
        user_id,
        COUNT(*) AS total_streams
    FROM streams
    GROUP BY user_id
),
ab_stats AS (
    SELECT
        user_id,
        COUNT(*) FILTER (WHERE converted) AS conversions
    FROM ab_tests
    GROUP BY user_id
),
all_users AS (
    SELECT user_id FROM click_stats
    UNION
    SELECT user_id FROM stream_stats
    UNION
    SELECT user_id FROM ab_stats
),
combined AS (
    SELECT
        u.user_id,
        COALESCE(cs.distinct_pages, 0) AS distinct_pages,
        COALESCE(ss.total_streams, 0) AS total_streams,
        COALESCE(ab.conversions, 0) AS conversions,
        (CASE WHEN cs.user_id IS NOT NULL THEN 1 ELSE 0 END
         + CASE WHEN ss.user_id IS NOT NULL THEN 1 ELSE 0 END
         + CASE WHEN ab.user_id IS NOT NULL THEN 1 ELSE 0 END) AS tables_present
    FROM all_users u
    LEFT JOIN click_stats cs ON cs.user_id = u.user_id
    LEFT JOIN stream_stats ss ON ss.user_id = u.user_id
    LEFT JOIN ab_stats ab ON ab.user_id = u.user_id
)
SELECT
    user_id,
    distinct_pages,
    total_streams,
    conversions,
    (distinct_pages * 10) + (total_streams * 5) + (conversions * 20) AS engagement_score
FROM combined
WHERE tables_present >= 2
ORDER BY engagement_score DESC;\
""",
    hint="Aggregate each table per user, UNION user_ids, LEFT JOIN all stats, count table presence, and compute the score.",
    explanation=(
        "Each CTE aggregates a single metric per user: pages from clickstream, streams from streams, conversions from ab_tests. "
        "A UNION of all user_ids creates the complete user list. "
        "LEFT JOINs attach each metric, with COALESCE defaulting missing values to 0. "
        "We count how many source tables each user appears in (tables_present). "
        "Only users present in at least 2 tables are included, and the engagement score is computed from the formula."
    ),
)


# ============================================================
# 51-54: Sessionization (Uber, Netflix)
# ============================================================

q51 = InterviewQuestion(
    id=51,
    title="Session Duration from Event Log",
    description=(
        "For each session in the event_log table, calculate the number of events, "
        "session start time, session end time, and duration in seconds. "
        "Return session_id, user_id, event_count, session_start, session_end, duration_seconds. "
        "Order by session_start."
    ),
    company_tags=["Uber", "Netflix"],
    pattern="Sessionization",
    difficulty="medium",
    tables=["event_log"],
    solution_sql="""\
SELECT session_id, user_id, COUNT(*) AS event_count,
    MIN(created_at) AS session_start, MAX(created_at) AS session_end,
    EXTRACT(EPOCH FROM MAX(created_at) - MIN(created_at)) AS duration_seconds
FROM event_log
GROUP BY session_id, user_id
ORDER BY session_start;\
""",
    hint="GROUP BY session_id and user_id, use MIN/MAX for timestamps and EXTRACT(EPOCH FROM ...) for duration.",
    explanation="Grouping by session_id treats each session as a unit. MIN/MAX give first and last event timestamps. EXTRACT(EPOCH FROM interval) converts the time difference to seconds.",
)

q52 = InterviewQuestion(
    id=52,
    title="Purchase Sessions with Page Views",
    description=(
        "Find sessions that contain at least one purchase event. For each, show session_id, user_id, "
        "total purchase amount (from event_data JSONB), number of page_view events, and session duration "
        "in seconds. Order by session_id."
    ),
    company_tags=["Netflix", "Spotify"],
    pattern="Sessionization",
    difficulty="hard",
    tables=["event_log"],
    solution_sql="""\
WITH purchases AS (
    SELECT session_id, user_id,
        SUM((event_data->>'amount')::NUMERIC) AS total_purchase_amount
    FROM event_log WHERE event_type = 'purchase'
    GROUP BY session_id, user_id
),
session_stats AS (
    SELECT session_id, user_id,
        COUNT(*) FILTER (WHERE event_type = 'page_view') AS page_views_count,
        EXTRACT(EPOCH FROM MAX(created_at) - MIN(created_at)) AS duration_seconds
    FROM event_log GROUP BY session_id, user_id
)
SELECT s.session_id, s.user_id, p.total_purchase_amount,
    s.page_views_count, s.duration_seconds
FROM session_stats s
JOIN purchases p ON s.session_id = p.session_id AND s.user_id = p.user_id
ORDER BY s.session_id;\
""",
    hint="Use one CTE for purchase amounts (extract from JSONB), another for session stats with COUNT FILTER, then JOIN.",
    explanation="Combines JSONB extraction, FILTER aggregation, and sessionization. The JOIN naturally filters to purchase sessions only.",
)

q53 = InterviewQuestion(
    id=53,
    title="Average Session Length by User",
    description=(
        "Calculate each user's average session duration in seconds and total number of sessions. "
        "Only include sessions with at least 2 events. "
        "Return user_id, session_count, avg_duration_seconds. Order by avg_duration_seconds DESC."
    ),
    company_tags=["Uber", "Airbnb"],
    pattern="Sessionization",
    difficulty="medium",
    tables=["event_log"],
    solution_sql="""\
WITH sessions AS (
    SELECT user_id, session_id,
        EXTRACT(EPOCH FROM MAX(created_at) - MIN(created_at)) AS duration_seconds,
        COUNT(*) AS event_count
    FROM event_log
    GROUP BY user_id, session_id
    HAVING COUNT(*) >= 2
)
SELECT user_id, COUNT(*) AS session_count,
    ROUND(AVG(duration_seconds)::NUMERIC, 2) AS avg_duration_seconds
FROM sessions
GROUP BY user_id
ORDER BY avg_duration_seconds DESC;\
""",
    hint="First compute per-session duration with HAVING >= 2 events, then aggregate per user.",
    explanation="The CTE computes duration per session, filtering to multi-event sessions. The outer query averages these durations per user.",
)

# ============================================================
# 54-56: JSONB Extraction (Stripe, Airbnb)
# ============================================================

q54 = InterviewQuestion(
    id=54,
    title="Extract User Settings from JSONB",
    description=(
        "From user_profiles, extract the theme, plan, and email notification preference from the JSONB settings column. "
        "Return username, theme, plan, and email_notifications (boolean). Only include users where settings is not null. "
        "Order by username."
    ),
    company_tags=["Stripe", "Airbnb"],
    pattern="JSONB extraction",
    difficulty="easy",
    tables=["user_profiles"],
    solution_sql="""\
SELECT username,
    settings->>'theme' AS theme,
    settings->>'plan' AS plan,
    (settings->'notifications'->>'email')::BOOLEAN AS email_notifications
FROM user_profiles
WHERE settings IS NOT NULL
ORDER BY username;\
""",
    hint="Use ->> to extract JSONB text values. For nested keys, chain -> then ->>.",
    explanation="The -> operator returns a JSONB sub-object, while ->> extracts the value as text. Chain them to reach nested keys like settings->'notifications'->>'email'.",
)

q55 = InterviewQuestion(
    id=55,
    title="Tag Frequency Analysis",
    description=(
        "From user_profiles, unnest the tags array and count how many users have each tag. "
        "Return tag and user_count. Order by user_count DESC, tag ASC."
    ),
    company_tags=["Airbnb", "Stripe"],
    pattern="JSONB extraction",
    difficulty="easy",
    tables=["user_profiles"],
    solution_sql="""\
SELECT UNNEST(tags) AS tag, COUNT(*) AS user_count
FROM user_profiles
WHERE tags IS NOT NULL
GROUP BY tag
ORDER BY user_count DESC, tag ASC;\
""",
    hint="UNNEST expands the array into rows, then GROUP BY the unnested value.",
    explanation="UNNEST(tags) creates one row per tag per user. GROUP BY tag counts how many users have each tag.",
)

q56 = InterviewQuestion(
    id=56,
    title="JSONB Event Data Aggregation",
    description=(
        "From event_log, for each event_type, calculate the count and the average value of the "
        "'amount' field in event_data (only for events that have an amount). "
        "Return event_type, event_count, and avg_amount. Order by event_count DESC."
    ),
    company_tags=["Stripe", "Square"],
    pattern="JSONB extraction",
    difficulty="medium",
    tables=["event_log"],
    solution_sql="""\
SELECT event_type,
    COUNT(*) AS event_count,
    ROUND(AVG((event_data->>'amount')::NUMERIC), 2) AS avg_amount
FROM event_log
WHERE event_data->>'amount' IS NOT NULL
GROUP BY event_type
ORDER BY event_count DESC;\
""",
    hint="Extract amount with ->>, cast to NUMERIC, and use AVG. Filter where amount key exists.",
    explanation="The ->> operator extracts amount as text, which is cast to NUMERIC for aggregation. NULL is returned for events without the amount key, filtered by WHERE.",
)

# ============================================================
# 57-59: Gap & Island (Google, Amazon)
# ============================================================

q57 = InterviewQuestion(
    id=57,
    title="Find Missing Sequence Numbers",
    description=(
        "In the event_log table, find all missing seq_num values per user_id within each session. "
        "A missing seq_num is a gap between the minimum and maximum seq_num for that user+session. "
        "Return user_id, session_id, and missing_seq_num. Order by user_id, session_id, missing_seq_num."
    ),
    company_tags=["Google", "Amazon"],
    pattern="Gap & Island",
    difficulty="hard",
    tables=["event_log"],
    solution_sql="""\
WITH bounds AS (
    SELECT user_id, session_id, MIN(seq_num) AS min_seq, MAX(seq_num) AS max_seq
    FROM event_log GROUP BY user_id, session_id
),
all_seqs AS (
    SELECT b.user_id, b.session_id, g.n AS expected_seq
    FROM bounds b
    CROSS JOIN LATERAL generate_series(b.min_seq, b.max_seq) AS g(n)
)
SELECT a.user_id, a.session_id, a.expected_seq AS missing_seq_num
FROM all_seqs a
LEFT JOIN event_log e ON a.user_id = e.user_id AND a.session_id = e.session_id AND a.expected_seq = e.seq_num
WHERE e.seq_num IS NULL
ORDER BY a.user_id, a.session_id, a.expected_seq;\
""",
    hint="Generate the full expected sequence with generate_series between MIN and MAX seq_num, then LEFT JOIN to find gaps.",
    explanation="generate_series creates all expected sequence numbers. LEFT JOIN with the actual data reveals gaps where no matching row exists (e.seq_num IS NULL).",
)

q58 = InterviewQuestion(
    id=58,
    title="Consecutive Active Subscription Months",
    description=(
        "Find the longest streak of consecutive months where each customer had an active subscription. "
        "Return customer_id and longest_streak (number of months). Order by longest_streak DESC, customer_id."
    ),
    company_tags=["Amazon", "Google"],
    pattern="Gap & Island",
    difficulty="hard",
    tables=["subscriptions"],
    solution_sql="""\
WITH months AS (
    SELECT customer_id,
        generate_series(
            DATE_TRUNC('month', started_at),
            DATE_TRUNC('month', COALESCE(ended_at, CURRENT_DATE)),
            '1 month'::INTERVAL
        )::DATE AS active_month
    FROM subscriptions
),
distinct_months AS (
    SELECT DISTINCT customer_id, active_month FROM months
),
islands AS (
    SELECT customer_id, active_month,
        active_month - (ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY active_month) * INTERVAL '1 month') AS grp
    FROM distinct_months
)
SELECT customer_id, MAX(streak) AS longest_streak
FROM (
    SELECT customer_id, grp, COUNT(*) AS streak
    FROM islands GROUP BY customer_id, grp
) t
GROUP BY customer_id
ORDER BY longest_streak DESC, customer_id;\
""",
    hint="Expand subscriptions into active months with generate_series, then use the gap-and-island technique with ROW_NUMBER.",
    explanation="generate_series expands each subscription into its active months. The gap-and-island technique groups consecutive months, and we take the longest streak per customer.",
)

q59 = InterviewQuestion(
    id=59,
    title="Anomaly Streaks in Sensor Data",
    description=(
        "Find consecutive streaks of anomalous readings per sensor. Return sensor_id, streak_start, "
        "streak_end, and anomaly_count. Only include streaks with 2+ consecutive anomalies. "
        "Order by sensor_id, streak_start."
    ),
    company_tags=["Google", "Tesla"],
    pattern="Gap & Island",
    difficulty="hard",
    tables=["sensor_readings"],
    solution_sql="""\
WITH anomalies AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY sensor_id ORDER BY recorded_at) AS rn,
        ROW_NUMBER() OVER (PARTITION BY sensor_id, is_anomaly ORDER BY recorded_at) AS rn2
    FROM sensor_readings
),
streaks AS (
    SELECT sensor_id, rn - rn2 AS grp,
        MIN(recorded_at) AS streak_start, MAX(recorded_at) AS streak_end,
        COUNT(*) AS anomaly_count
    FROM anomalies WHERE is_anomaly = TRUE
    GROUP BY sensor_id, grp
    HAVING COUNT(*) >= 2
)
SELECT sensor_id, streak_start, streak_end, anomaly_count
FROM streaks ORDER BY sensor_id, streak_start;\
""",
    hint="Use dual ROW_NUMBER (overall vs within anomaly flag) — the difference identifies consecutive groups.",
    explanation="Two ROW_NUMBERs: one for all rows, one for only anomalous rows. The difference between them is constant for consecutive anomalies, creating a grouping key.",
)

# ============================================================
# 60-62: Recursive Hierarchies (LinkedIn, Meta)
# ============================================================

q60 = InterviewQuestion(
    id=60,
    title="Category Breadcrumb Paths",
    description=(
        "Build full breadcrumb paths for all categories in the categories table. "
        "Return id, name, depth, and full_path (e.g., 'Electronics > Computers > Laptops'). "
        "Order by full_path."
    ),
    company_tags=["LinkedIn", "Meta"],
    pattern="Recursive hierarchy",
    difficulty="medium",
    tables=["categories"],
    solution_sql="""\
WITH RECURSIVE tree AS (
    SELECT id, name, parent_id, 0 AS depth, name::TEXT AS full_path
    FROM categories WHERE parent_id IS NULL
    UNION ALL
    SELECT c.id, c.name, c.parent_id, t.depth + 1, t.full_path || ' > ' || c.name
    FROM categories c JOIN tree t ON c.parent_id = t.id
)
SELECT id, name, depth, full_path FROM tree ORDER BY full_path;\
""",
    hint="Use a recursive CTE starting from root categories (parent_id IS NULL), concatenating names at each level.",
    explanation="The anchor selects root categories. The recursive step joins children to parents, incrementing depth and appending to the path string.",
)

q61 = InterviewQuestion(
    id=61,
    title="Count Descendants per Category",
    description=(
        "For each root-level category (parent_id IS NULL), count the total number of descendants "
        "(children, grandchildren, etc.). Return root category name and descendant_count. "
        "Order by descendant_count DESC."
    ),
    company_tags=["Meta", "LinkedIn"],
    pattern="Recursive hierarchy",
    difficulty="hard",
    tables=["categories"],
    solution_sql="""\
WITH RECURSIVE tree AS (
    SELECT id, name, id AS root_id, name AS root_name
    FROM categories WHERE parent_id IS NULL
    UNION ALL
    SELECT c.id, c.name, t.root_id, t.root_name
    FROM categories c JOIN tree t ON c.parent_id = t.id
)
SELECT root_name, COUNT(*) - 1 AS descendant_count
FROM tree GROUP BY root_id, root_name
ORDER BY descendant_count DESC;\
""",
    hint="Recursive CTE carrying the root_id through all levels, then GROUP BY root and count (-1 to exclude the root itself).",
    explanation="Each row in the recursive result carries its root ancestor's ID. Grouping by root and counting gives total nodes per tree. Subtract 1 to exclude the root from the descendant count.",
)

q62 = InterviewQuestion(
    id=62,
    title="Ticket Resolution Chain",
    description=(
        "Find tickets that have been reassigned (have multiple entries). For each such ticket, "
        "show ticket_ref, subject, priority, assigned_to, and total number of status updates "
        "(count of rows per ticket_ref). Order by update count DESC, ticket_ref."
    ),
    company_tags=["LinkedIn", "Salesforce"],
    pattern="Recursive hierarchy",
    difficulty="medium",
    tables=["tickets"],
    solution_sql="""\
SELECT ticket_ref, subject, priority, assigned_to, update_count
FROM (
    SELECT ticket_ref, subject, priority, assigned_to,
        COUNT(*) OVER (PARTITION BY ticket_ref) AS update_count
    FROM tickets
) t
WHERE update_count > 1
ORDER BY update_count DESC, ticket_ref;\
""",
    hint="Use a window function to count rows per ticket_ref, then filter to those with more than one entry.",
    explanation=(
        "A subquery with COUNT(*) OVER (PARTITION BY ticket_ref) counts entries per ticket. "
        "The outer query filters to tickets with multiple entries, indicating reassignment."
    ),
)


INTERVIEW_QUESTIONS = [
    q1, q2, q3, q4, q5, q6, q7, q8, q9, q10,
    q11, q12, q13, q14, q15, q16, q17, q18, q19, q20,
    q21, q22, q23, q24, q25, q26, q27, q28, q29, q30,
    q31, q32, q33, q34, q35, q36, q37, q38, q39, q40,
    q41, q42, q43, q44, q45, q46, q47, q48, q49, q50,
    q51, q52, q53, q54, q55, q56, q57, q58, q59, q60,
    q61, q62,
]

QUESTIONS_BY_ID = {q.id: q for q in INTERVIEW_QUESTIONS}
