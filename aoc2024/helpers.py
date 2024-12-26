import os
import sys
import time

directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
cw_direction = {direction: directions[(i+1)%4] for i, direction in enumerate(directions)}
ccw_direction = {direction: directions[(i-1)%4] for i, direction in enumerate(directions)}
cell_to_direction = {ord("^"): (-1, 0), ord(">"): (0, 1), ord("v"): (1, 0), ord("<"): (0, -1)}
direction_to_cell = {v: k for k, v in cell_to_direction.items()}

def print_2d_debug_info(header, array, center, seconds):
    sys.stdout.write("\033[2J\033[H")
    print(header)
    print_2d_chr_array(array, center, header.count("\n") + 1)
    time.sleep(seconds)

def print_2d_chr_array(array, center, top_margin):
    terminal_size = os.get_terminal_size()
    height = terminal_size.lines - top_margin
    width = terminal_size.columns
    row_start = max(0, center[0] - height//2) if height < array.shape[0] else 0
    row_end = min(array.shape[0], row_start + height)
    column_start = max(0, center[1] - width//2) if width < array.shape[1] else 0
    column_end = min(array.shape[1], column_start + width)
    row_slice, column_slice = slice(row_start, row_end), slice(column_start, column_end)
    sys.stdout.write("\n".join("".join(map(chr, row[column_slice])) for row in array[row_slice]))
