import re

def matlab_matrix_to_python(matlab_str: str) -> str:
    """
    Convert MATLAB-style matrix [a,b;c,d] into Python-style nested list [[a, b], [c, d]].
    Whitespace is stripped from all elements.
    """
    matlab_str = matlab_str.strip().rstrip(';')

    # Remove outer brackets if present
    if matlab_str.startswith('[') and matlab_str.endswith(']'):
        matlab_str = matlab_str[1:-1].strip()

    # Split into rows and clean each element
    rows = [
        f"[{', '.join(e.strip() for e in row.strip().split(','))}]"
        for row in matlab_str.split(';') if row.strip()
    ]

    return f"[{', '.join(rows)}]"