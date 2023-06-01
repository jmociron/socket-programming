import math
import time
import random

# Function for printing in lists in matrix form
def print_matrix(matrix):
    for row in matrix:
        print(row)

# Assign a randomized non-zero value (1-1000) to grid points divisible by 10
def assign_values(matrix):

    for x in range(0, len(matrix), 10):
        for y in range(0, len(matrix), 10):
            matrix[x][y] = float(random.randint(0, 1000))
    
    # print_matrix(matrix)
    return matrix

# Gets the nearest intervals of 10 to the number
def round_number(n):
    

    # Skips rounding if n == 0
    if(n == 0):
        return [0, 10]
    
    # Returns multiples of 10 before and after n
    else:
        rounded = round(n, -1)
        return [rounded-10, rounded]

# Retrieving the indices containing values surrounding the given point (x,y)
def get_surrounding(x,y):

    # cols = round_number(x)
    # rows = round_number(y)

    rows = round_number(x)
    cols = round_number(y)

    surrounding_points = {
        "A": [rows[0], cols[0]], 
        "B": [rows[0], cols[1]], 
        "C": [rows[1], cols[0]], 
        "D": [rows[1], cols[1]], 
    }

    # surrounding_points = {
    #     "A": [rows[0], cols[0]], 
    #     "B": [rows[0], cols[1]], 
    #     "C": [rows[1], cols[0]], 
    #     "D": [rows[1], cols[1]], 
    # }

    return surrounding_points

# Computes for the area between the intermediate point and a given data point
def get_area(int_point, data_point):
    return abs((data_point[0] - int_point[0]) * (data_point[1] - int_point[1]))

# Computes for the elevation of point (x,y) using Area Weighted Interpolation
def aw_inter(x, y, matrix):

    points = get_surrounding(x,y) # Data points (A, B, C, D)
    int_point = [x,y] # Intermediate point E

    area_labels = ["d", "c", "b", "a"]
    area = {}
    i = 0

    for label, coords in points.items():
        area[area_labels[i]] = get_area(int_point, coords)
        i += 1

    numerator = 0

    # Computes for aA + bB + cC + dD    
    for label in list(reversed(area_labels)):
        try:
            x, y = points[label.upper()]
            numerator += area[label] * matrix[x][y]
        except:
            pass
            # print(int_point, points)
            # print(f"X: {x}, Y: {y}, Rows: {len(matrix)}, Cols: {len(matrix[0])}")
            print("\nError in interpolation!")

    # Computes for the elevation of the given point
    elevation = (numerator/sum(area.values()))

    return elevation
    
def terrain_inter(matrix):

    # n = len(matrix)
    row = len(matrix)
    col = len(matrix[0])
    start = time.time()

    print(f"Rows: {row}, Columns: {col}")

    for i in range(row):
        for j in range(col):
            if matrix[i][j] == 0:
                matrix[i][j] = round(aw_inter(i, j, matrix), 2)
    
    end = time.time()
    print_matrix(matrix)
    print("\nTime elapsed:", (end-start))

if __name__ == "__main__":

    # n = int(input("Enter n: "))+1
    n = 21

    # Create a zero n x n square matrix M.
    # matrix = [[200, 0, 0, 0, 0, 0, 0, 0, 0, 0, 500],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10]]
    matrix = [[0 for x in range(n)] for y in range(n)]
    print_matrix(assign_values(matrix))
    terrain_inter(matrix)

    # # Sample matrix from the lab handout
    # n = 11


    # terrain_inter(matrix)
    # print("(0,5)", aw_inter(0,5))
    # print("(5,0)", aw_inter(5,0))
    # print("(5,4)", aw_inter(5,4))
    # print("(5,10)", aw_inter(5,10))
    # print("(10,5)", aw_inter(10,5))

