"""
Calculate the building template for a triangular puzzle as a dictionary of lists of 2-tuples.
Please refer to the package's README for an in depth explanation.
"""
from typing import Dict, List, NamedTuple


class Neighbor(NamedTuple):
    neighbor: int
    edge: int


# index constants for the edges
BOTTOM = 0
LEFT = 1
RIGHT = 2


def calculate_template_for_a_puzzle_of(num_tiles: int = 9) -> Dict[int, List[Neighbor]]:
    """
    Calculate tiling template from the number of tiles in the puzzle.
    :param num_tiles: the number of tiles in the puzzle, defaults to 9
    :return: the tiling template dictionary
    """
    puzzle_height = int(num_tiles ** 0.5)
    if num_tiles < 1 or num_tiles > puzzle_height ** 2:
        raise ValueError("the number of tiles must be the square of a positve integer")

    template: Dict[int, List[Neighbor]] = {}
    if num_tiles == 1:
        return template

    current_row_size = puzzle_height * 2 - 1
    current_row = 0
    current_tile = 1
    tile_in_row = 1

    while current_row_size > 0:

        if tile_in_row % 2 == 1:
            template[current_tile] = [Neighbor(neighbor=current_tile - 1, edge=RIGHT)]
        elif current_row == 0:
            template[current_tile] = [Neighbor(neighbor=current_tile - 1, edge=LEFT)]
        elif tile_in_row == 0:
            template[current_tile] = [Neighbor(neighbor=current_tile - current_row_size - 1, edge=BOTTOM)]
        else:
            template[current_tile] = [
                Neighbor(neighbor=current_tile - 1, edge=LEFT),
                Neighbor(neighbor=current_tile - current_row_size - 1, edge=BOTTOM)
            ]

        current_tile += 1
        current_row, current_row_size, tile_in_row = adjust_cursors(current_row, current_row_size, tile_in_row)

    return template


def adjust_cursors(current_row, current_row_size, tile_in_row):
    tile_in_row += 1
    if tile_in_row >= current_row_size:
        tile_in_row = 0
        current_row += 1
        current_row_size -= 2
    return current_row, current_row_size, tile_in_row