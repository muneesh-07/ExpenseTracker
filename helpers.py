from typing import List, Tuple

def format_table(expenses: List[Tuple]) -> str:
    if not expenses:
        return "No expenses found"
    
    headers = ["ID", "Category", "Amount", "Date"]
    rows = []
    
    for exp in expenses:
        try:
            amount = f"₹{float(exp[2]):.2f}"
        except (ValueError, TypeError):
            amount = str(exp[2])
        
        rows.append((
            str(exp[0]),      # ID
            exp[1],           # Category
            amount,
            exp[3]            # Date
        ))
    
    # Calculate column widths
    col_widths = [
        max(len(str(row[i])) for row in [headers] + rows
    ) for i in range(len(headers))]
    
    # Build table
    table = "\n" + " | ".join(
        f"{header:<{col_widths[i]}}" for i, header in enumerate(headers)
    ) + "\n"
    table += "-+-".join(["─" * width for width in col_widths]) + "\n"
    
    for row in rows:
        table += " | ".join(
            f"{row[i]:<{col_widths[i]}}" if i != 2 else f"{row[i]:>{col_widths[i]}}"
            for i in range(len(row))
        ) + "\n"
    
    return table