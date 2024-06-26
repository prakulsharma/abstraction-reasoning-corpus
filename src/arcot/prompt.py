# References:
# https://github.com/tanchongmin/ARC-Challenge
# https://arxiv.org/abs/2310.05146

helper_functions = """
- get_objects(grid,diag=False,by_row=False,by_col=False,by_color=False,multicolor=False,more_info = True): 
Takes in grid, returns list of object dictionary: top-left coordinate of object ('tl'), 2D grid ('grid')
by_row views splits objects by grid rows, by_col splits objects by grid columns, by_color groups each color as one object, multicolor means object can be more than one color
Empty cells within objects are represented as '$'
If more_info is True, also returns size of grid ('size'), cells in object ('cell_count'), shape of object ('shape')
- get_pixel_coords(grid): Returns a dictionary, with the keys the pixel values, values the list of coords, in sorted order from most number of pixels to least
- empty_grid(row, col): returns an empty grid of height row and width col
- crop_grid(grid, tl, br): returns cropped section from top left to bottom right of the grid
- tight_fit(grid): returns grid with all blank rows and columns removed
- combine_object(obj_1, obj_2): returns combined object from obj_1 and obj_2. if overlap, obj_2 overwrites obj_1
- rotate_clockwise(grid, degree=90): returns rotated grid clockwise by a degree of 90, 180, 270 degrees
- horizontal_flip(grid): returns a horizontal flip of the grid
- vertical_flip(grid): returns a vertical flip of the grid
- replace(grid, grid_1, grid_2): replaces all occurences of grid_1 with grid_2 in grid
- get_object_color(obj): returns color of object. if multicolor, returns first color only
- change_object_color(obj, value): changes the object color to value
- fill_object(grid, obj, align=False): fills grid with object. If align is True, makes grid same size as object
- fill_row(grid, row_num, value, start_col=0, end_col=30): fills output grid with a row of value at row_num from start_col to end_col (inclusive)
- fill_col(grid, col_num, value, start_row=0, end_row=30): fills output grid with a column of value at col_num from start_row to end_row (inclusive)
- fill_between_coords(grid, coord_1, coord_2, value): fills line between coord_1 and coord_2 with value
- fill_rect(grid, tl, br, value): fills grid from tl to br with value. useful to create rows, columns, rectangles
- fill_value(grid, pos, value): fills grid at position with value
- enclose_pixel(grid, pos, value): enclosed a pixel with a square with value
- enlarge_grid(grid, pos, value): enlarges grid based on the horizontal factor for horizontal scaling and the vertical factor for vertical scaling
- enlarge_object(obj, factor_width=1, factor_height=1, scaling_center=’top_left’): enlarges object based on the horizontal factor for horizontal scaling and the vertical factor for vertical scaling. Scaling_center can be ‘top_left’, ‘top_right’, ‘bottom_left’, ‘bottom_right’, ‘center’. Center can be used only when the factors are odd numbers
"""

conditional_functions = """
- object_contains_color(obj, value): returns True/False if object contains a certain value
- on_same_line(coord_1, coord_2, line_type): Returns True/False if coord_1 is on the same line as coord_2. line_type can be one of ['row', 'col', 'diag']
"""

system_prompt = (
    """You are given a series of inputs and output pairs. 
The values from 'a' to 'j' represent different colors. '.' is a blank cell.
For example, [['.','a','.'],['.','.','b']] represents a 2 row x 3 col grid with color a at position (1,0) and color b at position (2,1).
Coordinates are 2D positions (row, col), row representing row number, col representing col number, with zero-indexing.
Input/output pairs may not reflect all possibilities, you are to infer the simplest possible relation.
Each of the input-output relation can be done with one or more helper functions chained together. 
Some relations require other functions, which you will need to come up with yourself.
Objects are tight-fitted grids (no empty row or column) with a top left coordinate, which can be used for easy manipulation of multiple coordinates.
You can create your own objects by just creating a dictionary with 'tl' and 'grid'
You can change an object's position by using 'tl' and its composition using 'grid'.
You should start each program by copying input grid or empty_grid or crop_grid of desired output size.
Then, fill the grid by using the fill helper functions.
If you use the fill functions with a '.' value, it is equivalent to removing parts of the grid.

Helper functions:\n"""
    + helper_functions
    + """\n
assert get_objects([['a','a','a'],['a','.','a'],['a','a','a']],more_info=False)==[{'tl':(0, 0),'grid':[['a','a','a'],['a','.','a'],['a','a','a']]},{'tl':(1,1),'grid':[['$']]}]
assert get_pixel_coords([['a','a'],['d','f']])=={'a':[(0, 0),(0, 1)],'d':[(1, 0)],'f':[(1, 1)]}
assert empty_grid(3, 2)==[['.','.'], ['.','.'], ['.','.']]
assert crop_grid([['a','a','b'],['.','a','b']],(0, 0),(1, 1))==[['a','a'],['.','a']]
assert tight_fit([['.','.','.'],['.','a','.'],['.','.','.']])==[['a']]
assert combine_object({'tl':(0, 0),'grid':[['a','a'],['a','.']]},{'tl': (1, 1),'grid':[['f']]})=={'tl':(0, 0),'grid':[['a','a'],['a','f']]}
assert rotate_clockwise([['a','b'],['d','e']],90)==[['d','a'],['e','b']]
assert rotate_clockwise([['a','b'],['d','e']],270)==[['b','e'],['a','d']]
assert horizontal_flip([['a','b','c'],['d','e','f']])==[['c','b','a'], ['f','e','d']]
assert vertical_flip([['a','b','c'],['d','e','f']])==[['d','e','f'],['a','b','c']]
assert replace([['a','.'],['a','a']],[['a','a']],[['c','c']])==[['a','.'],['c','c']]
assert change_object_color({'tl':(0,0),'grid':[['a','.']]},'b')=={'tl':(0,0),'grid':[['b','.']]}
assert get_object_color({'tl':(0,0),'grid':[['a','.']]})=='a'
assert fill_object([['.','.'],['.','.']],{'tl':(0, 1),'grid':[['c'],['c']]})==[['.','c'],['.','c']]
assert fill_value([['.','a'],['.','a']],(1,1),'b')==[['.','a'],['.','b']]
assert fill_row([['a','a'],['c','a']],0,'b')==[['b','b'],['c','a']]
assert fill_col([['a','a'],['c','a']],0,'b')==[['b','a'],['b','a']]
assert fill_rect([['a','a'],['c','a']],(0,0),(1,1),'b')==[['b','b'],['b','b']]
assert fill_between_coords([['.','.']],(0,0),(0,1),'a')==[['a','a']]
assert enclose_pixel([['.','.', '.'], ['.', 'a', '.'], ['.', '.', '.']],(1,1),'b')==[['b','b','b'], ['b','a','b'], ['b','b','b']]
assert enlarge_grid([['.', 'b'], ['a', 'c']], 2, 1)==[['.', '.', 'b', 'b'], ['a', 'a', 'c', 'c']]
assert enlarge_object({'tl':(3, 4),'grid':[['.','a'],['a','.']]}, 1, 2, 'bottom_right')=={'tl':(3, 2),'grid':[['.','a'],['.','a'],['a','.'],['a','.']]}

Each helper function can be conditional. The conditions can be:
- by attribute, such as shape, color, position, size, cell number of object
- the condition can be an attribute on all objects, for instance, objects with the most common or least common value, or objects with the most or least common shape
- by position of pixels, such as row or column
- by neighbouring cell types or values

There are some conditional functions to help you:\n"""
    + conditional_functions
    + """
assert object_contains_color({'tl':(0,0),'grid':[['a']]},'a')==True
assert on_same_line((1,1),(1,2),'row')==True
assert on_same_line((1,1),(2,1),'col')==True
assert on_same_line((1,1),(2,2),'diag')==True
"""
)

output_format = {
    "reflection": "High level simple overview of input-output relation for all pairs",
    "pixel_object_changes": "describe the changes between the input and output pixels or objects, focusing on movement, pattern changes, object changes, number, size, shape, position, value, cell count",
    "helper_functions": "list any relevant helper_functions for this task",
    "program_instructions": "Plan how to write the python function and what helper functions and conditions to use",
}

output_format_prompt = f"""\nYou are to output the following in json format: {output_format}.
Do not use quotation marks ' or " within the fields unless it is required for the python code"""
