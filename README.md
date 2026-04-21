# Toy_SQL_Compiler
A lightweight SQL compiler built in Python that parses and executes queries on CSV files, implementing core database operations and compiler concepts.

---

## What it does

You type in a SQL-style query, and the engine reads your CSV file, processes the query, and prints the result in your terminal. No database setup, no dependencies — just Python and a CSV file.

It supports:

- `SELECT` with specific columns or `*`
- `WHERE` conditions for filtering rows
- `ORDER BY` (ascending and descending)
- `LIMIT` to cap results
- `GROUP BY` with `COUNT`
- `INSERT`, `UPDATE`, and `DELETE`
- Duplicate ID prevention on insert

---

## Project structure

```
Toy-SQL-Compiler/
│
├── toy_compiler.py     # Main engine — tokenizer, parser, and executor
├── students.csv        # Sample dataset used for testing
├── README.md
└── screenshots/        # Output screenshots
```

---

## How to run

No installation needed. Just clone the repo and run:

```bash
git clone https://github.com/your-username/Toy-SQL-Compiler.git
cd Toy-SQL-Compiler
python toy_compiler.py
```

Then type your query when prompted.

---

## Try these queries

```sql
-- Get all students
SELECT * FROM students

-- Sort by marks, highest first
SELECT name, marks FROM students ORDER BY marks DESC

-- Count students by age group
SELECT age, count FROM students GROUP BY age

-- Add a new student (id, name, age, marks)
INSERT INTO students VALUES (9, John, 23, 88)

-- Remove a student
DELETE FROM students WHERE id = 2

-- Update a student's marks
UPDATE students SET marks = 95 WHERE name = Skanda
```

---

## How it works internally

1. **Tokenizer** — splits the raw query string into individual tokens (keywords, column names, values, operators)
2. **Parser** — reads the token list and figures out what type of query it is and what it's asking for
3. **Executor** — carries out the operation on the CSV data (filter rows, sort, group, insert, etc.)
4. **Storage** — all data lives in `students.csv` and gets read/written on every query

`GROUP BY` is handled using a Python dictionary that aggregates counts as it loops through rows.

---

## Screenshots

**SELECT query**

*(add screenshot here)*

**INSERT query**

*(add screenshot here)*

**GROUP BY**

*(add screenshot here)*

---

## Known limitations

- No support for `JOIN` across multiple tables
- `WHERE` only handles a single condition (no `AND` / `OR` yet)
- Designed to work with structured, well-formatted CSV files
- Values in queries don't use quotes (e.g. `WHERE name = John`, not `WHERE name = 'John'`)

---

## What we'd like to add next

- `JOIN` support for querying across two CSV files
- `AND` / `OR` in `WHERE` conditions
- Better error messages for invalid queries
- A simple GUI or table-formatted terminal output

---

## Built with

- Python (standard library only)
- CSV file handling
- Compiler concepts: tokenization and parsing

---

## Team

Built as part of a college project. Feel free to fork, use, or build on top of it.
