from dataclasses import dataclass


@dataclass
class SQLPattern:
    id: int
    name: str
    category: str
    description: str
    template_sql: str
    example_sql: str
    explanation: str
    use_cases: list[str]
    related_task_ids: list[int]


PATTERNS: list[SQLPattern] = [
    # ── Filtering (1-3) ──
    SQLPattern(
        id=1,
        name="WHERE + AND/OR",
        category="Filtering",
        description="Combine multiple conditions in a WHERE clause using AND (all must be true) or OR (at least one must be true) to narrow down result sets.",
        template_sql=(
            "SELECT *\n"
            "FROM -- your_table\n"
            "WHERE -- condition_1\n"
            "  AND -- condition_2\n"
            "   OR -- condition_3;"
        ),
        example_sql=(
            "SELECT *\n"
            "FROM employees\n"
            "WHERE department_id = 1\n"
            "  AND salary > 90000;"
        ),
        explanation=(
            "Use AND when every condition must hold simultaneously, and OR when any one "
            "condition is sufficient. Parentheses control evaluation order: "
            "WHERE (a OR b) AND c is different from WHERE a OR (b AND c). "
            "This is the most fundamental filtering pattern and appears in virtually every query."
        ),
        use_cases=[
            "Filter employees by department and minimum salary",
            "Find orders that are either pending or shipped within a date range",
            "Select active subscriptions on a specific plan",
        ],
        related_task_ids=[4, 5, 6],
    ),
    SQLPattern(
        id=2,
        name="IN / NOT IN subquery",
        category="Filtering",
        description="Use a subquery inside IN or NOT IN to filter rows based on whether a value appears in another result set.",
        template_sql=(
            "SELECT *\n"
            "FROM -- table_a\n"
            "WHERE -- column IN (\n"
            "    SELECT -- column\n"
            "    FROM -- table_b\n"
            "    WHERE -- condition\n"
            ");"
        ),
        example_sql=(
            "SELECT *\n"
            "FROM customers\n"
            "WHERE id NOT IN (\n"
            "    SELECT DISTINCT customer_id\n"
            "    FROM orders\n"
            ");"
        ),
        explanation=(
            "IN checks whether a value matches any value returned by the subquery, while "
            "NOT IN excludes those matches. Be cautious with NOT IN when the subquery can "
            "return NULL values, as NULL comparisons cause the entire predicate to evaluate "
            "to UNKNOWN, potentially returning no rows."
        ),
        use_cases=[
            "Find customers who have never placed an order",
            "Select products that have been ordered at least once",
            "Identify employees whose IDs appear in the salary change log",
        ],
        related_task_ids=[13, 14, 15],
    ),
    SQLPattern(
        id=3,
        name="EXISTS / NOT EXISTS",
        category="Filtering",
        description="Test for the existence (or absence) of rows returned by a correlated subquery. More NULL-safe than IN/NOT IN.",
        template_sql=(
            "SELECT *\n"
            "FROM -- table_a a\n"
            "WHERE EXISTS (\n"
            "    SELECT 1\n"
            "    FROM -- table_b b\n"
            "    WHERE b.a_id = a.id\n"
            "      AND -- extra_condition\n"
            ");"
        ),
        example_sql=(
            "SELECT d.id, d.name\n"
            "FROM departments d\n"
            "WHERE EXISTS (\n"
            "    SELECT 1\n"
            "    FROM employees e\n"
            "    WHERE e.department_id = d.id\n"
            "      AND e.salary > 90000\n"
            ");"
        ),
        explanation=(
            "EXISTS returns TRUE as soon as the subquery finds at least one matching row, "
            "making it efficient because it short-circuits. Unlike IN, EXISTS handles NULLs "
            "gracefully. Use NOT EXISTS to find rows with no matching counterpart, which is "
            "the standard anti-join pattern."
        ),
        use_cases=[
            "Find departments that have at least one high-earning employee",
            "Identify employees who have never had a salary change",
            "Check which customers have placed orders in the last month",
        ],
        related_task_ids=[46, 47, 48],
    ),

    # ── Aggregation (4-6) ──
    SQLPattern(
        id=4,
        name="GROUP BY + HAVING",
        category="Aggregation",
        description="Group rows by one or more columns, compute aggregate values, then filter groups with HAVING (which operates on aggregated results, unlike WHERE).",
        template_sql=(
            "SELECT -- group_column, AGG(-- value_column) AS alias\n"
            "FROM -- your_table\n"
            "GROUP BY -- group_column\n"
            "HAVING AGG(-- value_column) > -- threshold;"
        ),
        example_sql=(
            "SELECT d.name, COUNT(*) AS emp_count, ROUND(AVG(e.salary), 2) AS avg_salary\n"
            "FROM employees e\n"
            "JOIN departments d ON e.department_id = d.id\n"
            "GROUP BY d.name\n"
            "HAVING COUNT(*) >= 2;"
        ),
        explanation=(
            "GROUP BY collapses rows sharing the same group key into a single output row, "
            "and aggregate functions (COUNT, SUM, AVG, MIN, MAX) summarize the grouped data. "
            "HAVING filters after aggregation, so you can discard groups that do not meet a "
            "threshold. WHERE filters individual rows before grouping; HAVING filters groups after."
        ),
        use_cases=[
            "Show departments with more than a minimum number of employees",
            "Find product categories whose average price exceeds a threshold",
            "List customers whose total order value exceeds a target",
        ],
        related_task_ids=[10, 11, 12],
    ),
    SQLPattern(
        id=5,
        name="Conditional Aggregation (CASE in SUM/COUNT)",
        category="Aggregation",
        description="Place a CASE expression inside an aggregate function to count or sum only the rows meeting specific conditions, avoiding multiple queries.",
        template_sql=(
            "SELECT\n"
            "    -- group_column,\n"
            "    SUM(CASE WHEN -- condition THEN 1 ELSE 0 END) AS condition_count,\n"
            "    SUM(CASE WHEN -- condition THEN -- value ELSE 0 END) AS condition_sum\n"
            "FROM -- your_table\n"
            "GROUP BY -- group_column;"
        ),
        example_sql=(
            "SELECT\n"
            "    test_name,\n"
            "    variant,\n"
            "    COUNT(*) AS total_users,\n"
            "    SUM(CASE WHEN converted THEN 1 ELSE 0 END) AS conversions,\n"
            "    ROUND(100.0 * SUM(CASE WHEN converted THEN 1 ELSE 0 END) / COUNT(*), 1) AS conv_rate\n"
            "FROM ab_tests\n"
            "GROUP BY test_name, variant\n"
            "ORDER BY test_name, variant;"
        ),
        explanation=(
            "Conditional aggregation lets you compute several filtered metrics in a single "
            "pass over the data. Instead of writing separate queries with different WHERE "
            "clauses, you embed the filter logic inside CASE within SUM or COUNT. This "
            "pattern is essential for building summary dashboards and conversion reports."
        ),
        use_cases=[
            "Calculate conversion rates per A/B test variant",
            "Count orders by status in a single query",
            "Compute revenue split between paid and unpaid invoices",
        ],
        related_task_ids=[23, 24, 35, 36],
    ),
    SQLPattern(
        id=6,
        name="Pivot with CASE",
        category="Aggregation",
        description="Transform row-level categorical data into columns (pivot) using CASE expressions inside aggregate functions, creating a cross-tab report.",
        template_sql=(
            "SELECT -- group_column,\n"
            "    SUM(CASE WHEN -- category_column = 'val1' THEN -- measure ELSE 0 END) AS val1_total,\n"
            "    SUM(CASE WHEN -- category_column = 'val2' THEN -- measure ELSE 0 END) AS val2_total\n"
            "FROM -- your_table\n"
            "GROUP BY -- group_column;"
        ),
        example_sql=(
            "SELECT\n"
            "    DATE_TRUNC('month', ordered_at) AS month,\n"
            "    SUM(CASE WHEN status = 'completed' THEN total ELSE 0 END) AS completed_revenue,\n"
            "    SUM(CASE WHEN status = 'pending' THEN total ELSE 0 END) AS pending_revenue,\n"
            "    SUM(CASE WHEN status = 'shipped' THEN total ELSE 0 END) AS shipped_revenue\n"
            "FROM orders\n"
            "GROUP BY DATE_TRUNC('month', ordered_at)\n"
            "ORDER BY month;"
        ),
        explanation=(
            "Since PostgreSQL does not have a native PIVOT keyword, CASE inside aggregates "
            "is the standard way to rotate rows into columns. Each distinct category value "
            "becomes its own column via a separate CASE expression. This pattern is common "
            "in reporting where you need a matrix layout."
        ),
        use_cases=[
            "Show monthly revenue broken down by order status as columns",
            "Create a genre-vs-user stream count matrix",
            "Display subscription plan counts per city as a cross-tab",
        ],
        related_task_ids=[23, 24, 25],
    ),

    # ── Joins (7-9) ──
    SQLPattern(
        id=7,
        name="Self-Join",
        category="Joins",
        description="Join a table to itself to compare rows within the same table, such as finding pairs, hierarchies, or sequential relationships.",
        template_sql=(
            "SELECT a.-- column, b.-- column\n"
            "FROM -- your_table a\n"
            "JOIN -- your_table b\n"
            "  ON a.-- key = b.-- key\n"
            " AND a.id <> b.id;  -- avoid matching a row with itself"
        ),
        example_sql=(
            "SELECT\n"
            "    e1.first_name AS higher_earner,\n"
            "    e2.first_name AS lower_earner,\n"
            "    e1.department_id,\n"
            "    e1.salary - e2.salary AS salary_diff\n"
            "FROM employees e1\n"
            "JOIN employees e2\n"
            "  ON e1.department_id = e2.department_id\n"
            " AND e1.salary > e2.salary\n"
            "ORDER BY e1.department_id, salary_diff DESC;"
        ),
        explanation=(
            "A self-join treats two aliases of the same table as if they were different "
            "tables. You typically join on a shared attribute (same department, same year) "
            "and add an inequality to avoid pairing a row with itself. Self-joins are useful "
            "for comparisons, hierarchy traversal, and finding duplicates."
        ),
        use_cases=[
            "Compare salaries of employees within the same department",
            "Find pairs of employees hired in the same year",
            "Match salary change log entries that occurred in the same period",
        ],
        related_task_ids=[37, 38, 39],
    ),
    SQLPattern(
        id=8,
        name="LEFT JOIN + IS NULL (anti-join)",
        category="Joins",
        description="Use a LEFT JOIN combined with an IS NULL check on the right table to find rows in the left table that have no matching counterpart.",
        template_sql=(
            "SELECT a.*\n"
            "FROM -- table_a a\n"
            "LEFT JOIN -- table_b b\n"
            "  ON a.id = b.a_id\n"
            "WHERE b.id IS NULL;"
        ),
        example_sql=(
            "SELECT o.id, o.customer_id, o.total, o.status\n"
            "FROM orders o\n"
            "LEFT JOIN invoices i ON o.id = i.order_id\n"
            "WHERE i.id IS NULL\n"
            "ORDER BY o.id;"
        ),
        explanation=(
            "This anti-join pattern is one of the most common ways to find missing "
            "relationships. The LEFT JOIN preserves all rows from the left table, and "
            "WHERE b.id IS NULL keeps only those with no match on the right. It is "
            "functionally equivalent to NOT EXISTS but sometimes preferred for readability."
        ),
        use_cases=[
            "Find orders that have no corresponding invoice",
            "Identify customers who have never placed an order",
            "Discover employees with no entries in the salary log",
        ],
        related_task_ids=[14, 42, 47],
    ),
    SQLPattern(
        id=9,
        name="FULL OUTER JOIN",
        category="Joins",
        description="Combine two tables keeping all rows from both sides, filling in NULLs where there is no match. Useful for reconciliation and completeness checks.",
        template_sql=(
            "SELECT\n"
            "    COALESCE(a.-- key, b.-- key) AS key,\n"
            "    a.-- column,\n"
            "    b.-- column\n"
            "FROM -- table_a a\n"
            "FULL OUTER JOIN -- table_b b\n"
            "  ON a.-- key = b.-- key;"
        ),
        example_sql=(
            "SELECT\n"
            "    c.name AS customer_name,\n"
            "    c.city,\n"
            "    s.plan,\n"
            "    s.price,\n"
            "    s.is_active\n"
            "FROM customers c\n"
            "FULL OUTER JOIN subscriptions s ON c.id = s.customer_id\n"
            "ORDER BY c.name;"
        ),
        explanation=(
            "A FULL OUTER JOIN returns all rows from both tables. Rows that match on the "
            "join key appear together; unmatched rows from either side appear with NULLs "
            "for the other side's columns. This is useful for data reconciliation, finding "
            "orphaned records, and building complete inventories."
        ),
        use_cases=[
            "Reconcile customers against subscriptions to find gaps on either side",
            "Merge two data sources that may each have exclusive entries",
            "Audit invoices against orders to detect missing records",
        ],
        related_task_ids=[40, 42],
    ),

    # ── Window Functions (10-13) ──
    SQLPattern(
        id=10,
        name="RANK / ROW_NUMBER / DENSE_RANK",
        category="Window Functions",
        description="Assign a ranking to each row within a partition. ROW_NUMBER gives unique sequential numbers, RANK leaves gaps on ties, and DENSE_RANK does not.",
        template_sql=(
            "SELECT *,\n"
            "    ROW_NUMBER() OVER (PARTITION BY -- group_col ORDER BY -- sort_col DESC) AS rn,\n"
            "    RANK()       OVER (PARTITION BY -- group_col ORDER BY -- sort_col DESC) AS rnk,\n"
            "    DENSE_RANK() OVER (PARTITION BY -- group_col ORDER BY -- sort_col DESC) AS drnk\n"
            "FROM -- your_table;"
        ),
        example_sql=(
            "SELECT\n"
            "    e.first_name,\n"
            "    e.last_name,\n"
            "    d.name AS department,\n"
            "    e.salary,\n"
            "    RANK() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) AS salary_rank\n"
            "FROM employees e\n"
            "JOIN departments d ON e.department_id = d.id;"
        ),
        explanation=(
            "These three ranking functions all assign ordinal positions within partitions "
            "but differ in tie handling. ROW_NUMBER always produces unique values (ties get "
            "arbitrary but deterministic ordering). RANK gives tied rows the same number and "
            "skips subsequent ranks. DENSE_RANK gives tied rows the same number but does not "
            "skip. Choose based on whether you need unique IDs, gap-aware ranks, or compact ranks."
        ),
        use_cases=[
            "Rank employees by salary within each department",
            "Assign a row number for pagination",
            "Find the top-N items per category using a subquery on the rank",
        ],
        related_task_ids=[16, 49, 51],
    ),
    SQLPattern(
        id=11,
        name="Running Total (SUM OVER)",
        category="Window Functions",
        description="Compute a cumulative sum that grows row by row using SUM() with an ORDER BY inside the OVER clause.",
        template_sql=(
            "SELECT *,\n"
            "    SUM(-- value_column) OVER (ORDER BY -- sort_column) AS running_total\n"
            "FROM -- your_table;"
        ),
        example_sql=(
            "SELECT\n"
            "    id,\n"
            "    ordered_at,\n"
            "    total,\n"
            "    SUM(total) OVER (ORDER BY ordered_at) AS running_total\n"
            "FROM orders;"
        ),
        explanation=(
            "When SUM() is used with OVER(ORDER BY ...), PostgreSQL defaults to a frame of "
            "RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW, which produces a running "
            "total. You can partition by a column (e.g., customer_id) to get separate running "
            "totals per group. This pattern is essential for financial reporting and trend analysis."
        ),
        use_cases=[
            "Show a running total of revenue over time",
            "Calculate cumulative page views per session",
            "Track running subscription revenue per customer",
        ],
        related_task_ids=[17, 54],
    ),
    SQLPattern(
        id=12,
        name="LAG / LEAD",
        category="Window Functions",
        description="Access a value from a preceding row (LAG) or a following row (LEAD) within the same partition, enabling row-to-row comparisons.",
        template_sql=(
            "SELECT *,\n"
            "    LAG(-- column)  OVER (PARTITION BY -- group_col ORDER BY -- sort_col) AS prev_val,\n"
            "    LEAD(-- column) OVER (PARTITION BY -- group_col ORDER BY -- sort_col) AS next_val\n"
            "FROM -- your_table;"
        ),
        example_sql=(
            "SELECT\n"
            "    user_id,\n"
            "    song,\n"
            "    streamed_at,\n"
            "    LAG(song) OVER (PARTITION BY user_id ORDER BY streamed_at) AS prev_song,\n"
            "    EXTRACT(EPOCH FROM\n"
            "        streamed_at - LAG(streamed_at) OVER (PARTITION BY user_id ORDER BY streamed_at)\n"
            "    ) AS gap_seconds\n"
            "FROM streams;"
        ),
        explanation=(
            "LAG looks backward by a specified offset (default 1) and LEAD looks forward. "
            "They are invaluable for computing differences between consecutive rows, such as "
            "time gaps, value changes, or sequential page flows. The first row's LAG and the "
            "last row's LEAD return NULL unless you provide a default value."
        ),
        use_cases=[
            "Calculate time gap between consecutive user streams",
            "Detect page-to-page navigation flows in clickstream data",
            "Compare each month's revenue to the previous month",
        ],
        related_task_ids=[18, 52],
    ),
    SQLPattern(
        id=13,
        name="NTILE for bucketing",
        category="Window Functions",
        description="Divide ordered rows into a specified number of roughly equal-sized buckets using NTILE(n), useful for percentile and quartile analysis.",
        template_sql=(
            "SELECT *,\n"
            "    NTILE(-- n) OVER (ORDER BY -- sort_column) AS bucket\n"
            "FROM -- your_table;"
        ),
        example_sql=(
            "SELECT\n"
            "    first_name,\n"
            "    last_name,\n"
            "    salary,\n"
            "    NTILE(4) OVER (ORDER BY salary) AS salary_quartile\n"
            "FROM employees;"
        ),
        explanation=(
            "NTILE(n) assigns each row an integer from 1 to n, distributing rows as evenly "
            "as possible. If the total row count is not evenly divisible, earlier buckets get "
            "one extra row. This is the simplest way to create quartiles, deciles, or any "
            "fixed number of segments for analysis."
        ),
        use_cases=[
            "Divide employees into salary quartiles",
            "Segment customers into spending tiers (low/mid/high)",
            "Create decile buckets for order values",
        ],
        related_task_ids=[49, 53],
    ),

    # ── CTEs (14-15) ──
    SQLPattern(
        id=14,
        name="Basic CTE",
        category="CTEs",
        description="Define a named temporary result set with WITH ... AS to break complex queries into readable, reusable steps.",
        template_sql=(
            "WITH -- cte_name AS (\n"
            "    SELECT -- columns\n"
            "    FROM -- your_table\n"
            "    WHERE -- condition\n"
            ")\n"
            "SELECT *\n"
            "FROM -- cte_name;"
        ),
        example_sql=(
            "WITH dept_costs AS (\n"
            "    SELECT department_id, SUM(salary) AS total_salary\n"
            "    FROM employees\n"
            "    GROUP BY department_id\n"
            ")\n"
            "SELECT d.name, d.budget, dc.total_salary, d.budget - dc.total_salary AS remaining\n"
            "FROM departments d\n"
            "JOIN dept_costs dc ON d.id = dc.department_id;"
        ),
        explanation=(
            "A Common Table Expression (CTE) defined with the WITH keyword acts like a "
            "named inline view that exists only for the duration of the query. CTEs improve "
            "readability by giving meaningful names to intermediate results and avoiding "
            "deeply nested subqueries. You can chain multiple CTEs separated by commas."
        ),
        use_cases=[
            "Compare department budgets against actual salary expenses",
            "Pre-aggregate order data before joining with customer details",
            "Calculate booking revenue per city as a reusable intermediate step",
        ],
        related_task_ids=[19, 20, 21],
    ),
    SQLPattern(
        id=15,
        name="CTE + Window combo",
        category="CTEs",
        description="Use a CTE to pre-aggregate data, then apply window functions on the CTE's results for multi-layer analytics like moving averages or ranked aggregates.",
        template_sql=(
            "WITH -- agg_cte AS (\n"
            "    SELECT -- group_col, AGG(-- val) AS metric\n"
            "    FROM -- your_table\n"
            "    GROUP BY -- group_col\n"
            ")\n"
            "SELECT *,\n"
            "    AVG(metric) OVER (ORDER BY -- group_col ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg\n"
            "FROM -- agg_cte;"
        ),
        example_sql=(
            "WITH monthly AS (\n"
            "    SELECT DATE_TRUNC('month', ordered_at) AS month, SUM(total) AS revenue\n"
            "    FROM orders\n"
            "    GROUP BY month\n"
            ")\n"
            "SELECT\n"
            "    month,\n"
            "    revenue,\n"
            "    ROUND(AVG(revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS moving_avg_3m\n"
            "FROM monthly\n"
            "ORDER BY month;"
        ),
        explanation=(
            "Combining CTEs with window functions is a powerful two-stage pattern. The CTE "
            "handles the first level of aggregation (e.g., monthly totals), and the outer "
            "query applies window functions (e.g., moving average, ranking) on those aggregated "
            "results. This avoids complex nested subqueries and keeps the logic clear."
        ),
        use_cases=[
            "Calculate a 3-month moving average of monthly revenue",
            "Rank customers by total spending using a CTE for pre-aggregation",
            "Segment pre-aggregated data into NTILE buckets",
        ],
        related_task_ids=[53, 54],
    ),

    # ── Advanced (16-18) ──
    SQLPattern(
        id=16,
        name="Top-N per group",
        category="Advanced",
        description="Retrieve the top N rows within each group by ranking rows with ROW_NUMBER() in a subquery or CTE, then filtering by rank.",
        template_sql=(
            "WITH ranked AS (\n"
            "    SELECT *,\n"
            "        ROW_NUMBER() OVER (PARTITION BY -- group_col ORDER BY -- sort_col DESC) AS rn\n"
            "    FROM -- your_table\n"
            ")\n"
            "SELECT *\n"
            "FROM ranked\n"
            "WHERE rn <= -- N;"
        ),
        example_sql=(
            "WITH ranked AS (\n"
            "    SELECT\n"
            "        e.first_name,\n"
            "        e.last_name,\n"
            "        d.name AS department,\n"
            "        e.salary,\n"
            "        ROW_NUMBER() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) AS rn\n"
            "    FROM employees e\n"
            "    JOIN departments d ON e.department_id = d.id\n"
            ")\n"
            "SELECT first_name, last_name, department, salary\n"
            "FROM ranked\n"
            "WHERE rn <= 2;"
        ),
        explanation=(
            "The top-N per group pattern is one of the most frequently asked interview "
            "questions. You assign a row number partitioned by the group column and ordered "
            "by the ranking criterion, then filter to keep only rows where the row number is "
            "at most N. Use RANK() instead of ROW_NUMBER() if you want ties to share the same "
            "position."
        ),
        use_cases=[
            "Find the top 2 highest-paid employees per department",
            "Get the 3 most recent orders per customer",
            "Retrieve the highest-grossing product in each category",
        ],
        related_task_ids=[15, 16, 49, 53],
    ),
    SQLPattern(
        id=17,
        name="Gap & Island detection",
        category="Advanced",
        description="Identify contiguous sequences (islands) and breaks between them (gaps) by comparing a value with its row number to form grouping keys.",
        template_sql=(
            "WITH numbered AS (\n"
            "    SELECT *,\n"
            "        -- date_or_seq_col - ROW_NUMBER() OVER (ORDER BY -- date_or_seq_col) * INTERVAL '1 day' AS grp\n"
            "    FROM -- your_table\n"
            "    WHERE -- condition\n"
            ")\n"
            "SELECT grp, MIN(-- date_or_seq_col) AS island_start, MAX(-- date_or_seq_col) AS island_end, COUNT(*) AS length\n"
            "FROM numbered\n"
            "GROUP BY grp\n"
            "ORDER BY island_start;"
        ),
        example_sql=(
            "WITH active_days AS (\n"
            "    SELECT\n"
            "        user_id,\n"
            "        streamed_at::DATE AS stream_date,\n"
            "        streamed_at::DATE - (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY streamed_at::DATE))::INT AS grp\n"
            "    FROM streams\n"
            "    GROUP BY user_id, streamed_at::DATE\n"
            ")\n"
            "SELECT\n"
            "    user_id,\n"
            "    MIN(stream_date) AS streak_start,\n"
            "    MAX(stream_date) AS streak_end,\n"
            "    COUNT(*) AS streak_length\n"
            "FROM active_days\n"
            "GROUP BY user_id, grp\n"
            "ORDER BY user_id, streak_start;"
        ),
        explanation=(
            "The gap-and-island technique exploits the fact that for a contiguous sequence "
            "of dates or integers, subtracting ROW_NUMBER() produces a constant group key. "
            "Gaps break this constant, forming separate groups. This pattern is essential for "
            "detecting streaks, finding missing dates, and analyzing session continuity."
        ),
        use_cases=[
            "Detect consecutive listening streaks per user",
            "Find gaps in sequential order IDs",
            "Identify continuous active subscription periods",
        ],
        related_task_ids=[18, 34, 52],
    ),
    SQLPattern(
        id=18,
        name="Date-based cohort analysis",
        category="Advanced",
        description="Group users by their registration or first-activity date (cohort), then measure retention or revenue over subsequent time periods.",
        template_sql=(
            "WITH cohorts AS (\n"
            "    SELECT -- user_id,\n"
            "        DATE_TRUNC('month', MIN(-- first_activity_date)) AS cohort_month\n"
            "    FROM -- your_table\n"
            "    GROUP BY -- user_id\n"
            "),\n"
            "activity AS (\n"
            "    SELECT -- user_id,\n"
            "        DATE_TRUNC('month', -- activity_date) AS activity_month\n"
            "    FROM -- activity_table\n"
            ")\n"
            "SELECT c.cohort_month,\n"
            "    a.activity_month,\n"
            "    COUNT(DISTINCT a.-- user_id) AS active_users\n"
            "FROM cohorts c\n"
            "JOIN activity a ON c.-- user_id = a.-- user_id\n"
            "GROUP BY c.cohort_month, a.activity_month\n"
            "ORDER BY c.cohort_month, a.activity_month;"
        ),
        example_sql=(
            "WITH customer_cohorts AS (\n"
            "    SELECT\n"
            "        c.id AS customer_id,\n"
            "        DATE_TRUNC('month', c.registered_at) AS cohort_month\n"
            "    FROM customers c\n"
            "),\n"
            "order_activity AS (\n"
            "    SELECT\n"
            "        customer_id,\n"
            "        DATE_TRUNC('month', ordered_at) AS order_month\n"
            "    FROM orders\n"
            ")\n"
            "SELECT\n"
            "    cc.cohort_month,\n"
            "    oa.order_month,\n"
            "    COUNT(DISTINCT oa.customer_id) AS active_customers,\n"
            "    SUM(o.total) AS cohort_revenue\n"
            "FROM customer_cohorts cc\n"
            "JOIN order_activity oa ON cc.customer_id = oa.customer_id\n"
            "JOIN orders o ON oa.customer_id = o.customer_id\n"
            "    AND DATE_TRUNC('month', o.ordered_at) = oa.order_month\n"
            "GROUP BY cc.cohort_month, oa.order_month\n"
            "ORDER BY cc.cohort_month, oa.order_month;"
        ),
        explanation=(
            "Cohort analysis assigns each user to a cohort based on when they first appeared "
            "(e.g., registration month), then tracks their behavior over subsequent periods. "
            "This reveals retention trends and revenue patterns that aggregate metrics hide. "
            "The pattern typically uses two CTEs: one for cohort assignment and one for activity "
            "aggregation."
        ),
        use_cases=[
            "Track monthly retention of customers by registration cohort",
            "Analyze revenue per cohort over time to measure lifetime value",
            "Compare subscription plan upgrade rates across signup cohorts",
        ],
        related_task_ids=[21, 25, 34, 54],
    ),
]

PATTERNS_BY_ID = {p.id: p for p in PATTERNS}
PATTERN_CATEGORIES = sorted(set(p.category for p in PATTERNS))
