import csv

def parse_query(query):
    tokens = query.replace(",", " ,").split()

    # Convert only keywords to uppercase
    tokens_upper = [t.upper() for t in tokens]

    # Find positions
    select_index = tokens_upper.index("SELECT")
    from_index = tokens_upper.index("FROM")

    # Extract columns
    columns = tokens[select_index + 1:from_index]
    columns = [col for col in columns if col != ","]

    # Normalize column names
    columns = [col.lower() for col in columns]

    # Extract table name
    table = tokens[from_index + 1].lower()

    # Extract condition
    condition = None
    if "WHERE" in tokens_upper:
        where_index = tokens_upper.index("WHERE")

        col = tokens[where_index + 1].lower()
        op = tokens[where_index + 2]
        val = tokens[where_index + 3]

        if val.isdigit():
            val = int(val)

        condition = (col, op, val)

    return columns, table, condition


def check_condition(row, condition):
    if not condition:
        return True

    col, op, val = condition

    if col not in row:
        print(f"❌ Column '{col}' not found")
        return False

    row_val = row[col]


    try:
        row_val = int(row_val)
    except:
        try:
            row_val = float(row_val)
        except:
            pass

    try:
        val = int(val)
    except:
        try:
            val = float(val)
        except:
            pass

    if op == ">":
        return row_val > val
    elif op == "<":
        return row_val < val
    elif op == ">=":
        return row_val >= val
    elif op == "<=":
        return row_val <= val
    elif op == "==" or op == "=":
        return row_val == val

    print("❌ Invalid operator")
    return False


def execute_query(columns, table, condition):
    filename = table + ".csv"

    try:
        with open(filename, newline='') as file:
            reader = csv.DictReader(file)

            # Normalize CSV headers to lowercase
            fieldnames = [field.lower() for field in reader.fieldnames]

            for row in reader:
                # Convert row keys to lowercase
                row = {k.lower(): v for k, v in row.items()}

                if check_condition(row, condition):
                    if columns == ["*"]:
                        print(row)
                    else:
                        try:
                            print({col: row[col] for col in columns})
                        except KeyError as e:
                            print(f"❌ Column not found: {e}")

    except FileNotFoundError:
        print(f"❌ Table '{table}' not found (missing {filename})")


# MAIN
query = input("Enter SQL Query: ")

columns, table, condition = parse_query(query)
execute_query(columns, table, condition)