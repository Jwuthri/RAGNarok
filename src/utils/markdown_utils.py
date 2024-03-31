def align_markdown_table(md_table: str) -> str:
    """
    Takes a markdown table as input and returns a perfectly aligned markdown table.

    :param md_table: Multiline string representing the markdown table.
    :return: A string of the perfectly aligned markdown table.
    """
    # Split the table into lines
    lines = md_table.strip().split("\n")

    # Extract the headers and rows
    headers = lines[0].split("|")[1:-1]  # Ignore empty strings due to leading and trailing |
    rows = [line.split("|")[1:-1] for line in lines[2:]]  # The actual data rows

    # Determine the maximum width for each column
    col_widths = [
        max(len(header.strip()), *(len(cell.strip()) for cell in col)) for header, col in zip(headers, zip(*rows))
    ]

    # Rebuild the table with aligned columns
    aligned_table = []
    aligned_table.append(
        "| " + " | ".join(header.strip().ljust(width) for header, width in zip(headers, col_widths)) + " |"
    )
    aligned_table.append("|-" + "-|-".join("-" * width for width in col_widths) + "-|")

    for row in rows:
        aligned_table.append(
            "| " + " | ".join(cell.strip().ljust(width) for cell, width in zip(row, col_widths)) + " |"
        )

    return "\n".join(aligned_table)
