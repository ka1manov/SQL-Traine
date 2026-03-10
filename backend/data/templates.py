from dataclasses import dataclass


@dataclass
class QueryTemplate:
    id: int
    title: str
    category: str
    description: str
    sql: str


TEMPLATES: list[QueryTemplate] = [
    QueryTemplate(1, "Basic SELECT", "Basics",
                  "Select all rows from a table",
                  "SELECT *\nFROM table_name\nLIMIT 10;"),
    QueryTemplate(2, "Filter with WHERE", "Basics",
                  "Filter rows with conditions",
                  "SELECT *\nFROM employees\nWHERE salary > 80000\n  AND is_active = TRUE;"),
    QueryTemplate(3, "INNER JOIN", "Joins",
                  "Combine two tables on a key",
                  "SELECT e.first_name, d.name AS department\nFROM employees e\nJOIN departments d ON e.department_id = d.id;"),
    QueryTemplate(4, "LEFT JOIN with NULL check", "Joins",
                  "Find rows without matches",
                  "SELECT c.name, o.id AS order_id\nFROM customers c\nLEFT JOIN orders o ON c.id = o.customer_id\nWHERE o.id IS NULL;"),
    QueryTemplate(5, "GROUP BY with HAVING", "Aggregation",
                  "Aggregate and filter groups",
                  "SELECT department_id, COUNT(*) AS emp_count, AVG(salary) AS avg_salary\nFROM employees\nGROUP BY department_id\nHAVING COUNT(*) > 2;"),
    QueryTemplate(6, "Window Function - RANK", "Window Functions",
                  "Rank rows within partitions",
                  "SELECT first_name, salary,\n  RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rank\nFROM employees;"),
    QueryTemplate(7, "Running Total", "Window Functions",
                  "Cumulative sum over ordered rows",
                  "SELECT id, total,\n  SUM(total) OVER (ORDER BY ordered_at) AS running_total\nFROM orders;"),
    QueryTemplate(8, "CTE - Common Table Expression", "CTEs",
                  "Named subquery for readability",
                  "WITH dept_stats AS (\n  SELECT department_id, AVG(salary) AS avg_sal\n  FROM employees\n  GROUP BY department_id\n)\nSELECT d.name, ds.avg_sal\nFROM departments d\nJOIN dept_stats ds ON d.id = ds.department_id;"),
    QueryTemplate(9, "CASE Expression", "Conditional",
                  "Conditional column values",
                  "SELECT first_name, salary,\n  CASE\n    WHEN salary > 95000 THEN 'Senior'\n    WHEN salary > 70000 THEN 'Mid'\n    ELSE 'Junior'\n  END AS tier\nFROM employees;"),
    QueryTemplate(10, "Pivot with CASE", "Conditional",
                   "Turn rows into columns",
                   "SELECT\n  COUNT(CASE WHEN status = 'completed' THEN 1 END) AS completed,\n  COUNT(CASE WHEN status = 'pending' THEN 1 END) AS pending,\n  COUNT(CASE WHEN status = 'shipped' THEN 1 END) AS shipped\nFROM orders;"),
    QueryTemplate(11, "Date Truncation", "Date & Time",
                   "Group by month/week/year",
                   "SELECT DATE_TRUNC('month', ordered_at) AS month,\n  COUNT(*) AS orders,\n  SUM(total) AS revenue\nFROM orders\nGROUP BY month\nORDER BY month;"),
    QueryTemplate(12, "Subquery in WHERE", "Subqueries",
                   "Filter using a subquery",
                   "SELECT *\nFROM employees\nWHERE salary > (\n  SELECT AVG(salary) FROM employees\n);"),
    QueryTemplate(13, "UNION", "Set Operations",
                   "Combine results from two queries",
                   "SELECT first_name AS name FROM employees\nUNION\nSELECT name FROM customers;"),
    QueryTemplate(14, "String Functions", "String",
                   "Common string operations",
                   "SELECT\n  UPPER(first_name) AS upper_name,\n  LENGTH(email) AS email_len,\n  SPLIT_PART(email, '@', 2) AS domain\nFROM employees;"),
    QueryTemplate(15, "LAG / LEAD", "Window Functions",
                   "Access previous/next row values",
                   "SELECT song, streamed_at,\n  LAG(song) OVER (PARTITION BY user_id ORDER BY streamed_at) AS prev_song\nFROM streams;"),
]
