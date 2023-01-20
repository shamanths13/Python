# Program to add two matrices using nested loop

# Create two matrixes of same dimensions of rows and columns
# The rows and columns do not have to be equal but the two matrices must have same dimensions

rows=3
columns=3

matrix_x = [[1,2,3],
            [4,5,6],
            [7,8,9]]

matrix_y = [[9,8,7],
            [6,5,4],
            [3,2,1]]

# Create an empty matrix of dimensions n*m, whose elements we can replace
matrix_sum = [[0,0,0],
              [0,0,0],
              [0,0,0]]

# Create a nested for loop to iterate through rows and columns  
# Iterate through rows
for i in range(rows):
# Iterate through columns
    for j in range(columns):
        matrix_sum[i][j] = matrix_x[i][j] + matrix_y[i][j]

# Print the resultant matrix by looping through the rows
for n in matrix_sum:
    print(n)