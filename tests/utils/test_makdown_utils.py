from ragnarok.utils.markdown_utils import align_markdown_table


def test_align_markdown_table():
    md_table = """
    | Model Name | Description | Dimensions | Language | Use Cases |
    |------------|-------------|------------|----------|-----------|
    | model_1    | Description of model 1. | Dimension size | Language(s) supported | Recommended use cases |
    | model_2    | Description of model 2. | Dimension size | Language(s) supported | Recommended use cases |
    """
    expected_aligned_md_table = """
    | Model Name | Description             | Dimensions     | Language              | Use Cases             |
    |------------|-------------------------|----------------|-----------------------|-----------------------|
    | model_1    | Description of model 1. | Dimension size | Language(s) supported | Recommended use cases |
    | model_2    | Description of model 2. | Dimension size | Language(s) supported | Recommended use cases |
    """
    # Call the function under test
    aligned_md_table = align_markdown_table(md_table)

    # Normalize whitespace for comparison
    aligned_md_table_lines = aligned_md_table.strip().split("\n")
    expected_aligned_md_table_lines = expected_aligned_md_table.strip().split("\n")
    assert len(aligned_md_table_lines) == len(expected_aligned_md_table_lines), "The number of lines should match"

    for actual_line, expected_line in zip(aligned_md_table_lines, expected_aligned_md_table_lines):
        assert (
            actual_line.strip() == expected_line.strip()
        ), f"Line mismatch: expected '{expected_line.strip()}' but got '{actual_line.strip()}'"
