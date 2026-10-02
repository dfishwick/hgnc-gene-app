def cell_to_list(cell_contents):
    """Convert cell contents into a list of strings.

    Parameters
    ----------
    cell_contents : str
        The text in the cell, "|" separated for multiple values.
        Empty cells are represented as "".

    Returns
    -------
    list of str
        A list of strings, or an empty list if the cell is empty.
    """
    if cell_contents == "":
        return []
    return cell_contents.split("|")
