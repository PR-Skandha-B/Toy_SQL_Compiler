import csv
import os

# -------------- str,int -----------------
def safe_number(val):
    try:
        return int(str(val).strip())
    except:
        try:
            return float(str(val).strip())
        except:
            return 0

# ---------------- TOKENIZER ----------------
def tokenize(query):
    for op in [">=", "<=", ">", "<", "="]:
        query = query.replace(op, f" {op} ")
    return query.replace(",", " ,").replace("(", " ( ").replace(")", " ) ").split()


# ---------------- PARSER ----------------
def parse_query(query):
    tokens = tokenize(query)
    tokens_upper = [t.upper() for t in tokens]

    query_type = tokens_upper[0]

    if query_type == "SELECT":
        select_index = tokens_upper.index("SELECT")
        from_index = tokens_upper.index("FROM")

        
       
        columns = tokens[select_index + 1:from_index]

        # remove commas and clean properly
        clean_columns = []
        for col in columns:
         if col != ",":
            clean_columns.append(col.replace(",", "").strip().lower())

        columns = clean_columns
        

        table = tokens[from_index + 1].lower()

        condition = None
        order_by = None
        limit = None

        if "WHERE" in tokens_upper:
            i = tokens_upper.index("WHERE")
            condition = (tokens[i+1].lower(), tokens[i+2], tokens[i+3])

        if "ORDER" in tokens_upper:
            i = tokens_upper.index("BY")
            order_by = tokens[i+1].lower()
            order_type = "ASC"

            if len(tokens_upper) > i+2 and tokens_upper[i+2] in ["ASC", "DESC"]:
                order_type = tokens_upper[i+2]

        if "LIMIT" in tokens_upper:
            i = tokens_upper.index("LIMIT")
            limit = int(tokens[i+1])

        return ("SELECT", columns, table, condition, order_by, order_type, limit)

    elif query_type == "INSERT":
        table = tokens[2].lower()

        values_part = query.split("VALUES")[1].strip()
        values_part = values_part.strip("()")

        values = [v.strip() for v in values_part.split(",")]

        return ("INSERT", table, values)

    elif query_type == "DELETE":
        table = tokens[2].lower()
        condition = None
        if "WHERE" in tokens_upper:
            i = tokens_upper.index("WHERE")
            condition = (tokens[i+1].lower(), tokens[i+2], tokens[i+3])
        return ("DELETE", table, condition)

    elif query_type == "UPDATE":
        table = tokens[1].lower()
        set_i = tokens_upper.index("SET")
        where_i = tokens_upper.index("WHERE")

        set_col = tokens[set_i+1].lower()
        set_val = tokens[set_i+3]

        condition = (tokens[where_i+1].lower(), tokens[where_i+2], tokens[where_i+3])

        return ("UPDATE", table, set_col, set_val, condition)


# ---------------- CONDITION ----------------
def check_condition(row, condition):
    if not condition:
        return True

    col, op, val = condition
    row_val = row[col]

    try:
        row_val = int(row_val)
        val = int(val)
    except:
        pass

    if op == ">": return row_val > val
    if op == "<": return row_val < val
    if op == ">=": return row_val >= val
    if op == "<=": return row_val <= val
    if op in ["=", "=="]: return row_val == val

    return False


# ---------------- UTIL ----------------
def get_next_id(filename):
    max_id = 0
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            max_id = max(max_id, int(row["id"]))
    return max_id + 1


# ---------------- SELECT ----------------
def execute_select(columns, table, condition, order_by, order_type, limit):
    filename = table + ".csv"

    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        rows = []

        for row in reader:
            row = {k.lower(): v.strip().replace(",", "") for k, v in row.items()}
            if check_condition(row, condition):
                rows.append(row)

        # ORDER BY
        if order_by:
         reverse = True if order_type == "DESC" else False
         rows.sort(key=lambda x: safe_number(x.get(order_by, 0)), reverse=reverse)

        # LIMIT
        if limit:
            rows = rows[:limit]

        # PRINT
        for row in rows:
            if columns == ["*"]:
                print(row)
            else:
                print({c: row[c] for c in columns})


# ---------------- INSERT ----------------
def execute_insert(table, values):
    filename = table + ".csv"

    # Auto ID suggestion
    next_id = get_next_id(filename)
    print(f"👉 Suggested ID: {next_id}")

    # Prevent duplicate
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["id"] == values[0]:
                print("❌ Duplicate ID!")
                return

     # Clean values (remove commas/spaces)
    clean_values = [v.replace(",", "").strip() for v in values]

    with open(filename, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(clean_values)

    print("✅ Inserted successfully")


# ---------------- DELETE ----------------
def execute_delete(table, condition):
    filename = table + ".csv"
    rows = []

    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames

        for row in reader:
            row = {k.lower(): v for k, v in row.items()}
            if not check_condition(row, condition):
                rows.append(row)

    with open(filename, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print("✅ Deleted")


# ---------------- UPDATE ----------------
def execute_update(table, set_col, set_val, condition):
    filename = table + ".csv"
    rows = []

    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames

        for row in reader:
            row = {k.lower(): v for k, v in row.items()}
            if check_condition(row, condition):
                row[set_col] = set_val
            rows.append(row)

    with open(filename, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print("✅ Updated")


# ---------------- MAIN ----------------
query = input("Enter SQL Query: ")

parsed = parse_query(query)

if parsed:
    if parsed[0] == "SELECT":
        _, cols, table, cond, order, order_type, limit = parsed
        execute_select(cols, table, cond, order, order_type, limit)

    elif parsed[0] == "INSERT":
        _, table, values = parsed
        execute_insert(table, values)

    elif parsed[0] == "DELETE":
        _, table, cond = parsed
        execute_delete(table, cond)

    elif parsed[0] == "UPDATE":
        _, table, sc, sv, cond = parsed
        execute_update(table, sc, sv, cond)