from dataclasses import dataclass, field


@dataclass
class QuizQuestion:
    question: str
    answer: str


@dataclass
class SQLExample:
    title: str
    sql: str
    explanation: str


@dataclass
class PathStep:
    title: str
    description: str
    task_ids: list[int]
    example_sql: str | None = None
    theory: str = ""
    key_points: list[str] = field(default_factory=list)
    syntax: str | None = None
    examples: list[SQLExample] = field(default_factory=list)
    quiz: list[QuizQuestion] = field(default_factory=list)
    tips: list[str] = field(default_factory=list)


@dataclass
class LearningPath:
    id: int
    title: str
    description: str
    icon: str
    steps: list[PathStep]


# ---------------------------------------------------------------------------
# PATH 1 — SQL Fundamentals
# ---------------------------------------------------------------------------

_fundamentals_steps = [
    PathStep(
        title="Your First Query",
        description="Learn SELECT to retrieve data from tables.",
        task_ids=[1, 2],
        example_sql="SELECT first_name, last_name FROM employees;",
        theory=(
            "Every interaction with a relational database starts with a query, and the most "
            "fundamental query is SELECT. When you write a SELECT statement, you are asking the "
            "database to look inside a table and return specific pieces of information. Think of a "
            "table as a spreadsheet: it has columns (the fields like name, salary, email) and rows "
            "(individual records). SELECT lets you pick which columns you want to see and from which "
            "table.\n\n"

            "The simplest possible query is SELECT * FROM table_name. The asterisk (*) is a wildcard "
            "that means \"give me every column.\" While handy for quick exploration, production code "
            "should list columns explicitly — this makes your intent clear, avoids fetching unnecessary "
            "data, and protects you if someone adds new columns later.\n\n"

            "You can choose specific columns by listing them after SELECT, separated by commas: "
            "SELECT first_name, last_name, salary FROM employees. The database returns only those "
            "three columns, in the order you specified. You can also rename a column in the output "
            "using an alias: SELECT first_name AS name tells the database to label that column "
            "\"name\" in the result.\n\n"

            "Sometimes a column contains duplicate values and you only want unique ones. That is where "
            "DISTINCT comes in. SELECT DISTINCT department_id FROM employees returns each department ID "
            "exactly once, no matter how many employees share the same department. DISTINCT applies to "
            "the entire row of selected columns, so SELECT DISTINCT city, country gives you every "
            "unique city-country combination.\n\n"

            "Understanding SELECT is the gateway to everything else in SQL. Every complex query — "
            "joins, aggregations, subqueries — is still a SELECT statement at its core. Master the "
            "basics here and the rest will build naturally."
        ),
        key_points=[
            "SELECT specifies which columns to return; FROM specifies the table.",
            "Use * to select all columns — but prefer explicit column lists in real applications.",
            "Column aliases (AS) rename columns in the output without changing the table.",
            "DISTINCT eliminates duplicate rows from the result set.",
            "Column order in SELECT determines the order of columns in the output.",
        ],
        syntax="SELECT [DISTINCT] column1 [AS alias], column2, ...\nFROM table_name;",
        examples=[
            SQLExample(
                title="Select all columns",
                sql="SELECT * FROM employees;",
                explanation=(
                    "Returns every column and every row from the employees table. "
                    "Useful for exploring what data is available, but avoid in production "
                    "because it fetches more data than usually needed."
                ),
            ),
            SQLExample(
                title="Select specific columns with alias",
                sql="SELECT first_name AS name, salary AS annual_pay\nFROM employees;",
                explanation=(
                    "Returns only two columns, renamed to 'name' and 'annual_pay' in the output. "
                    "Aliases make results easier to read and are especially useful when column names "
                    "are long or ambiguous in joins."
                ),
            ),
            SQLExample(
                title="Select distinct values",
                sql="SELECT DISTINCT department_id\nFROM employees\nORDER BY department_id;",
                explanation=(
                    "Returns each unique department_id exactly once. Adding ORDER BY sorts them "
                    "so you can quickly scan the list. This is a common pattern for discovering "
                    "what distinct values exist in a column."
                ),
            ),
        ],
        quiz=[
            QuizQuestion(
                "What does SELECT * FROM employees return?",
                "All columns and all rows from the employees table.",
            ),
            QuizQuestion(
                "How do you rename a column in the output without changing the actual table?",
                "Use a column alias with the AS keyword: SELECT salary AS pay FROM employees.",
            ),
            QuizQuestion(
                "What does DISTINCT do, and does it apply to individual columns or entire rows?",
                "DISTINCT removes duplicate rows. It applies to the entire combination of selected columns, not just one column.",
            ),
        ],
        tips=[
            "In interviews, always list columns explicitly rather than using SELECT * — it shows you understand what data you need.",
            "DISTINCT can be expensive on large tables because the database must compare every row. Use it only when you truly need unique values.",
            "Some databases (like PostgreSQL) support DISTINCT ON(column) to keep the first row per group — a useful trick for deduplication.",
        ],
    ),

    PathStep(
        title="Filtering with WHERE",
        description="Use WHERE to filter rows based on conditions.",
        task_ids=[4, 5],
        example_sql="SELECT * FROM employees WHERE salary > 90000;",
        theory=(
            "Most of the time you don't want every row in a table — you want a specific subset. "
            "The WHERE clause acts as a filter: after the database identifies which table to read "
            "(FROM), it checks each row against the condition you provide and only keeps the rows "
            "that satisfy it.\n\n"

            "The most basic comparisons use operators you already know from math: = (equals), "
            "!= or <> (not equals), > (greater than), < (less than), >= and <=. For text, "
            "= performs an exact match (case-sensitive in most databases), so WHERE name = 'Alice' "
            "only matches that exact spelling.\n\n"

            "You can combine multiple conditions with AND and OR. AND requires both conditions to be "
            "true: WHERE salary > 50000 AND department_id = 3. OR requires at least one to be true. "
            "Use parentheses to control evaluation order — without them, AND binds tighter than OR, "
            "which can produce unexpected results. NOT inverts a condition: WHERE NOT department_id = 5.\n\n"

            "SQL provides several convenience operators for common filtering patterns. "
            "IN lets you match against a list: WHERE department_id IN (1, 3, 5) is cleaner than "
            "three OR conditions. BETWEEN checks an inclusive range: WHERE salary BETWEEN 50000 AND 80000 "
            "is equivalent to salary >= 50000 AND salary <= 80000. LIKE enables pattern matching on text: "
            "the % wildcard matches any sequence of characters (WHERE name LIKE 'A%' finds names starting "
            "with A) and _ matches exactly one character.\n\n"

            "NULL deserves special attention. In SQL, NULL means \"unknown\" — it is not zero, not an "
            "empty string, not false. You cannot compare NULL with = because NULL = NULL evaluates to "
            "NULL (unknown), not true. Instead, use IS NULL or IS NOT NULL: WHERE manager_id IS NULL "
            "finds employees with no manager. This is one of the most common sources of bugs in SQL, "
            "so always keep it in mind when filtering data that might contain missing values."
        ),
        key_points=[
            "WHERE filters rows after the FROM clause identifies the table.",
            "Use AND/OR to combine conditions; parentheses control evaluation order.",
            "IN matches against a list, BETWEEN matches an inclusive range, LIKE does pattern matching.",
            "NULL is not a value — use IS NULL / IS NOT NULL, never = NULL.",
            "String comparisons are case-sensitive in most databases (use ILIKE in PostgreSQL for case-insensitive matching).",
        ],
        syntax="SELECT columns\nFROM table\nWHERE condition1\n  AND/OR condition2\n  ...;",
        examples=[
            SQLExample(
                title="Multiple conditions with AND",
                sql="SELECT first_name, salary\nFROM employees\nWHERE salary > 60000\n  AND department_id = 2;",
                explanation=(
                    "Returns employees in department 2 who earn more than 60,000. "
                    "Both conditions must be true for a row to appear in the result."
                ),
            ),
            SQLExample(
                title="Using IN for a list of values",
                sql="SELECT *\nFROM employees\nWHERE department_id IN (1, 3, 5);",
                explanation=(
                    "Equivalent to department_id = 1 OR department_id = 3 OR department_id = 5, "
                    "but much more readable. IN is the preferred pattern when checking against a fixed set of values."
                ),
            ),
            SQLExample(
                title="Pattern matching with LIKE",
                sql="SELECT first_name, last_name\nFROM employees\nWHERE last_name LIKE 'S%';",
                explanation=(
                    "Returns employees whose last name starts with 'S'. The % wildcard matches "
                    "any number of characters. To find names containing 'son' anywhere, use '%son%'."
                ),
            ),
            SQLExample(
                title="Handling NULLs",
                sql="SELECT first_name, manager_id\nFROM employees\nWHERE manager_id IS NULL;",
                explanation=(
                    "Finds employees with no manager (top-level executives). "
                    "Using = NULL here would return no rows because NULL = NULL is unknown, not true."
                ),
            ),
        ],
        quiz=[
            QuizQuestion(
                "Why does WHERE salary = NULL return no rows even if some salaries are NULL?",
                "Because any comparison with NULL yields NULL (unknown), not true. You must use WHERE salary IS NULL.",
            ),
            QuizQuestion(
                "What is the difference between WHERE x IN (1,2,3) and WHERE x = 1 OR x = 2 OR x = 3?",
                "They produce the same result. IN is syntactic sugar for multiple OR conditions on the same column.",
            ),
            QuizQuestion(
                "In WHERE a OR b AND c, which condition is evaluated first without parentheses?",
                "AND is evaluated first due to higher precedence, so it is interpreted as a OR (b AND c). Use parentheses to make intent explicit.",
            ),
        ],
        tips=[
            "Always use IS NULL instead of = NULL — this is a classic interview trap question.",
            "When combining AND and OR, use parentheses even if you know the precedence — it makes your intent clear to the reader.",
            "In PostgreSQL, use ILIKE instead of LIKE for case-insensitive pattern matching.",
        ],
    ),

    PathStep(
        title="Sorting & Limiting",
        description="Order results and limit output with ORDER BY, LIMIT, and OFFSET.",
        task_ids=[3],
        example_sql="SELECT DISTINCT department_id FROM employees ORDER BY department_id;",
        theory=(
            "Relational databases do not guarantee any particular order for returned rows. "
            "If you run the same query twice, you might get rows in a different order. "
            "The ORDER BY clause lets you sort the result set by one or more columns so the "
            "output is predictable and meaningful.\n\n"

            "By default, ORDER BY sorts in ascending order (ASC) — smallest to largest for numbers, "
            "A to Z for text, earliest to latest for dates. Add DESC after a column name to sort "
            "in descending order. You can sort by multiple columns: ORDER BY department_id ASC, "
            "salary DESC first groups rows by department, then within each department sorts by "
            "salary from highest to lowest.\n\n"

            "LIMIT restricts how many rows are returned. This is essential for performance on large "
            "tables and for building paginated UIs. LIMIT 10 returns only the first 10 rows from "
            "the sorted result. Combined with ORDER BY, this gives you powerful patterns like "
            "\"top 5 highest-paid employees\": ORDER BY salary DESC LIMIT 5.\n\n"

            "OFFSET skips a specified number of rows before starting to return results. "
            "Together with LIMIT, OFFSET enables pagination: page 1 is LIMIT 10 OFFSET 0, "
            "page 2 is LIMIT 10 OFFSET 10, page 3 is LIMIT 10 OFFSET 20, and so on. "
            "However, OFFSET-based pagination becomes slow on large tables because the database "
            "still has to read and discard the skipped rows. For high-performance pagination, "
            "keyset pagination (also called cursor-based pagination) is preferred, where you filter "
            "using WHERE id > last_seen_id instead of using OFFSET.\n\n"

            "One important detail: ORDER BY happens after SELECT, so you can sort by a column alias "
            "defined in SELECT. You can also sort by column position (ORDER BY 1 means sort by the "
            "first column), though this is less readable and generally discouraged in production code."
        ),
        key_points=[
            "ORDER BY sorts results; ASC (default) for ascending, DESC for descending.",
            "You can sort by multiple columns — later columns break ties from earlier ones.",
            "LIMIT restricts the number of returned rows; OFFSET skips rows for pagination.",
            "Without ORDER BY, row order is not guaranteed — don't assume any natural ordering.",
            "OFFSET-based pagination is simple but slow on large datasets; keyset pagination is better for scale.",
        ],
        syntax="SELECT columns\nFROM table\n[WHERE ...]\nORDER BY column1 [ASC|DESC], column2 [ASC|DESC]\nLIMIT n\nOFFSET m;",
        examples=[
            SQLExample(
                title="Top 5 highest salaries",
                sql="SELECT first_name, salary\nFROM employees\nORDER BY salary DESC\nLIMIT 5;",
                explanation=(
                    "Sorts all employees by salary in descending order, then returns only the "
                    "first 5 rows — giving you the top 5 earners."
                ),
            ),
            SQLExample(
                title="Multi-column sort",
                sql="SELECT first_name, department_id, salary\nFROM employees\nORDER BY department_id ASC, salary DESC;",
                explanation=(
                    "First sorts by department (ascending), then within each department sorts "
                    "by salary from highest to lowest. This groups employees by department with "
                    "top earners first in each group."
                ),
            ),
            SQLExample(
                title="Pagination with LIMIT and OFFSET",
                sql="SELECT id, first_name, last_name\nFROM employees\nORDER BY id\nLIMIT 10 OFFSET 20;",
                explanation=(
                    "Skips the first 20 rows and returns the next 10, effectively showing page 3 "
                    "of a paginated result (assuming 10 items per page)."
                ),
            ),
        ],
        quiz=[
            QuizQuestion(
                "What is the default sort direction in ORDER BY?",
                "Ascending (ASC). Smallest values first for numbers, A-Z for text, earliest for dates.",
            ),
            QuizQuestion(
                "Why is OFFSET-based pagination considered slow on large tables?",
                "The database must still read and discard all the skipped rows, so OFFSET 1000000 means scanning a million rows before returning results.",
            ),
            QuizQuestion(
                "Can you ORDER BY a column that is not in the SELECT list?",
                "Yes. ORDER BY can reference any column from the table, not just those in SELECT (unless using DISTINCT, which restricts it to selected columns).",
            ),
        ],
        tips=[
            "In interviews, always pair LIMIT with ORDER BY — LIMIT without ORDER BY gives non-deterministic results.",
            "NULLs sort first in ascending order and last in descending order in most databases. PostgreSQL supports NULLS FIRST / NULLS LAST to control this.",
            "If asked about pagination at scale, mention keyset/cursor-based pagination as a superior alternative to OFFSET.",
        ],
    ),
]

# ---------------------------------------------------------------------------
# PATH 2 — Joins Mastery
# ---------------------------------------------------------------------------

_joins_steps = [
    PathStep(
        title="INNER JOIN",
        description="Combine rows from two tables on a matching column.",
        task_ids=[7],
        example_sql="SELECT e.first_name, d.name\nFROM employees e\nJOIN departments d ON e.department_id = d.id;",
        theory=(
            "Relational databases store data across multiple tables to avoid duplication — a process "
            "called normalization. Employees have a department_id rather than repeating the full "
            "department name on every row. To bring this data together, you use a JOIN.\n\n"

            "An INNER JOIN (or simply JOIN) returns only the rows that have a match in both tables. "
            "If an employee has department_id = 5 and there is a department with id = 5, the row is "
            "included. If an employee has a department_id that doesn't exist in the departments table, "
            "that employee is excluded. Similarly, departments with no employees are excluded.\n\n"

            "A LEFT JOIN (also called LEFT OUTER JOIN) returns all rows from the left table (the one "
            "after FROM) and matching rows from the right table. If there is no match, the right-side "
            "columns are filled with NULL. This is useful when you want all employees even if some "
            "don't belong to a department. RIGHT JOIN is the mirror image: all rows from the right table, "
            "with NULLs for the left where there is no match.\n\n"

            "A FULL OUTER JOIN returns all rows from both tables, filling NULLs on whichever side "
            "lacks a match. It's the union of LEFT and RIGHT joins. This is useful for finding "
            "unmatched rows in either table — for example, departments with no employees AND "
            "employees with no valid department.\n\n"

            "Table aliases make joins readable. Instead of writing the full table name in every "
            "column reference, use short aliases: FROM employees e JOIN departments d. This is "
            "especially important when a column name exists in both tables — you must qualify it "
            "with the table alias (e.g., e.id vs d.id) to avoid ambiguity errors."
        ),
        key_points=[
            "INNER JOIN returns only rows with matches in both tables.",
            "LEFT JOIN keeps all rows from the left table, filling NULLs for missing right-side matches.",
            "RIGHT JOIN keeps all rows from the right table (rarely used — just swap the table order and use LEFT JOIN).",
            "FULL OUTER JOIN keeps all rows from both tables, NULLs on both sides where no match exists.",
            "Always use table aliases in joins to keep queries readable and avoid column ambiguity.",
        ],
        syntax="SELECT a.col, b.col\nFROM table_a a\n[INNER | LEFT | RIGHT | FULL OUTER] JOIN table_b b\n  ON a.key = b.key;",
        examples=[
            SQLExample(
                title="INNER JOIN — employees with departments",
                sql="SELECT e.first_name, e.salary, d.name AS department\nFROM employees e\nJOIN departments d ON e.department_id = d.id;",
                explanation=(
                    "Returns only employees who have a valid department_id matching a department record. "
                    "Employees without a department and departments without employees are excluded."
                ),
            ),
            SQLExample(
                title="LEFT JOIN — all employees, even without departments",
                sql="SELECT e.first_name, d.name AS department\nFROM employees e\nLEFT JOIN departments d ON e.department_id = d.id;",
                explanation=(
                    "Returns every employee. If an employee's department_id doesn't match any department, "
                    "the department column shows NULL. This preserves all employees in the result."
                ),
            ),
            SQLExample(
                title="Find unmatched rows with LEFT JOIN + IS NULL",
                sql="SELECT d.name\nFROM departments d\nLEFT JOIN employees e ON d.id = e.department_id\nWHERE e.id IS NULL;",
                explanation=(
                    "A common pattern: LEFT JOIN followed by WHERE right_side IS NULL finds rows "
                    "in the left table with no match. Here it finds departments that have no employees."
                ),
            ),
        ],
        quiz=[
            QuizQuestion(
                "What happens to a row from the left table in a LEFT JOIN if there is no matching row in the right table?",
                "The row is still included in the result, but all columns from the right table are filled with NULL.",
            ),
            QuizQuestion(
                "What is the difference between JOIN and INNER JOIN?",
                "There is no difference. JOIN is shorthand for INNER JOIN — they are identical.",
            ),
            QuizQuestion(
                "How do you find rows in table A that have no match in table B?",
                "Use LEFT JOIN table_b ON ... WHERE table_b.key IS NULL. This returns only unmatched rows from the left table.",
            ),
        ],
        tips=[
            "In interviews, if asked about RIGHT JOIN, mention that most developers prefer LEFT JOIN and simply reorder the tables — it's more readable.",
            "Always check: do you want all rows from one side (LEFT/RIGHT) or only matched rows (INNER)? This is the most common JOIN mistake.",
            "When joining on multiple columns, list all conditions with AND in the ON clause: ON a.x = b.x AND a.y = b.y.",
        ],
    ),

    PathStep(
        title="Multi-Table Joins",
        description="Chain multiple tables together and explore self-joins.",
        task_ids=[8, 9],
        example_sql="SELECT o.id, c.name, p.name\nFROM orders o\nJOIN customers c ON o.customer_id = c.id\nJOIN products p ON o.product_id = p.id;",
        theory=(
            "Real-world queries often need data from three or more tables. You chain joins by "
            "adding additional JOIN clauses after the first one. Each new JOIN connects to any "
            "table already in the query. The database builds the result step by step: first it "
            "joins the first two tables, then joins the third table to that intermediate result, "
            "and so on.\n\n"

            "For example, to get order details with customer names and product names, you join "
            "orders to customers (on customer_id) and orders to products (on product_id). The "
            "order doesn't usually matter for INNER JOINs — the optimizer rearranges them — but "
            "for LEFT JOINs, order matters because it determines which side preserves all rows.\n\n"

            "A self-join is when a table joins to itself. This is common for hierarchical data. "
            "For example, an employees table with a manager_id column that references another "
            "employee's id. To get each employee along with their manager's name: "
            "FROM employees e JOIN employees m ON e.manager_id = m.id. You must use different "
            "aliases for the two references to the same table so the database can tell them apart.\n\n"

            "A CROSS JOIN produces the Cartesian product — every row from table A paired with "
            "every row from table B. If table A has 100 rows and table B has 50 rows, the result "
            "has 5,000 rows. This is rarely what you want, but it's useful for generating "
            "combinations (e.g., all possible product-color pairs) or for creating date scaffolds "
            "where you need every combination of dates and categories.\n\n"

            "When chaining many joins, keep your query organized: one JOIN per line, consistent "
            "alias naming (first letter of table name), and indent the ON clauses. This makes "
            "complex queries much easier to read, debug, and modify."
        ),
        key_points=[
            "Chain JOINs by adding more JOIN clauses — each connects to the running result set.",
            "Self-joins use different aliases for the same table to reference it twice.",
            "CROSS JOIN produces every combination of rows (Cartesian product) — use with caution.",
            "For LEFT JOINs, table order matters: the leftmost table keeps all its rows.",
            "Use consistent, short aliases and one-JOIN-per-line formatting for readability.",
        ],
        syntax="SELECT ...\nFROM table_a a\nJOIN table_b b ON a.key = b.key\nJOIN table_c c ON b.key = c.key\n...;",
        examples=[
            SQLExample(
                title="Three-table join",
                sql="SELECT o.id AS order_id,\n       c.name AS customer,\n       p.name AS product,\n       o.quantity\nFROM orders o\nJOIN customers c ON o.customer_id = c.id\nJOIN products p ON o.product_id = p.id;",
                explanation=(
                    "Joins orders to customers (for names) and to products (for product names). "
                    "The result is a human-readable order list with all three pieces of information."
                ),
            ),
            SQLExample(
                title="Self-join — employee and manager",
                sql="SELECT e.first_name AS employee,\n       m.first_name AS manager\nFROM employees e\nLEFT JOIN employees m ON e.manager_id = m.id;",
                explanation=(
                    "The employees table is referenced twice with aliases e (employee) and m (manager). "
                    "LEFT JOIN ensures employees without a manager (CEO) still appear — with NULL as manager."
                ),
            ),
            SQLExample(
                title="CROSS JOIN for combinations",
                sql="SELECT s.size, c.color\nFROM sizes s\nCROSS JOIN colors c;",
                explanation=(
                    "Produces every size-color combination. If there are 4 sizes and 6 colors, "
                    "you get 24 rows — one for each possible combination."
                ),
            ),
        ],
        quiz=[
            QuizQuestion(
                "Why do self-joins require different table aliases?",
                "Because the database needs to distinguish between the two references to the same table — without aliases, column references would be ambiguous.",
            ),
            QuizQuestion(
                "What does a CROSS JOIN produce?",
                "The Cartesian product: every row from the first table paired with every row from the second table. If table A has M rows and table B has N rows, the result has M × N rows.",
            ),
            QuizQuestion(
                "Can you chain LEFT JOINs and INNER JOINs in the same query?",
                "Yes. You can mix join types freely. Just be aware that an INNER JOIN after a LEFT JOIN can eliminate the NULL rows that the LEFT JOIN preserved.",
            ),
        ],
        tips=[
            "In interviews, if you need a self-join, clearly explain the aliases and the relationship — interviewers want to see you understand the concept.",
            "When debugging multi-table joins that return unexpected results, start by removing joins one at a time to isolate which join introduces the problem.",
            "Watch out for accidental CROSS JOINs: forgetting the ON clause in some SQL dialects silently produces a Cartesian product.",
        ],
    ),
]

# ---------------------------------------------------------------------------
# PATH 3 — Aggregation & Grouping
# ---------------------------------------------------------------------------

_aggregation_steps = [
    PathStep(
        title="Basic Aggregations",
        description="Use COUNT, SUM, AVG on groups of rows.",
        task_ids=[10, 12],
        example_sql="SELECT department_id, COUNT(*)\nFROM employees\nGROUP BY department_id;",
        theory=(
            "Aggregation functions take a set of rows and produce a single summary value. "
            "The five core functions are: COUNT (number of rows), SUM (total of a numeric column), "
            "AVG (average value), MIN (smallest value), and MAX (largest value). Without a GROUP BY, "
            "these functions operate on the entire table and return a single row.\n\n"

            "GROUP BY divides the table into groups based on one or more columns, then applies the "
            "aggregation function separately to each group. SELECT department_id, AVG(salary) FROM "
            "employees GROUP BY department_id gives you the average salary per department. Every "
            "non-aggregated column in SELECT must appear in GROUP BY — the database needs to know "
            "which group a column value belongs to.\n\n"

            "COUNT has two important variants. COUNT(*) counts all rows in a group, including rows "
            "where some columns are NULL. COUNT(column_name) counts only rows where that specific "
            "column is not NULL. This distinction matters: if 10 employees have department_id values "
            "and 3 have NULL manager_id, COUNT(*) returns 10 but COUNT(manager_id) returns 7.\n\n"

            "NULL handling in aggregations follows a simple rule: aggregate functions ignore NULLs "
            "(except COUNT(*)). So AVG(salary) computes the average using only non-NULL salary values, "
            "and SUM(bonus) sums only the non-NULL bonuses. If all values in a group are NULL, the "
            "aggregate returns NULL (except COUNT, which returns 0).\n\n"

            "You can use multiple aggregate functions in a single query: "
            "SELECT department_id, COUNT(*), AVG(salary), MAX(salary) FROM employees GROUP BY department_id. "
            "This gives you a comprehensive summary of each department in one query."
        ),
        key_points=[
            "COUNT(*) counts all rows; COUNT(column) counts only non-NULL values in that column.",
            "SUM, AVG, MIN, MAX all ignore NULL values when computing their results.",
            "Every non-aggregated column in SELECT must be listed in GROUP BY.",
            "Without GROUP BY, aggregate functions operate on the entire table and return one row.",
            "You can use multiple aggregate functions in a single SELECT statement.",
        ],
        syntax="SELECT group_col, COUNT(*), SUM(col), AVG(col), MIN(col), MAX(col)\nFROM table\n[WHERE ...]\nGROUP BY group_col;",
        examples=[
            SQLExample(
                title="Count and average per department",
                sql="SELECT department_id,\n       COUNT(*) AS employee_count,\n       ROUND(AVG(salary), 2) AS avg_salary\nFROM employees\nGROUP BY department_id;",
                explanation=(
                    "Groups employees by department, then counts how many are in each group and "
                    "computes the average salary. ROUND limits the average to 2 decimal places."
                ),
            ),
            SQLExample(
                title="COUNT(*) vs COUNT(column)",
                sql="SELECT COUNT(*) AS total_rows,\n       COUNT(manager_id) AS has_manager\nFROM employees;",
                explanation=(
                    "COUNT(*) counts every row regardless of NULLs. COUNT(manager_id) counts only "
                    "rows where manager_id is not NULL. The difference tells you how many employees "
                    "have no manager."
                ),
            ),
            SQLExample(
                title="Multiple group columns",
                sql="SELECT department_id, \n       EXTRACT(YEAR FROM hire_date) AS year,\n       COUNT(*) AS hires\nFROM employees\nGROUP BY department_id, EXTRACT(YEAR FROM hire_date)\nORDER BY department_id, year;",
                explanation=(
                    "Groups by both department and hire year, showing how many employees were hired "
                    "per department per year. Both group expressions appear in GROUP BY."
                ),
            ),
        ],
        quiz=[
            QuizQuestion(
                "What is the difference between COUNT(*) and COUNT(column_name)?",
                "COUNT(*) counts all rows including NULLs. COUNT(column_name) counts only rows where that column is not NULL.",
            ),
            QuizQuestion(
                "What happens if you put a non-aggregated column in SELECT but not in GROUP BY?",
                "Most databases (including PostgreSQL in strict mode) will raise an error because the database doesn't know which value to show for that column from the group.",
            ),
            QuizQuestion(
                "How does AVG handle NULL values?",
                "AVG ignores NULLs entirely — it sums the non-NULL values and divides by the count of non-NULL values, not the total row count.",
            ),
        ],
        tips=[
            "In interviews, explicitly mention that COUNT(*) vs COUNT(column) is a meaningful difference — it shows attention to detail about NULLs.",
            "When grouping by a date column, you often need to truncate it first (e.g., DATE_TRUNC) to group by month or year rather than exact timestamp.",
            "If you need the total alongside group subtotals, look into ROLLUP or GROUPING SETS — they're advanced but impressive in interviews.",
        ],
    ),

    PathStep(
        title="HAVING Clause",
        description="Filter groups after aggregation with HAVING.",
        task_ids=[11],
        example_sql="SELECT customer_id, SUM(total) AS spent\nFROM orders\nGROUP BY customer_id\nHAVING SUM(total) > 1000;",
        theory=(
            "WHERE filters individual rows before grouping. But what if you want to filter "
            "based on an aggregate result — like keeping only departments with more than 5 employees "
            "or customers who have spent over $1,000? That is what HAVING does: it filters groups "
            "after the aggregation has been computed.\n\n"

            "Understanding the SQL execution order is key to understanding why HAVING exists and "
            "how it differs from WHERE. The logical execution order is: FROM (identify tables) → "
            "WHERE (filter individual rows) → GROUP BY (form groups) → HAVING (filter groups) → "
            "SELECT (compute output columns) → ORDER BY (sort results) → LIMIT (restrict output). "
            "Notice that WHERE runs before GROUP BY, so it cannot reference aggregate results. "
            "HAVING runs after GROUP BY, so it can.\n\n"

            "A common pattern is combining WHERE and HAVING in the same query. For example: "
            "filter to only active customers (WHERE), group by customer, compute total spending "
            "(GROUP BY + SUM), then keep only high-spenders (HAVING SUM > threshold). Each clause "
            "operates at its correct stage in the pipeline.\n\n"

            "HAVING can reference any aggregate expression, even ones not in SELECT. For example, "
            "HAVING COUNT(*) > 3 is valid even if COUNT(*) isn't in your SELECT list. However, "
            "for readability, it's good practice to include the aggregate in SELECT when you filter by it.\n\n"

            "A practical use case is finding \"top N groups.\" For example, find departments where "
            "the average salary exceeds the company average. Or find product categories with more "
            "than 100 total sales. These are classic interview questions that combine GROUP BY, "
            "HAVING, and sometimes subqueries."
        ),
        key_points=[
            "WHERE filters rows before grouping; HAVING filters groups after aggregation.",
            "SQL execution order: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT.",
            "HAVING can reference aggregate functions; WHERE cannot.",
            "You can use both WHERE and HAVING in the same query — they operate at different stages.",
            "HAVING can reference aggregates not present in the SELECT list.",
        ],
        syntax="SELECT group_col, AGG(col)\nFROM table\n[WHERE row_condition]\nGROUP BY group_col\nHAVING AGG(col) condition;",
        examples=[
            SQLExample(
                title="Departments with many employees",
                sql="SELECT department_id, COUNT(*) AS emp_count\nFROM employees\nGROUP BY department_id\nHAVING COUNT(*) > 5\nORDER BY emp_count DESC;",
                explanation=(
                    "Groups employees by department, counts each group, then filters to only "
                    "departments with more than 5 employees. The remaining groups are sorted "
                    "by count in descending order."
                ),
            ),
            SQLExample(
                title="WHERE + HAVING combined",
                sql="SELECT department_id, AVG(salary) AS avg_sal\nFROM employees\nWHERE hire_date >= '2020-01-01'\nGROUP BY department_id\nHAVING AVG(salary) > 70000;",
                explanation=(
                    "First filters to employees hired in 2020 or later (WHERE). Then groups by "
                    "department and computes average salary. Finally, keeps only departments where "
                    "that average exceeds 70,000 (HAVING)."
                ),
            ),
            SQLExample(
                title="Top-spending customers",
                sql="SELECT customer_id,\n       COUNT(*) AS order_count,\n       SUM(total) AS total_spent\nFROM orders\nGROUP BY customer_id\nHAVING SUM(total) > 500\nORDER BY total_spent DESC\nLIMIT 10;",
                explanation=(
                    "Finds the top 10 customers who have spent more than $500 total. Combines "
                    "GROUP BY, HAVING, ORDER BY, and LIMIT in a single practical query."
                ),
            ),
        ],
        quiz=[
            QuizQuestion(
                "Can you use WHERE to filter by an aggregate like COUNT(*) > 5?",
                "No. WHERE runs before GROUP BY, so aggregates haven't been computed yet. You must use HAVING for aggregate conditions.",
            ),
            QuizQuestion(
                "In what order does SQL logically execute FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY?",
                "FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT. This is different from the order they appear in the written query.",
            ),
            QuizQuestion(
                "Can HAVING be used without GROUP BY?",
                "Technically yes — the entire table is treated as one group. But it is very rare and almost always GROUP BY is present when HAVING is used.",
            ),
        ],
        tips=[
            "In interviews, if asked 'WHERE vs HAVING' — answer in terms of execution order. WHERE filters rows before grouping, HAVING filters groups after aggregation.",
            "If you need to filter by both a row-level condition and an aggregate condition, always put the row-level one in WHERE for better performance — fewer rows to aggregate.",
            "Memorize the SQL execution order (FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT) — it explains many SQL behaviors.",
        ],
    ),
]

# ---------------------------------------------------------------------------
# PATH 4 — Subqueries & CTEs
# ---------------------------------------------------------------------------

_subqueries_steps = [
    PathStep(
        title="Simple Subqueries",
        description="Use subqueries in WHERE and SELECT to compose nested logic.",
        task_ids=[13, 14],
        example_sql="SELECT * FROM employees\nWHERE salary > (SELECT AVG(salary) FROM employees);",
        theory=(
            "A subquery is a SELECT statement nested inside another query. It lets you use "
            "the result of one query as an input to another. Subqueries can appear in three main "
            "places: in the WHERE clause, in the SELECT clause, and in the FROM clause.\n\n"

            "WHERE subqueries are the most common. A scalar subquery returns a single value and can "
            "be used with comparison operators: WHERE salary > (SELECT AVG(salary) FROM employees). "
            "The inner query computes the average salary, and the outer query uses that value to "
            "filter employees. The subquery runs first, produces one number, and that number is "
            "plugged into the comparison.\n\n"

            "When a subquery returns multiple rows, you use set operators instead of simple "
            "comparisons. IN checks if a value is in the set: WHERE department_id IN (SELECT id FROM "
            "departments WHERE location = 'NYC'). This finds all employees in NYC departments. "
            "You can also use NOT IN to exclude values, but be careful — if the subquery returns any "
            "NULL values, NOT IN will return no rows at all (a common trap).\n\n"

            "EXISTS checks whether a subquery returns at least one row, regardless of what that row "
            "contains. WHERE EXISTS (SELECT 1 FROM orders WHERE orders.customer_id = customers.id) "
            "finds customers who have at least one order. EXISTS is often more efficient than IN "
            "for large datasets because it can stop scanning as soon as it finds the first match.\n\n"

            "SELECT-clause subqueries (scalar subqueries) add a computed column to each row: "
            "SELECT name, (SELECT COUNT(*) FROM orders WHERE orders.customer_id = customers.id) AS order_count "
            "FROM customers. The subquery runs once per row in the outer query. FROM-clause subqueries "
            "(derived tables) create a temporary table: SELECT * FROM (SELECT ... ) AS derived. "
            "These are useful for breaking complex logic into steps."
        ),
        key_points=[
            "Scalar subqueries return one value — use with =, >, <, etc.",
            "Set subqueries return multiple rows — use with IN, NOT IN, ANY, ALL.",
            "EXISTS checks if at least one row exists — efficient for existence checks.",
            "NOT IN with NULLs in the subquery returns no rows — a common trap. Prefer NOT EXISTS.",
            "FROM-clause subqueries (derived tables) create a temporary result set you can query further.",
        ],
        syntax="-- WHERE subquery\nSELECT * FROM t WHERE col > (SELECT AGG(col) FROM t2);\n-- IN subquery\nSELECT * FROM t WHERE col IN (SELECT col FROM t2 WHERE ...);\n-- EXISTS\nSELECT * FROM t WHERE EXISTS (SELECT 1 FROM t2 WHERE t2.fk = t.pk);",
        examples=[
            SQLExample(
                title="Scalar subquery — above-average salary",
                sql="SELECT first_name, salary\nFROM employees\nWHERE salary > (SELECT AVG(salary) FROM employees);",
                explanation=(
                    "The inner query computes the average salary across all employees. The outer query "
                    "returns only employees whose salary exceeds that average. The subquery produces one number."
                ),
            ),
            SQLExample(
                title="IN subquery — employees in specific departments",
                sql="SELECT first_name, department_id\nFROM employees\nWHERE department_id IN (\n  SELECT id FROM departments WHERE name LIKE '%Engineering%'\n);",
                explanation=(
                    "The inner query finds IDs of engineering departments. The outer query returns "
                    "employees whose department_id is in that set. Equivalent to a JOIN but sometimes clearer."
                ),
            ),
            SQLExample(
                title="EXISTS — customers with orders",
                sql="SELECT c.name\nFROM customers c\nWHERE EXISTS (\n  SELECT 1 FROM orders o WHERE o.customer_id = c.id\n);",
                explanation=(
                    "For each customer, the subquery checks if any order exists. EXISTS returns true "
                    "as soon as it finds one matching row, making it efficient. SELECT 1 is a convention — "
                    "the actual value doesn't matter."
                ),
            ),
            SQLExample(
                title="FROM subquery (derived table)",
                sql="SELECT dept, avg_sal\nFROM (\n  SELECT department_id AS dept, AVG(salary) AS avg_sal\n  FROM employees\n  GROUP BY department_id\n) AS dept_avgs\nWHERE avg_sal > 80000;",
                explanation=(
                    "The inner query groups by department and computes averages. The outer query "
                    "treats it as a temporary table (must have an alias) and filters for high averages."
                ),
            ),
        ],
        quiz=[
            QuizQuestion(
                "What happens if you use NOT IN and the subquery contains a NULL value?",
                "NOT IN returns no rows when NULLs are present because the comparison col != NULL evaluates to unknown, making the entire NOT IN condition unknown. Use NOT EXISTS instead.",
            ),
            QuizQuestion(
                "What is the difference between a scalar subquery and a set subquery?",
                "A scalar subquery returns exactly one value (one row, one column) and can be used with comparison operators. A set subquery returns multiple rows and is used with IN, ANY, ALL, or EXISTS.",
            ),
            QuizQuestion(
                "Why might EXISTS be more efficient than IN for large datasets?",
                "EXISTS can stop scanning the subquery as soon as it finds the first match (short-circuit evaluation), while IN may need to build the complete result set first.",
            ),
        ],
        tips=[
            "In interviews, always prefer NOT EXISTS over NOT IN when the subquery might contain NULLs — this avoids a subtle and common bug.",
            "Many subqueries can be rewritten as JOINs. Practice both forms — interviewers may ask you to convert between them.",
            "A scalar subquery in SELECT runs once per row in the outer query. For large datasets, a JOIN is usually more efficient.",
        ],
    ),

    PathStep(
        title="Correlated Subqueries",
        description="Subqueries that reference the outer query for row-by-row logic.",
        task_ids=[15],
        example_sql=None,
        theory=(
            "A correlated subquery references columns from the outer query, so it executes "
            "once for each row in the outer query. This is different from a regular subquery, "
            "which runs once and its result is reused. Correlated subqueries are more powerful "
            "but can be slower because of the per-row execution.\n\n"

            "A classic example: find employees who earn more than the average salary in their own "
            "department. The subquery must know which department each employee belongs to: "
            "WHERE salary > (SELECT AVG(salary) FROM employees e2 WHERE e2.department_id = e1.department_id). "
            "Here, e1.department_id comes from the outer query, making this correlated. For each "
            "employee, the subquery computes the average for their specific department and compares.\n\n"

            "EXISTS and NOT EXISTS are the most common places you'll see correlated subqueries. "
            "WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id) is correlated "
            "because it references c.id from the outer customers table. For each customer, the "
            "database checks if any order exists for that customer.\n\n"

            "NOT EXISTS vs NOT IN is a critical distinction. NOT IN has a NULL trap: if the "
            "subquery returns any NULL value, NOT IN evaluates to unknown for every row, and "
            "no rows are returned. NOT EXISTS does not have this problem because it simply "
            "checks whether the subquery returns any rows, regardless of NULL values. Always "
            "prefer NOT EXISTS when the subquery column might contain NULLs.\n\n"

            "Performance-wise, modern query optimizers can often transform correlated subqueries "
            "into joins internally. However, it's good practice to understand both forms. In "
            "some cases (especially with EXISTS/NOT EXISTS), the correlated form is actually "
            "clearer and more natural than the equivalent join."
        ),
        key_points=[
            "A correlated subquery references the outer query and runs once per outer row.",
            "Regular subqueries run once; correlated subqueries run once per row — potentially slower.",
            "NOT EXISTS is safer than NOT IN when NULLs are possible in the subquery result.",
            "EXISTS with a correlated subquery is the standard way to check for related rows.",
            "Modern optimizers often convert correlated subqueries to joins internally.",
        ],
        syntax="SELECT *\nFROM table_a a\nWHERE a.col > (\n  SELECT AGG(b.col) FROM table_b b WHERE b.key = a.key\n);",
        examples=[
            SQLExample(
                title="Above department average",
                sql="SELECT e1.first_name, e1.salary, e1.department_id\nFROM employees e1\nWHERE e1.salary > (\n  SELECT AVG(e2.salary)\n  FROM employees e2\n  WHERE e2.department_id = e1.department_id\n);",
                explanation=(
                    "For each employee (e1), the subquery computes the average salary of their "
                    "specific department. The outer query keeps only employees who earn above that average. "
                    "The reference to e1.department_id makes this correlated."
                ),
            ),
            SQLExample(
                title="NOT EXISTS — customers with no orders",
                sql="SELECT c.name\nFROM customers c\nWHERE NOT EXISTS (\n  SELECT 1 FROM orders o WHERE o.customer_id = c.id\n);",
                explanation=(
                    "For each customer, the subquery checks if any order exists. NOT EXISTS returns "
                    "true when the subquery returns zero rows — finding customers who have never ordered. "
                    "This is NULL-safe, unlike NOT IN."
                ),
            ),
            SQLExample(
                title="Correlated subquery in SELECT",
                sql="SELECT e.first_name,\n       e.salary,\n       (SELECT COUNT(*)\n        FROM employees e2\n        WHERE e2.department_id = e.department_id) AS dept_size\nFROM employees e;",
                explanation=(
                    "For each employee, the scalar subquery counts how many employees are in their "
                    "department. The result is added as a column. This is equivalent to a window function "
                    "COUNT(*) OVER (PARTITION BY department_id)."
                ),
            ),
        ],
        quiz=[
            QuizQuestion(
                "Why does NOT IN fail when the subquery result contains NULLs?",
                "Because x NOT IN (..., NULL, ...) evaluates x != NULL for each comparison, which yields unknown. Since one unknown makes the entire NOT IN unknown, no rows pass the filter.",
            ),
            QuizQuestion(
                "How does a correlated subquery differ from a regular subquery in execution?",
                "A regular subquery runs once and its result is reused. A correlated subquery references the outer query and must re-execute for each row in the outer query.",
            ),
            QuizQuestion(
                "Can a correlated subquery be rewritten as a JOIN?",
                "Often yes. For example, NOT EXISTS can be rewritten as LEFT JOIN + IS NULL. The optimizer may do this automatically, but knowing both forms is valuable.",
            ),
        ],
        tips=[
            "NOT EXISTS vs NOT IN is a classic interview question. Always explain the NULL trap and recommend NOT EXISTS as the safer option.",
            "When writing a correlated subquery, make sure your aliases are distinct and clearly show which table belongs to the outer vs inner query.",
            "If a correlated subquery is slow, consider rewriting it as a JOIN or using a window function — both often perform better.",
        ],
    ),

    PathStep(
        title="CTEs with WITH",
        description="Use Common Table Expressions (CTEs) to organize complex queries.",
        task_ids=[19, 20, 21],
        example_sql="WITH totals AS (\n  SELECT dept_id, SUM(salary) AS s\n  FROM emp GROUP BY dept_id\n)\nSELECT * FROM totals;",
        theory=(
            "A Common Table Expression (CTE) is a named temporary result set defined at the "
            "beginning of a query using the WITH keyword. Think of it as giving a name to a "
            "subquery so you can reference it like a table in the main query. CTEs make complex "
            "queries dramatically more readable by breaking them into logical, named steps.\n\n"

            "The basic syntax is: WITH cte_name AS (SELECT ...) SELECT ... FROM cte_name. "
            "The CTE is defined once and can be referenced multiple times in the main query. "
            "This is a key advantage over derived tables (FROM subqueries), which you'd have to "
            "copy-paste if you need them in multiple places.\n\n"

            "You can define multiple CTEs separated by commas, and later CTEs can reference "
            "earlier ones. This creates a pipeline of data transformations: "
            "WITH step1 AS (...), step2 AS (SELECT ... FROM step1 ...) SELECT ... FROM step2. "
            "Each CTE builds on the previous one, making complex analytical queries read like "
            "a sequence of simple steps.\n\n"

            "Recursive CTEs solve problems involving hierarchical or graph data. A recursive CTE "
            "has two parts: the base case (anchor member) and the recursive step. For example, "
            "to traverse an org chart: the base case selects the CEO (WHERE manager_id IS NULL), "
            "and the recursive step joins back to the CTE to find each level of reports. "
            "The syntax is WITH RECURSIVE cte AS (base UNION ALL recursive_step).\n\n"

            "CTEs are also the preferred way to structure interview solutions. When an interviewer "
            "gives you a complex problem, sketch out the steps as CTEs: first compute this, then "
            "join that, then filter. It shows clear thinking and makes your solution easy to follow. "
            "Performance-wise, most modern databases (including PostgreSQL 12+) inline CTEs into "
            "the main query and optimize them together, so there is usually no performance penalty."
        ),
        key_points=[
            "CTEs (WITH clauses) name temporary result sets for use in the main query.",
            "A CTE can be referenced multiple times — unlike a derived table which must be duplicated.",
            "Multiple CTEs are separated by commas; later CTEs can reference earlier ones.",
            "Recursive CTEs (WITH RECURSIVE) solve hierarchical data problems like org charts.",
            "CTEs improve readability and are the preferred way to structure complex interview solutions.",
        ],
        syntax="WITH cte_name AS (\n  SELECT ...\n),\ncte2 AS (\n  SELECT ... FROM cte_name ...\n)\nSELECT ...\nFROM cte2\n...;",
        examples=[
            SQLExample(
                title="Basic CTE — department salary totals",
                sql="WITH dept_totals AS (\n  SELECT department_id,\n         SUM(salary) AS total_salary,\n         COUNT(*) AS emp_count\n  FROM employees\n  GROUP BY department_id\n)\nSELECT d.name, dt.total_salary, dt.emp_count\nFROM dept_totals dt\nJOIN departments d ON dt.department_id = d.id\nORDER BY dt.total_salary DESC;",
                explanation=(
                    "The CTE computes salary totals and headcount per department. The main query "
                    "joins to the departments table for names and sorts by total salary. The logic "
                    "is broken into two clear steps."
                ),
            ),
            SQLExample(
                title="Multiple CTEs — pipeline pattern",
                sql="WITH monthly_sales AS (\n  SELECT DATE_TRUNC('month', ordered_at) AS month,\n         SUM(total) AS revenue\n  FROM orders\n  GROUP BY 1\n),\nwith_growth AS (\n  SELECT month, revenue,\n         LAG(revenue) OVER (ORDER BY month) AS prev_revenue\n  FROM monthly_sales\n)\nSELECT month, revenue,\n       ROUND((revenue - prev_revenue) / prev_revenue * 100, 1) AS growth_pct\nFROM with_growth\nWHERE prev_revenue IS NOT NULL;",
                explanation=(
                    "First CTE computes monthly revenue. Second CTE adds the previous month's revenue "
                    "using LAG. The main query calculates month-over-month growth percentage. "
                    "Each step is clear and testable independently."
                ),
            ),
            SQLExample(
                title="Recursive CTE — org chart",
                sql="WITH RECURSIVE org AS (\n  SELECT id, first_name, manager_id, 1 AS level\n  FROM employees\n  WHERE manager_id IS NULL\n  UNION ALL\n  SELECT e.id, e.first_name, e.manager_id, o.level + 1\n  FROM employees e\n  JOIN org o ON e.manager_id = o.id\n)\nSELECT * FROM org ORDER BY level, first_name;",
                explanation=(
                    "The anchor selects the top-level employee (no manager). The recursive step finds "
                    "employees whose manager is already in the result, incrementing the level. "
                    "This builds the complete org hierarchy with depth levels."
                ),
            ),
        ],
        quiz=[
            QuizQuestion(
                "What is the advantage of a CTE over a derived table (FROM subquery)?",
                "A CTE can be referenced multiple times in the same query without copy-pasting, and it improves readability by giving a meaningful name to intermediate results.",
            ),
            QuizQuestion(
                "What are the two parts of a recursive CTE?",
                "The anchor member (base case) which runs once, and the recursive member which references the CTE itself and runs repeatedly until no new rows are produced. They are combined with UNION ALL.",
            ),
            QuizQuestion(
                "Can a CTE reference another CTE defined before it?",
                "Yes. In a WITH clause with multiple CTEs, later CTEs can reference earlier ones. This enables a pipeline pattern where each step builds on the previous.",
            ),
        ],
        tips=[
            "In interviews, always use CTEs to structure complex queries — it shows clear thinking and is much easier for the interviewer to follow.",
            "Name your CTEs descriptively (monthly_revenue, active_users) not generically (temp, data). The name should explain what the CTE contains.",
            "Recursive CTEs need a termination condition. Without one (e.g., a cycle in hierarchical data), the recursion runs forever. PostgreSQL has a default recursion limit to prevent this.",
        ],
    ),
]

# ---------------------------------------------------------------------------
# PATH 5 — Window Functions
# ---------------------------------------------------------------------------

_window_steps = [
    PathStep(
        title="RANK & ROW_NUMBER",
        description="Rank rows within partitions using window functions.",
        task_ids=[16],
        example_sql="SELECT name, salary,\n       RANK() OVER (ORDER BY salary DESC)\nFROM employees;",
        theory=(
            "Window functions perform calculations across a set of rows related to the current "
            "row — without collapsing them into a single output like GROUP BY does. This is the key "
            "difference: GROUP BY reduces many rows to one per group, while window functions keep "
            "every row and add a computed value alongside it.\n\n"

            "Every window function uses the OVER() clause to define its window. The simplest form "
            "is OVER() with nothing inside — the window is the entire result set. OVER(ORDER BY salary DESC) "
            "defines a window ordered by salary. OVER(PARTITION BY department_id ORDER BY salary DESC) "
            "splits the data into groups by department and orders within each group.\n\n"

            "The three most common ranking functions are:\n"
            "- ROW_NUMBER() assigns a unique sequential number (1, 2, 3...) with no gaps and no ties.\n"
            "- RANK() assigns the same number to tied rows and leaves gaps (1, 2, 2, 4).\n"
            "- DENSE_RANK() assigns the same number to ties but without gaps (1, 2, 2, 3).\n\n"

            "PARTITION BY is like GROUP BY for window functions — it splits the data into independent "
            "partitions. RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) ranks employees "
            "within each department separately: the highest-paid person in each department gets rank 1.\n\n"

            "A powerful pattern is \"top N per group\": find the top 3 earners in each department. "
            "You cannot do this with simple GROUP BY. The solution: use a CTE or subquery to assign "
            "ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC), then filter WHERE row_num <= 3 "
            "in the outer query. This is one of the most common SQL interview questions."
        ),
        key_points=[
            "Window functions compute values across rows without collapsing them (unlike GROUP BY).",
            "OVER() defines the window; PARTITION BY splits into groups, ORDER BY sorts within each.",
            "ROW_NUMBER: unique sequential numbers. RANK: ties get same rank, gaps follow. DENSE_RANK: ties, no gaps.",
            "Top-N-per-group: use ROW_NUMBER + PARTITION BY in a subquery, filter in outer query.",
            "Window functions execute after WHERE, GROUP BY, and HAVING — but before ORDER BY and LIMIT.",
        ],
        syntax="SELECT col,\n       ROW_NUMBER() OVER (PARTITION BY grp ORDER BY sort_col DESC) AS rn,\n       RANK() OVER (PARTITION BY grp ORDER BY sort_col DESC) AS rnk,\n       DENSE_RANK() OVER (PARTITION BY grp ORDER BY sort_col DESC) AS drnk\nFROM table;",
        examples=[
            SQLExample(
                title="ROW_NUMBER vs RANK vs DENSE_RANK",
                sql="SELECT first_name, salary,\n       ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num,\n       RANK()       OVER (ORDER BY salary DESC) AS rnk,\n       DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rnk\nFROM employees;",
                explanation=(
                    "If two employees both earn $95,000 (the highest), ROW_NUMBER gives them 1 and 2 "
                    "(arbitrary tiebreak), RANK gives both 1 then skips to 3, DENSE_RANK gives both 1 "
                    "then continues to 2. The choice depends on your use case."
                ),
            ),
            SQLExample(
                title="Rank within partitions",
                sql="SELECT first_name, department_id, salary,\n       RANK() OVER (\n         PARTITION BY department_id\n         ORDER BY salary DESC\n       ) AS dept_rank\nFROM employees;",
                explanation=(
                    "PARTITION BY splits employees into groups by department. Within each department, "
                    "employees are ranked by salary independently. Department 1's rank 1 and department 2's "
                    "rank 1 are different employees."
                ),
            ),
            SQLExample(
                title="Top 3 per department",
                sql="WITH ranked AS (\n  SELECT first_name, department_id, salary,\n         ROW_NUMBER() OVER (\n           PARTITION BY department_id\n           ORDER BY salary DESC\n         ) AS rn\n  FROM employees\n)\nSELECT * FROM ranked WHERE rn <= 3;",
                explanation=(
                    "The CTE assigns a row number within each department by salary. The outer query "
                    "filters to keep only the top 3. This is the classic \"top N per group\" pattern — "
                    "one of the most asked SQL interview questions."
                ),
            ),
        ],
        quiz=[
            QuizQuestion(
                "What is the key difference between GROUP BY and window functions?",
                "GROUP BY collapses rows into one per group. Window functions keep every row and add a computed column alongside. You can see both the detail and the aggregate.",
            ),
            QuizQuestion(
                "If three employees have the same salary, what does RANK assign them vs DENSE_RANK?",
                "RANK assigns all three the same rank (e.g., 2, 2, 2) then skips to 5. DENSE_RANK also assigns 2, 2, 2 but continues with 3 (no gap).",
            ),
            QuizQuestion(
                "How do you solve 'top N per group' in SQL?",
                "Use ROW_NUMBER() OVER (PARTITION BY group_col ORDER BY sort_col) in a CTE or subquery, then filter WHERE row_num <= N in the outer query.",
            ),
        ],
        tips=[
            "\"Top N per group\" is one of the most common SQL interview questions. Practice the ROW_NUMBER + CTE pattern until it's second nature.",
            "Choose ROW_NUMBER for unique assignments (pagination), RANK when gaps are acceptable, DENSE_RANK when you need consecutive ranking with ties.",
            "You cannot filter on window functions in the same SELECT (WHERE rn <= 3 fails). Always wrap in a subquery or CTE first.",
        ],
    ),

    PathStep(
        title="Running Totals",
        description="Compute cumulative sums and moving averages with window frames.",
        task_ids=[17],
        example_sql="SELECT id, total,\n       SUM(total) OVER (ORDER BY ordered_at) AS running_total\nFROM orders;",
        theory=(
            "Window functions become even more powerful when combined with aggregate functions "
            "like SUM, AVG, COUNT, MIN, and MAX. Instead of collapsing rows, these aggregates "
            "compute a running value across a defined window frame — a sliding set of rows relative "
            "to the current row.\n\n"

            "The simplest running total uses SUM with an ordered window: "
            "SUM(total) OVER (ORDER BY ordered_at). For each row, this sums all totals from the "
            "start up to and including the current row. The result is a cumulative sum that grows "
            "as you move down the rows. This is invaluable for financial reporting, tracking "
            "cumulative revenue, or monitoring running balances.\n\n"

            "By default, when you specify ORDER BY in OVER(), the window frame is "
            "ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW — everything from the start to the "
            "current row. You can customize this frame explicitly. Common frame specifications:\n"
            "- ROWS BETWEEN 2 PRECEDING AND CURRENT ROW — a 3-row moving window\n"
            "- ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING — the entire partition\n"
            "- ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING — centered 3-row window\n\n"

            "Moving averages are a common use case: "
            "AVG(revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) computes "
            "a 3-month moving average. This smooths out noise in time series data and is widely "
            "used in financial analysis, dashboards, and data science.\n\n"

            "You can combine PARTITION BY with frame specifications. For example, compute a running "
            "total per customer: SUM(total) OVER (PARTITION BY customer_id ORDER BY ordered_at). "
            "Each customer gets their own independent running total. The frame resets at each "
            "partition boundary."
        ),
        key_points=[
            "SUM() OVER (ORDER BY ...) produces a running (cumulative) total.",
            "The default frame with ORDER BY is ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW.",
            "Custom frames like ROWS BETWEEN N PRECEDING AND CURRENT ROW create moving windows.",
            "Moving averages smooth time-series data: AVG() OVER (ORDER BY date ROWS BETWEEN N PRECEDING AND CURRENT ROW).",
            "PARTITION BY resets the running total for each group independently.",
        ],
        syntax="SELECT col,\n       SUM(val) OVER (\n         [PARTITION BY grp]\n         ORDER BY sort_col\n         [ROWS BETWEEN frame_start AND frame_end]\n       ) AS running_total\nFROM table;",
        examples=[
            SQLExample(
                title="Running total of order revenue",
                sql="SELECT id, ordered_at, total,\n       SUM(total) OVER (ORDER BY ordered_at) AS running_total\nFROM orders;",
                explanation=(
                    "For each order, running_total shows the cumulative sum of all orders up to and "
                    "including this one. The last row's running_total equals the total of all orders."
                ),
            ),
            SQLExample(
                title="3-month moving average",
                sql="WITH monthly AS (\n  SELECT DATE_TRUNC('month', ordered_at) AS month,\n         SUM(total) AS revenue\n  FROM orders\n  GROUP BY 1\n)\nSELECT month, revenue,\n       ROUND(AVG(revenue) OVER (\n         ORDER BY month\n         ROWS BETWEEN 2 PRECEDING AND CURRENT ROW\n       ), 2) AS moving_avg_3m\nFROM monthly;",
                explanation=(
                    "First aggregates orders by month. Then computes a 3-month moving average (current "
                    "month plus two prior months). This smooths out month-to-month volatility and reveals trends."
                ),
            ),
            SQLExample(
                title="Running total per customer",
                sql="SELECT customer_id, ordered_at, total,\n       SUM(total) OVER (\n         PARTITION BY customer_id\n         ORDER BY ordered_at\n       ) AS customer_running_total\nFROM orders;",
                explanation=(
                    "PARTITION BY customer_id gives each customer their own running total. "
                    "Customer A's cumulative spend is independent of Customer B's. The running total "
                    "resets at each partition boundary."
                ),
            ),
        ],
        quiz=[
            QuizQuestion(
                "What is the default window frame when ORDER BY is specified in OVER()?",
                "ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW — from the first row in the partition to the current row.",
            ),
            QuizQuestion(
                "How do you compute a 7-day moving average?",
                "AVG(value) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW). The window includes the current row plus 6 preceding rows for a total of 7 rows.",
            ),
            QuizQuestion(
                "What happens to the running total at a partition boundary?",
                "It resets. Each partition is treated as an independent group, so the running total starts fresh at 0 for each new partition.",
            ),
        ],
        tips=[
            "Running totals and moving averages are heavily used in analytics interviews. Practice computing cumulative revenue and 7-day averages.",
            "Be aware of ROWS vs RANGE: ROWS counts physical rows, RANGE considers logical value ranges. For most use cases, ROWS is what you want.",
            "If you omit the frame clause but include ORDER BY, the default frame is UNBOUNDED PRECEDING to CURRENT ROW — not the entire partition.",
        ],
    ),

    PathStep(
        title="LAG & LEAD",
        description="Access previous and next row values for period-over-period analysis.",
        task_ids=[18],
        example_sql="SELECT song,\n       LAG(song) OVER (PARTITION BY user_id ORDER BY streamed_at)\nFROM streams;",
        theory=(
            "LAG and LEAD let you access values from other rows relative to the current row "
            "without using a self-join. LAG looks backward (previous rows), LEAD looks forward "
            "(next rows). They are essential for period-over-period comparisons, calculating changes, "
            "and detecting transitions.\n\n"

            "The syntax is LAG(column, offset, default) OVER (ORDER BY ...). The offset defaults "
            "to 1 (previous row). The default parameter specifies what to return when there is no "
            "previous row (instead of NULL). For example: LAG(revenue, 1, 0) OVER (ORDER BY month) "
            "returns the previous month's revenue, or 0 for the first month.\n\n"

            "The most common use case is period-over-period growth. To compute month-over-month "
            "revenue change: first get monthly totals, then use LAG to get the previous month's "
            "revenue, and finally calculate (current - previous) / previous * 100 for the percentage "
            "change. This is an extremely common analytics query and interview question.\n\n"

            "LAG and LEAD work beautifully with PARTITION BY. "
            "LAG(salary) OVER (PARTITION BY department_id ORDER BY hire_date) gives you the previous "
            "hire's salary within each department. Each partition is independent — the first person "
            "hired in each department has no LAG value (NULL).\n\n"

            "Two related functions are FIRST_VALUE and LAST_VALUE. FIRST_VALUE returns the first "
            "value in the window frame, and LAST_VALUE returns the last. Be careful with LAST_VALUE: "
            "with the default frame (UNBOUNDED PRECEDING to CURRENT ROW), LAST_VALUE always returns "
            "the current row's value. To get the actual last value in the partition, you need to "
            "specify ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING."
        ),
        key_points=[
            "LAG(col, n) accesses the value n rows before the current row; LEAD(col, n) accesses n rows after.",
            "The third parameter is the default value when there is no previous/next row (instead of NULL).",
            "Period-over-period growth = (current - LAG) / LAG * 100.",
            "FIRST_VALUE and LAST_VALUE return the first/last values in the window frame.",
            "LAST_VALUE with the default frame returns the current row — specify UNBOUNDED FOLLOWING to get the actual last value.",
        ],
        syntax="SELECT col,\n       LAG(col, 1) OVER (ORDER BY sort_col) AS prev_val,\n       LEAD(col, 1) OVER (ORDER BY sort_col) AS next_val,\n       col - LAG(col, 1) OVER (ORDER BY sort_col) AS change\nFROM table;",
        examples=[
            SQLExample(
                title="Month-over-month revenue growth",
                sql="WITH monthly AS (\n  SELECT DATE_TRUNC('month', ordered_at) AS month,\n         SUM(total) AS revenue\n  FROM orders\n  GROUP BY 1\n)\nSELECT month, revenue,\n       LAG(revenue) OVER (ORDER BY month) AS prev_month,\n       ROUND(\n         (revenue - LAG(revenue) OVER (ORDER BY month))\n         / LAG(revenue) OVER (ORDER BY month) * 100, 1\n       ) AS growth_pct\nFROM monthly;",
                explanation=(
                    "LAG(revenue) OVER (ORDER BY month) retrieves the previous month's revenue. "
                    "The growth calculation divides the difference by the previous value. "
                    "The first month shows NULL because there is no prior month to compare to."
                ),
            ),
            SQLExample(
                title="LEAD — next event analysis",
                sql="SELECT user_id, event_type, created_at,\n       LEAD(event_type) OVER (\n         PARTITION BY user_id ORDER BY created_at\n       ) AS next_event,\n       LEAD(created_at) OVER (\n         PARTITION BY user_id ORDER BY created_at\n       ) - created_at AS time_to_next\nFROM events;",
                explanation=(
                    "For each event, shows what the user did next and how long it took. "
                    "This is the foundation of funnel and session analysis. The last event "
                    "for each user shows NULL for next_event."
                ),
            ),
            SQLExample(
                title="FIRST_VALUE — best in each group",
                sql="SELECT first_name, department_id, salary,\n       FIRST_VALUE(first_name) OVER (\n         PARTITION BY department_id\n         ORDER BY salary DESC\n       ) AS top_earner\nFROM employees;",
                explanation=(
                    "FIRST_VALUE with ORDER BY salary DESC gives the highest-paid person in each "
                    "department. Every row in the department sees the same top_earner value."
                ),
            ),
        ],
        quiz=[
            QuizQuestion(
                "What does LAG(salary, 2) return?",
                "The salary value from 2 rows before the current row (based on the ORDER BY in the OVER clause). If there are fewer than 2 preceding rows, it returns NULL.",
            ),
            QuizQuestion(
                "Why does LAST_VALUE often return the current row's value instead of the actual last value?",
                "Because the default frame is ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW. The 'last' value in this frame is always the current row. Use ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING to get the true last value.",
            ),
            QuizQuestion(
                "How do you calculate period-over-period percentage change using LAG?",
                "ROUND((current_value - LAG(current_value) OVER (ORDER BY period)) / LAG(current_value) OVER (ORDER BY period) * 100, 1). The formula is (new - old) / old * 100.",
            ),
        ],
        tips=[
            "Period-over-period growth using LAG is a top analytics interview question. Practice it until the pattern is automatic.",
            "If you need LAG with a default value for the first row, use the third parameter: LAG(revenue, 1, 0) to avoid NULL.",
            "When computing changes, always handle the NULL case (first row has no LAG). Use COALESCE or filter with WHERE prev IS NOT NULL.",
        ],
    ),
]

# ---------------------------------------------------------------------------
# PATH 6 — Interview Ready
# ---------------------------------------------------------------------------

_interview_steps = [
    PathStep(
        title="CASE Expressions",
        description="Add conditional logic to your SQL queries.",
        task_ids=[22, 23, 24],
        example_sql="SELECT name,\n       CASE WHEN salary > 95000 THEN 'Senior'\n            ELSE 'Junior' END AS level\nFROM employees;",
        theory=(
            "CASE expressions bring conditional logic — similar to if/else in programming — directly "
            "into SQL queries. They evaluate conditions in order and return a value for the first "
            "condition that is true. If no condition matches and there is no ELSE clause, NULL is returned.\n\n"

            "The searched CASE form is the most flexible: CASE WHEN condition1 THEN result1 "
            "WHEN condition2 THEN result2 ELSE default END. Each WHEN is an independent boolean "
            "expression, so you can use different columns, complex logic, and even subqueries. "
            "There is also a simple CASE form: CASE column WHEN value1 THEN result1 ... END, which "
            "is shorthand for equality checks on a single column.\n\n"

            "One of the most powerful patterns is conditional aggregation — combining CASE with "
            "aggregate functions. For example: SELECT department_id, "
            "COUNT(CASE WHEN salary > 80000 THEN 1 END) AS high_earners, "
            "COUNT(CASE WHEN salary <= 80000 THEN 1 END) AS others. This pivots data from rows "
            "to columns in a single query, counting different categories within each group.\n\n"

            "COALESCE(a, b, c) returns the first non-NULL value from its arguments. It's a "
            "shortcut for CASE WHEN a IS NOT NULL THEN a WHEN b IS NOT NULL THEN b ELSE c END. "
            "Common uses: providing defaults (COALESCE(nickname, first_name)), handling missing "
            "data, and preventing division by zero in combination with NULLIF.\n\n"

            "NULLIF(a, b) returns NULL if a equals b, otherwise returns a. Its main use is "
            "preventing division by zero: revenue / NULLIF(cost, 0) returns NULL instead of "
            "crashing when cost is zero. COALESCE and NULLIF together are a powerful pair: "
            "COALESCE(revenue / NULLIF(cost, 0), 0) gives you the ratio, or 0 if cost is zero."
        ),
        key_points=[
            "CASE WHEN evaluates conditions in order, returns the first match. No match without ELSE returns NULL.",
            "Conditional aggregation: COUNT/SUM(CASE WHEN ... THEN ... END) pivots rows into columns.",
            "COALESCE returns the first non-NULL argument — use it for default values.",
            "NULLIF(a, b) returns NULL if a = b — use it to prevent division by zero.",
            "CASE works in SELECT, WHERE, ORDER BY, GROUP BY, and even inside aggregate functions.",
        ],
        syntax="CASE\n  WHEN condition1 THEN result1\n  WHEN condition2 THEN result2\n  ELSE default_result\nEND",
        examples=[
            SQLExample(
                title="Categorize with CASE",
                sql="SELECT first_name, salary,\n       CASE\n         WHEN salary >= 100000 THEN 'Executive'\n         WHEN salary >= 75000  THEN 'Senior'\n         WHEN salary >= 50000  THEN 'Mid'\n         ELSE 'Junior'\n       END AS level\nFROM employees\nORDER BY salary DESC;",
                explanation=(
                    "Each employee is classified into a salary tier. Conditions are checked top "
                    "to bottom — an employee earning $110k matches 'Executive' first and stops. "
                    "The ELSE catches anyone below $50k."
                ),
            ),
            SQLExample(
                title="Conditional aggregation (pivot)",
                sql="SELECT department_id,\n       COUNT(*) AS total,\n       COUNT(CASE WHEN salary > 80000 THEN 1 END) AS high_earners,\n       COUNT(CASE WHEN salary <= 80000 THEN 1 END) AS others,\n       ROUND(AVG(CASE WHEN salary > 80000 THEN salary END), 2) AS avg_high\nFROM employees\nGROUP BY department_id;",
                explanation=(
                    "A single query produces multiple conditional counts and averages per department. "
                    "This is far more efficient than running separate filtered queries. The CASE inside "
                    "COUNT returns 1 for matching rows and NULL (ignored) for non-matching."
                ),
            ),
            SQLExample(
                title="COALESCE and NULLIF together",
                sql="SELECT product_name,\n       revenue,\n       cost,\n       COALESCE(\n         ROUND(revenue / NULLIF(cost, 0), 2),\n         0\n       ) AS roi\nFROM products;",
                explanation=(
                    "NULLIF(cost, 0) returns NULL when cost is 0, preventing a division-by-zero error. "
                    "COALESCE then converts the resulting NULL to 0. This is a standard defensive pattern "
                    "for safe division."
                ),
            ),
        ],
        quiz=[
            QuizQuestion(
                "What does a CASE expression return if no WHEN condition matches and there is no ELSE?",
                "NULL. Always include an ELSE clause if you don't want NULL as a fallback.",
            ),
            QuizQuestion(
                "How do you prevent division by zero in SQL?",
                "Use NULLIF in the denominator: value / NULLIF(divisor, 0). If divisor is 0, it becomes NULL, and the division returns NULL instead of an error.",
            ),
            QuizQuestion(
                "What is conditional aggregation?",
                "Using CASE inside an aggregate function (like COUNT, SUM, AVG) to count or sum only rows meeting a specific condition. It pivots data from rows to columns within a GROUP BY.",
            ),
        ],
        tips=[
            "Conditional aggregation is a top interview technique. It lets you compute multiple metrics in a single pass instead of multiple queries or subqueries.",
            "Remember that CASE conditions are evaluated in order — put the most specific conditions first to avoid them being shadowed by broader conditions above.",
            "COALESCE with more than 2 arguments is valid: COALESCE(a, b, c, d) checks each in order. Use it for fallback chains.",
        ],
    ),

    PathStep(
        title="Date Functions",
        description="Work with dates, timestamps, and time-based analysis.",
        task_ids=[25, 26, 27],
        example_sql="SELECT DATE_TRUNC('month', ordered_at) AS month,\n       COUNT(*) AS orders\nFROM orders\nGROUP BY month;",
        theory=(
            "Date and time handling is essential for analytics. Most business questions are "
            "time-based: monthly revenue, daily active users, year-over-year growth, retention "
            "by cohort. PostgreSQL provides powerful date functions that make these analyses "
            "straightforward.\n\n"

            "DATE_TRUNC truncates a timestamp to a specified precision: DATE_TRUNC('month', timestamp) "
            "sets the day, hour, minute, and second to their minimums, effectively rounding down to "
            "the first moment of that month. This is the primary function for grouping by time period. "
            "Common precisions: 'year', 'quarter', 'month', 'week', 'day', 'hour'.\n\n"

            "EXTRACT (or the equivalent date_part function) pulls a specific component from a date: "
            "EXTRACT(YEAR FROM ordered_at) returns the year as a number, EXTRACT(DOW FROM date) returns "
            "the day of week (0 = Sunday, 6 = Saturday). This is useful for filtering (WHERE EXTRACT(YEAR "
            "FROM date) = 2024) or for analysis like \"which day of week has the most orders?\"\n\n"

            "Date arithmetic in PostgreSQL uses the INTERVAL type. Adding an interval to a date: "
            "ordered_at + INTERVAL '30 days' gives a date 30 days later. Subtracting two dates gives "
            "an interval: end_date - start_date returns the time difference. You can use this for "
            "calculating ages, durations, and deadlines.\n\n"

            "CURRENT_DATE returns today's date (no time component), CURRENT_TIMESTAMP returns the "
            "current date and time, and NOW() is a PostgreSQL alias for CURRENT_TIMESTAMP. "
            "AGE(timestamp) returns the interval between the timestamp and now. AGE(end, start) returns "
            "the interval between two timestamps. These are useful for calculating \"days since signup,\" "
            "\"time since last order,\" and similar relative metrics."
        ),
        key_points=[
            "DATE_TRUNC('period', timestamp) rounds down to the start of that period — essential for time grouping.",
            "EXTRACT(field FROM timestamp) extracts a numeric component (year, month, day, hour, dow).",
            "Date arithmetic uses INTERVAL: date + INTERVAL '7 days', end_date - start_date.",
            "CURRENT_DATE (date only), NOW() (timestamp), AGE() (interval between dates).",
            "Always GROUP BY the exact same DATE_TRUNC expression used in SELECT to avoid errors.",
        ],
        syntax="-- Truncate to period\nDATE_TRUNC('month', timestamp_col)\n-- Extract component\nEXTRACT(YEAR FROM timestamp_col)\n-- Date arithmetic\ntimestamp_col + INTERVAL '30 days'\n-- Current date/time\nCURRENT_DATE, NOW(), AGE(timestamp_col)",
        examples=[
            SQLExample(
                title="Monthly order count",
                sql="SELECT DATE_TRUNC('month', ordered_at) AS month,\n       COUNT(*) AS order_count,\n       SUM(total) AS revenue\nFROM orders\nGROUP BY DATE_TRUNC('month', ordered_at)\nORDER BY month;",
                explanation=(
                    "Truncates each order's timestamp to the first of its month, then groups by that "
                    "truncated date. The result is one row per month with order count and revenue. "
                    "Note: GROUP BY uses the same expression, not the alias."
                ),
            ),
            SQLExample(
                title="Day-of-week analysis",
                sql="SELECT EXTRACT(DOW FROM ordered_at) AS day_of_week,\n       COUNT(*) AS orders,\n       ROUND(AVG(total), 2) AS avg_order_value\nFROM orders\nGROUP BY 1\nORDER BY 1;",
                explanation=(
                    "EXTRACT(DOW FROM ...) returns 0 for Sunday through 6 for Saturday. "
                    "This reveals patterns like whether weekends or weekdays drive more orders."
                ),
            ),
            SQLExample(
                title="Orders in the last 30 days",
                sql="SELECT id, customer_id, total, ordered_at\nFROM orders\nWHERE ordered_at >= CURRENT_DATE - INTERVAL '30 days'\nORDER BY ordered_at DESC;",
                explanation=(
                    "CURRENT_DATE minus an interval gives a date 30 days ago. This filters to "
                    "only recent orders. Using >= ensures inclusive boundaries."
                ),
            ),
            SQLExample(
                title="Days since last order per customer",
                sql="SELECT customer_id,\n       MAX(ordered_at) AS last_order,\n       CURRENT_DATE - MAX(ordered_at)::date AS days_since\nFROM orders\nGROUP BY customer_id\nORDER BY days_since DESC;",
                explanation=(
                    "MAX(ordered_at) finds each customer's most recent order. Subtracting from "
                    "CURRENT_DATE gives the number of days since that order — useful for identifying "
                    "inactive customers who might be churning."
                ),
            ),
        ],
        quiz=[
            QuizQuestion(
                "What does DATE_TRUNC('month', '2024-03-15 14:30:00') return?",
                "'2024-03-01 00:00:00' — it rounds down to the first moment of the month, setting day to 1 and time to midnight.",
            ),
            QuizQuestion(
                "How do you filter for records from the current year?",
                "WHERE EXTRACT(YEAR FROM date_col) = EXTRACT(YEAR FROM CURRENT_DATE) or WHERE date_col >= DATE_TRUNC('year', CURRENT_DATE).",
            ),
            QuizQuestion(
                "What is the difference between CURRENT_DATE and NOW()?",
                "CURRENT_DATE returns just the date (no time). NOW() returns the full timestamp including time. CURRENT_DATE is equivalent to NOW()::date.",
            ),
        ],
        tips=[
            "DATE_TRUNC is your best friend for time-series analysis. Most analytics questions involve grouping by day/week/month — DATE_TRUNC handles all of them.",
            "When filtering date ranges, prefer >= and < over BETWEEN for timestamps. BETWEEN is inclusive on both ends, which can include unwanted records at midnight boundaries.",
            "In interviews, always mention time zones when discussing timestamps. PostgreSQL has both TIMESTAMP (no timezone) and TIMESTAMPTZ (with timezone) types.",
        ],
    ),

    PathStep(
        title="Advanced Analytics",
        description="Funnel analysis, cohort retention, churn, and YoY growth.",
        task_ids=[34, 35, 36],
        example_sql=None,
        theory=(
            "Advanced analytics questions in SQL interviews combine everything you've learned "
            "into multi-step problems that mirror real business analysis. These patterns — funnel "
            "analysis, cohort retention, churn, and year-over-year growth — are what data analysts "
            "and data scientists do daily. Mastering them demonstrates you can go beyond basic "
            "queries to deliver actionable business insights.\n\n"

            "Funnel analysis tracks how users progress through a sequence of steps. For example: "
            "how many users visited the homepage, then viewed a product, then added to cart, then "
            "purchased? The approach: count distinct users at each step using conditional aggregation. "
            "COUNT(DISTINCT CASE WHEN event = 'view_product' THEN user_id END) gives the count at "
            "each stage. Conversion rate is each stage's count divided by the previous stage's count.\n\n"

            "Cohort retention groups users by their signup month (the cohort) and tracks what "
            "percentage are still active in subsequent months. The typical approach: (1) identify each "
            "user's first activity date (their cohort), (2) compute the number of months between "
            "cohort date and each subsequent activity, (3) count distinct users per cohort per month "
            "offset, (4) divide by the cohort's initial size for the retention percentage.\n\n"

            "Churn analysis identifies users who were active in one period but inactive in the next. "
            "A common approach: find users active last month using a CTE, find users active this month "
            "in another CTE, then LEFT JOIN and check for NULLs to find churned users. "
            "Churn rate = churned users / previous period active users * 100.\n\n"

            "Year-over-year (YoY) growth compares the same period across years. The approach: "
            "aggregate by month, use LAG with an offset of 12 to get the same month last year, "
            "then compute (current - previous_year) / previous_year * 100. This removes seasonality "
            "from the analysis and reveals true growth trends."
        ),
        key_points=[
            "Funnel analysis: COUNT(DISTINCT CASE WHEN event = 'step' THEN user_id END) at each stage.",
            "Cohort retention: group by signup month, count active users at each month offset.",
            "Churn: LEFT JOIN active users between periods; NULL on the right side = churned.",
            "YoY growth: LAG with offset 12 (months) to compare same-month last year.",
            "All advanced patterns combine CTEs, window functions, conditional aggregation, and date functions.",
        ],
        syntax="-- Funnel\nSELECT\n  COUNT(DISTINCT CASE WHEN step >= 1 THEN user_id END) AS step1,\n  COUNT(DISTINCT CASE WHEN step >= 2 THEN user_id END) AS step2\nFROM events;\n\n-- Retention\nWITH cohorts AS (\n  SELECT user_id, DATE_TRUNC('month', MIN(created_at)) AS cohort\n  FROM events GROUP BY 1\n)\nSELECT cohort, month_offset, COUNT(DISTINCT user_id)\nFROM ...\nGROUP BY 1, 2;",
        examples=[
            SQLExample(
                title="Funnel conversion rates",
                sql="WITH funnel AS (\n  SELECT\n    COUNT(DISTINCT CASE WHEN event_type = 'page_view' THEN user_id END) AS views,\n    COUNT(DISTINCT CASE WHEN event_type = 'add_to_cart' THEN user_id END) AS carts,\n    COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_id END) AS purchases\n  FROM events\n)\nSELECT views, carts, purchases,\n       ROUND(carts::numeric / views * 100, 1) AS view_to_cart_pct,\n       ROUND(purchases::numeric / carts * 100, 1) AS cart_to_purchase_pct\nFROM funnel;",
                explanation=(
                    "Counts distinct users at each funnel stage using conditional aggregation. "
                    "Then computes conversion rates between stages. This single query replaces "
                    "what might otherwise be three separate queries."
                ),
            ),
            SQLExample(
                title="Cohort retention analysis",
                sql="WITH cohorts AS (\n  SELECT user_id,\n         DATE_TRUNC('month', MIN(created_at)) AS cohort_month\n  FROM events\n  GROUP BY user_id\n),\nactivity AS (\n  SELECT c.cohort_month,\n         DATE_TRUNC('month', e.created_at) AS active_month,\n         e.user_id\n  FROM events e\n  JOIN cohorts c ON e.user_id = c.user_id\n)\nSELECT cohort_month,\n       EXTRACT(MONTH FROM AGE(active_month, cohort_month)) AS month_offset,\n       COUNT(DISTINCT user_id) AS active_users\nFROM activity\nGROUP BY 1, 2\nORDER BY 1, 2;",
                explanation=(
                    "First CTE finds each user's cohort (month of first activity). Second CTE joins "
                    "activity data with cohorts. Main query counts active users by cohort and month offset. "
                    "Month 0 is the signup month, month 1 is the next month, etc."
                ),
            ),
            SQLExample(
                title="Year-over-year growth",
                sql="WITH monthly AS (\n  SELECT DATE_TRUNC('month', ordered_at) AS month,\n         SUM(total) AS revenue\n  FROM orders\n  GROUP BY 1\n)\nSELECT month, revenue,\n       LAG(revenue, 12) OVER (ORDER BY month) AS same_month_last_year,\n       ROUND(\n         (revenue - LAG(revenue, 12) OVER (ORDER BY month))\n         / LAG(revenue, 12) OVER (ORDER BY month) * 100, 1\n       ) AS yoy_growth_pct\nFROM monthly\nORDER BY month;",
                explanation=(
                    "LAG with offset 12 looks back 12 months, giving the same month in the previous year. "
                    "The growth formula computes the percentage change. The first 12 months show NULL "
                    "because there's no prior year to compare."
                ),
            ),
        ],
        quiz=[
            QuizQuestion(
                "How do you compute conversion rate in a funnel?",
                "Divide the count of distinct users at each stage by the count at the previous stage: ROUND(stage_n::numeric / stage_n_minus_1 * 100, 1) AS conversion_pct.",
            ),
            QuizQuestion(
                "In cohort retention, what does 'month offset 0' represent?",
                "The signup month itself — the month when the user first appeared. This is always 100% retention by definition.",
            ),
            QuizQuestion(
                "How do you identify churned users between two periods?",
                "LEFT JOIN last-period active users with current-period active users on user_id. Users where the right side IS NULL have churned.",
            ),
        ],
        tips=[
            "In analytics interviews, always start by clarifying definitions: 'How do you define an active user? What counts as churn?' This shows business thinking.",
            "Structure complex analytics queries as a pipeline of CTEs — it makes your logic clear and debuggable. Name each CTE after what it contains.",
            "When computing rates and percentages, always cast to numeric/float before dividing to avoid integer division truncating to 0.",
        ],
    ),
]

# ---------------------------------------------------------------------------
# Path 7: JSONB & Array Mastery
# ---------------------------------------------------------------------------
_jsonb_steps = [
    PathStep(
        title="JSONB Basics: Accessing & Querying",
        description="Extract values from JSONB columns using ->, ->>, and @> operators.",
        task_ids=[59, 60, 61],
        example_sql="SELECT settings->>'theme' AS theme\nFROM user_profiles\nWHERE settings @> '{\"notifications\": true}';",
        theory=(
            "PostgreSQL's JSONB type stores JSON data in an efficient binary format that supports "
            "indexing and rich querying. The -> operator returns a JSON element by key (still JSONB), "
            "while ->> returns the value as text. For nested access, chain operators: "
            "col->'address'->>'city'.\n\n"
            "The containment operator @> checks if the left JSONB contains the right: "
            "settings @> '{\"theme\": \"dark\"}' returns true if settings has that key-value pair. "
            "This is index-friendly with GIN indexes.\n\n"
            "Use jsonb_each() to expand a JSONB object into key-value rows, jsonb_array_elements() "
            "to unnest a JSONB array, and jsonb_typeof() to check value types. Cast extracted text "
            "to other types as needed: (col->>'amount')::NUMERIC."
        ),
        key_points=[
            "-> returns JSONB, ->> returns TEXT — choose based on whether you need further nesting",
            "@> is the containment operator — checks if left contains right",
            "Cast ->> results to the type you need: ::INT, ::NUMERIC, ::BOOLEAN",
            "GIN indexes on JSONB columns make @> and ? operators fast",
        ],
        syntax="SELECT col->>'key' FROM t;\nSELECT * FROM t WHERE col @> '{\"k\": \"v\"}';\nSELECT * FROM t WHERE col ? 'key';",
        examples=[
            SQLExample("Extract nested JSONB", "SELECT username, settings->>'theme' AS theme FROM user_profiles WHERE settings->>'theme' IS NOT NULL;", "The ->> operator extracts the theme value as text from the settings JSONB column."),
            SQLExample("Containment query", "SELECT username FROM user_profiles WHERE settings @> '{\"notifications\": true}';", "The @> operator checks if the JSONB contains the specified key-value pair."),
        ],
        quiz=[
            QuizQuestion("What is the difference between -> and ->> in PostgreSQL?", "-> returns a JSONB value (preserving type for further chaining), while ->> returns the value as a plain TEXT string."),
            QuizQuestion("How do you check if a JSONB column contains a specific key?", "Use the ? operator: WHERE col ? 'key_name'. For key-value containment, use @>: WHERE col @> '{\"key\": \"value\"}'."),
        ],
        tips=[
            "In interviews, mention GIN indexes when discussing JSONB performance — it shows you understand production considerations.",
            "Always cast ->> results when comparing with non-text types to avoid implicit cast issues.",
        ],
    ),
    PathStep(
        title="Arrays: UNNEST, ANY, and Aggregation",
        description="Work with PostgreSQL array types using UNNEST, ANY/ALL, and array_agg.",
        task_ids=[62, 63],
        example_sql="SELECT username, UNNEST(tags) AS tag\nFROM user_profiles;",
        theory=(
            "PostgreSQL supports native array columns (TEXT[], INT[], etc.). Arrays are useful for "
            "storing multi-value attributes without a separate join table.\n\n"
            "UNNEST(array) expands an array into a set of rows — one row per element. This is essential "
            "for querying individual array elements. Combine with GROUP BY to aggregate across unnested values.\n\n"
            "The ANY(array) operator checks if a value matches any element: WHERE 'sql' = ANY(tags). "
            "ALL(array) checks if a condition holds for every element. array_agg() does the reverse — "
            "it aggregates rows back into an array.\n\n"
            "Array functions include array_length(), array_position(), array_remove(), and the || "
            "concatenation operator. Use the @> and <@ operators for array containment checks."
        ),
        key_points=[
            "UNNEST(array) expands an array into rows for per-element analysis",
            "ANY(array) checks membership: WHERE value = ANY(col)",
            "array_agg() aggregates values back into an array",
            "@> checks array containment: ARRAY[1,2] @> ARRAY[1] is TRUE",
        ],
        syntax="SELECT UNNEST(arr_col) FROM t;\nSELECT * FROM t WHERE val = ANY(arr_col);\nSELECT array_agg(col) FROM t GROUP BY grp;",
        examples=[
            SQLExample("Unnest and count tags", "SELECT tag, COUNT(*) FROM (SELECT UNNEST(tags) AS tag FROM user_profiles) t GROUP BY tag ORDER BY COUNT(*) DESC;", "UNNEST expands each user's tags array into rows, then GROUP BY counts occurrences of each tag."),
        ],
        quiz=[
            QuizQuestion("What does UNNEST do to an array?", "It expands the array into a set of rows, with one row per element. This turns an array column into a table-like set for joining and aggregation."),
        ],
        tips=[
            "Interviewers love the UNNEST + GROUP BY combo for tag analysis — practice it until it's automatic.",
        ],
    ),
]

# ---------------------------------------------------------------------------
# Path 8: Recursive CTEs & Hierarchies
# ---------------------------------------------------------------------------
_recursive_steps = [
    PathStep(
        title="Recursive CTE Fundamentals",
        description="Understand the structure and execution of recursive CTEs.",
        task_ids=[55, 56],
        example_sql="WITH RECURSIVE tree AS (\n  SELECT id, name, parent_id, 0 AS level\n  FROM categories WHERE parent_id IS NULL\n  UNION ALL\n  SELECT c.id, c.name, c.parent_id, t.level + 1\n  FROM categories c JOIN tree t ON c.parent_id = t.id\n)\nSELECT * FROM tree ORDER BY level, name;",
        theory=(
            "A recursive CTE has two parts joined by UNION ALL: the base case (anchor) and the "
            "recursive step. The anchor runs first and returns the starting rows. Then the recursive "
            "step runs repeatedly, each time using the rows produced by the previous iteration, until "
            "no new rows are generated.\n\n"
            "The syntax is: WITH RECURSIVE cte AS (anchor UNION ALL recursive_step) SELECT ... "
            "The RECURSIVE keyword is required. The recursive step must reference the CTE name.\n\n"
            "For hierarchies like org charts or category trees, the anchor selects root nodes "
            "(WHERE parent_id IS NULL) and the recursive step joins children to parents. Add a level "
            "counter to track depth. Add a path array to build materialized paths for display."
        ),
        key_points=[
            "Recursive CTEs have two parts: anchor (base case) + recursive step joined by UNION ALL",
            "The RECURSIVE keyword is mandatory in PostgreSQL",
            "Execution stops when the recursive step returns zero rows",
            "Always include a termination condition to prevent infinite loops",
        ],
        syntax="WITH RECURSIVE cte_name AS (\n  -- anchor\n  SELECT ... WHERE parent_id IS NULL\n  UNION ALL\n  -- recursive step\n  SELECT ... FROM table JOIN cte_name ON ...\n)\nSELECT * FROM cte_name;",
        examples=[
            SQLExample("Category tree traversal", "WITH RECURSIVE tree AS (\n  SELECT id, name, parent_id, 1 AS depth\n  FROM categories WHERE parent_id IS NULL\n  UNION ALL\n  SELECT c.id, c.name, c.parent_id, t.depth + 1\n  FROM categories c JOIN tree t ON c.parent_id = t.id\n)\nSELECT * FROM tree ORDER BY depth, name;", "The anchor selects root categories. The recursive step joins children to already-found parents, incrementing depth. Terminates when no more children exist."),
        ],
        quiz=[
            QuizQuestion("What are the two parts of a recursive CTE?", "The anchor (base case) that provides starting rows, and the recursive step that references the CTE itself and adds new rows in each iteration until no more rows are produced."),
            QuizQuestion("When does a recursive CTE stop executing?", "When the recursive step produces no new rows (empty result set). Without proper termination, it could loop infinitely, so PostgreSQL has a max recursion depth setting."),
        ],
        tips=[
            "Recursive CTEs appear in nearly every senior-level SQL interview. Practice hierarchical traversal until the pattern is second nature.",
            "Always mention termination conditions when discussing recursive CTEs — it shows production awareness.",
        ],
    ),
    PathStep(
        title="Advanced Recursion: Paths and Aggregation",
        description="Build materialized paths, compute hierarchical aggregates, and traverse graphs.",
        task_ids=[57, 58],
        example_sql="WITH RECURSIVE tree AS (\n  SELECT id, name, parent_id, name::TEXT AS path\n  FROM categories WHERE parent_id IS NULL\n  UNION ALL\n  SELECT c.id, c.name, c.parent_id, t.path || ' > ' || c.name\n  FROM categories c JOIN tree t ON c.parent_id = t.id\n)\nSELECT * FROM tree ORDER BY path;",
        theory=(
            "Beyond simple traversal, recursive CTEs can build materialized paths (breadcrumb strings), "
            "compute cumulative values up or down a hierarchy, and even detect cycles.\n\n"
            "To build a path, concatenate names at each level: t.path || ' > ' || c.name. This produces "
            "strings like 'Electronics > Computers > Laptops' that show the full hierarchy.\n\n"
            "For hierarchical aggregates, traverse the tree first, then join with aggregate queries to "
            "roll up values from children to parents. To detect cycles, maintain an array of visited IDs "
            "and check membership: WHERE NOT c.id = ANY(t.visited)."
        ),
        key_points=[
            "Concatenate at each recursion level to build materialized paths",
            "Use arrays to track visited nodes and detect cycles",
            "Combine recursive CTEs with window functions for hierarchical ranking",
            "PostgreSQL's CYCLE clause (v14+) provides built-in cycle detection",
        ],
        syntax=None,
        examples=[
            SQLExample("Full path with depth", "WITH RECURSIVE tree AS (\n  SELECT id, name, parent_id, ARRAY[id] AS path_ids, name::TEXT AS full_path\n  FROM categories WHERE parent_id IS NULL\n  UNION ALL\n  SELECT c.id, c.name, c.parent_id, t.path_ids || c.id, t.full_path || ' > ' || c.name\n  FROM categories c JOIN tree t ON c.parent_id = t.id\n  WHERE NOT c.id = ANY(t.path_ids)\n)\nSELECT * FROM tree ORDER BY full_path;", "Tracks visited IDs in an array to prevent cycles, and builds a readable breadcrumb path."),
        ],
        quiz=[
            QuizQuestion("How can you detect cycles in a recursive CTE?", "Track visited node IDs in an array column, and add WHERE NOT node.id = ANY(cte.visited_ids) to the recursive step. PostgreSQL 14+ also has a built-in CYCLE clause."),
        ],
        tips=[
            "When asked about recursive queries, start by identifying the base case and termination condition — interviewers value structured thinking.",
        ],
    ),
]

# ---------------------------------------------------------------------------
# Path 9: Time-Series & Gap Analysis
# ---------------------------------------------------------------------------
_timeseries_steps = [
    PathStep(
        title="Gap & Island Detection",
        description="Identify consecutive sequences and gaps in time-series data.",
        task_ids=[67, 68, 69],
        example_sql="WITH numbered AS (\n  SELECT *, recorded_at - ROW_NUMBER() OVER (ORDER BY recorded_at) * INTERVAL '1 day' AS grp\n  FROM sensor_readings\n)\nSELECT MIN(recorded_at) AS start_date, MAX(recorded_at) AS end_date, COUNT(*) AS length\nFROM numbered GROUP BY grp ORDER BY start_date;",
        theory=(
            "The gap-and-island problem identifies consecutive groups (islands) and missing values "
            "(gaps) in sequential data. The classic technique uses ROW_NUMBER: subtract the row number "
            "from the value (or date) — consecutive values produce the same difference, creating a "
            "grouping key.\n\n"
            "For date sequences: date - ROW_NUMBER() * INTERVAL '1 day' gives the same base date for "
            "consecutive dates. Group by this computed value to find each island.\n\n"
            "For numeric sequences: value - ROW_NUMBER() OVER (ORDER BY value) gives the same offset "
            "for consecutive integers. Gaps in the sequence break this pattern."
        ),
        key_points=[
            "The trick: subtract ROW_NUMBER from the value — consecutive values share the same difference",
            "For dates: date - ROW_NUMBER() * INTERVAL creates grouping keys for islands",
            "Gaps appear where the difference changes",
            "PARTITION BY allows detecting islands within groups (per sensor, per user, etc.)",
        ],
        syntax="WITH grps AS (\n  SELECT *, val - ROW_NUMBER() OVER (ORDER BY val) AS island_id\n  FROM table\n)\nSELECT MIN(val), MAX(val), COUNT(*)\nFROM grps GROUP BY island_id;",
        examples=[
            SQLExample("Find active streaks", "SELECT sensor_id, MIN(recorded_at) AS streak_start, MAX(recorded_at) AS streak_end, COUNT(*) AS readings\nFROM (\n  SELECT *, recorded_at::DATE - (ROW_NUMBER() OVER (PARTITION BY sensor_id ORDER BY recorded_at::DATE))::INT * INTERVAL '1 day' AS grp\n  FROM sensor_readings WHERE NOT is_anomaly\n) t GROUP BY sensor_id, grp ORDER BY sensor_id, streak_start;", "Groups consecutive non-anomalous readings per sensor into streaks using the date minus row_number technique."),
        ],
        quiz=[
            QuizQuestion("What is the core technique for detecting islands in sequential data?", "Subtract ROW_NUMBER() from the sequential value. Consecutive values produce the same difference, which becomes a grouping key. Non-consecutive values produce different differences, breaking the group."),
        ],
        tips=[
            "Gap-and-island is a top interview pattern at Google and Amazon — practice it with both date and integer sequences.",
        ],
    ),
    PathStep(
        title="Sessionization & Time Windows",
        description="Group events into sessions based on time gaps and analyze session behavior.",
        task_ids=[73, 74, 75, 76],
        example_sql="SELECT session_id, COUNT(*) AS events,\n  MIN(created_at) AS start, MAX(created_at) AS end,\n  EXTRACT(EPOCH FROM MAX(created_at) - MIN(created_at)) AS duration_sec\nFROM event_log GROUP BY session_id;",
        theory=(
            "Sessionization groups a stream of events into logical sessions based on time gaps. If two "
            "consecutive events are more than N minutes apart, a new session starts. This is fundamental "
            "for web analytics, product metrics, and behavioral analysis.\n\n"
            "The technique uses LAG() to get the previous event timestamp, then a CASE expression to "
            "flag session boundaries where the gap exceeds the threshold. A cumulative SUM of these "
            "flags creates session IDs.\n\n"
            "Once sessions are defined, aggregate to compute metrics: session duration, event count, "
            "conversion within session, bounce rate, etc."
        ),
        key_points=[
            "Use LAG() to find time between consecutive events",
            "Flag new sessions where the gap exceeds a threshold",
            "SUM() the flags with a window function to create session IDs",
            "EXTRACT(EPOCH FROM interval) converts time differences to seconds",
        ],
        syntax=None,
        examples=[
            SQLExample("Basic session metrics", "SELECT session_id, user_id, COUNT(*) AS event_count, MIN(created_at) AS session_start, MAX(created_at) AS session_end, EXTRACT(EPOCH FROM MAX(created_at) - MIN(created_at)) AS duration_seconds FROM event_log GROUP BY session_id, user_id ORDER BY session_start;", "Groups pre-assigned sessions and computes core metrics: event count, start/end times, and duration."),
        ],
        quiz=[
            QuizQuestion("What SQL technique is used to detect session boundaries?", "Use LAG() to get the previous event's timestamp, compute the time gap, and flag rows where the gap exceeds the session timeout threshold. Cumulative SUM of these flags creates session IDs."),
        ],
        tips=[
            "Sessionization questions appear at Uber, Netflix, and Spotify interviews. Know both the pre-assigned session_id approach and the gap-based approach.",
        ],
    ),
]

# ---------------------------------------------------------------------------
# Path 10: Financial SQL Patterns
# ---------------------------------------------------------------------------
_financial_steps = [
    PathStep(
        title="Running Balances & Transaction Analysis",
        description="Compute running totals, balances, and financial aggregates from transaction data.",
        task_ids=[70, 71, 72],
        example_sql="SELECT txn_date, amount,\n  SUM(amount) OVER (ORDER BY txn_date) AS running_balance\nFROM transactions WHERE account_id = 1;",
        theory=(
            "Financial SQL requires precise calculations with running totals, period comparisons, and "
            "categorized aggregations. Running balance is computed with SUM() OVER (ORDER BY date) — "
            "this creates a cumulative sum that represents the account balance after each transaction.\n\n"
            "Period-over-period comparison uses LAG() to access previous period values: "
            "current_month - LAG(current_month) OVER (ORDER BY month). Percentage change is "
            "(current - previous) / previous * 100.\n\n"
            "The COUNT(*) FILTER (WHERE condition) syntax is PostgreSQL-specific and extremely useful "
            "for computing conditional aggregates without CASE expressions. For example: "
            "COUNT(*) FILTER (WHERE txn_type = 'credit') counts only credit transactions."
        ),
        key_points=[
            "SUM() OVER (ORDER BY date) computes running balances",
            "LAG() enables period-over-period comparisons",
            "COUNT/SUM FILTER (WHERE ...) is cleaner than CASE for conditional aggregates",
            "NUMERIC type prevents floating-point errors in financial calculations",
        ],
        syntax="SELECT SUM(amount) OVER (ORDER BY txn_date) AS running_bal FROM transactions;\nSELECT COUNT(*) FILTER (WHERE type = 'credit') FROM transactions;",
        examples=[
            SQLExample("Running balance per account", "SELECT account_id, txn_date, amount, SUM(amount) OVER (PARTITION BY account_id ORDER BY txn_date, id) AS running_balance FROM transactions ORDER BY account_id, txn_date;", "Partitions by account to keep balances separate, orders by date and id for deterministic results."),
            SQLExample("Monthly summary with FILTER", "SELECT DATE_TRUNC('month', txn_date) AS month, COUNT(*) FILTER (WHERE txn_type = 'credit') AS credits, COUNT(*) FILTER (WHERE txn_type = 'debit') AS debits, SUM(amount) AS net_amount FROM transactions GROUP BY 1 ORDER BY 1;", "FILTER clauses compute separate aggregates for credits and debits without CASE expressions."),
        ],
        quiz=[
            QuizQuestion("Why use NUMERIC instead of FLOAT for financial data?", "FLOAT has binary floating-point precision issues (e.g., 0.1 + 0.2 != 0.3). NUMERIC stores exact decimal values, which is essential for financial calculations where rounding errors are unacceptable."),
            QuizQuestion("What does COUNT(*) FILTER (WHERE ...) do?", "It counts only the rows that match the FILTER condition. It's a PostgreSQL-specific shorthand that's cleaner than COUNT(CASE WHEN condition THEN 1 END) and can be used with any aggregate function."),
        ],
        tips=[
            "Financial SQL questions test precision and edge case handling. Always mention NUMERIC over FLOAT and discuss NULL handling in aggregates.",
            "Running balance with SUM OVER is a very common interview pattern — practice partition ordering.",
        ],
    ),
]

# ---------------------------------------------------------------------------
# Assemble all paths
# ---------------------------------------------------------------------------

LEARNING_PATHS: list[LearningPath] = [
    LearningPath(
        id=1,
        title="SQL Fundamentals",
        description="Master the basics: SELECT, WHERE, ORDER BY, LIMIT.",
        icon="BookOpen",
        steps=_fundamentals_steps,
    ),
    LearningPath(
        id=2,
        title="Joins Mastery",
        description="Connect tables with INNER, LEFT, RIGHT, and FULL joins.",
        icon="Link",
        steps=_joins_steps,
    ),
    LearningPath(
        id=3,
        title="Aggregation & Grouping",
        description="Summarize data with GROUP BY, COUNT, SUM, AVG.",
        icon="BarChart",
        steps=_aggregation_steps,
    ),
    LearningPath(
        id=4,
        title="Subqueries & CTEs",
        description="Write nested queries and common table expressions.",
        icon="Layers",
        steps=_subqueries_steps,
    ),
    LearningPath(
        id=5,
        title="Window Functions",
        description="Rank, running totals, and lag/lead analysis.",
        icon="TrendingUp",
        steps=_window_steps,
    ),
    LearningPath(
        id=6,
        title="Interview Ready",
        description="Advanced patterns for technical interviews.",
        icon="Award",
        steps=_interview_steps,
    ),
    LearningPath(
        id=7,
        title="JSONB & Array Mastery",
        description="Query JSON documents and array columns in PostgreSQL.",
        icon="Braces",
        steps=_jsonb_steps,
    ),
    LearningPath(
        id=8,
        title="Recursive CTEs & Hierarchies",
        description="Traverse trees, graphs, and hierarchical data with recursive queries.",
        icon="GitBranch",
        steps=_recursive_steps,
    ),
    LearningPath(
        id=9,
        title="Time-Series & Gap Analysis",
        description="Detect gaps, islands, and sessions in sequential data.",
        icon="Clock",
        steps=_timeseries_steps,
    ),
    LearningPath(
        id=10,
        title="Financial SQL Patterns",
        description="Running balances, period comparisons, and conditional aggregates.",
        icon="DollarSign",
        steps=_financial_steps,
    ),
]
