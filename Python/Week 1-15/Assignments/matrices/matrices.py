import numpy as np

def describe(array):
    print(array, "\n")
    print(array.shape, array.dtype, "\n")

def multiply(array1, array2):
    if array1.shape[1] != array2.shape[0]:
        print("Cannot multiply: these 2 arrays have incompatible dimensions")
        return None
    result = np.dot(array1, array2)
    return result

def determinant(d_array):
    if d_array.shape[0] != d_array.shape[1]:
        print("Cannot find determinant: not a square matrix")
        return None
    result = np.linalg.det(d_array)
    return result

def inverse(i_array):
    if i_array.shape[0] != i_array.shape[1]:
        print("Cannot find inverse: not a square matrix")
        return None
    result = np.linalg.inv(i_array)
    return result

def check_solution(a, b, x):
    # multiply A*x and make sure we get b
    assert np.allclose(np.dot(a, x), b)

def solve_linear_system(a, b, unknowns):
    x = np.linalg.solve(a, b)
    check_solution(a, b, x)
    results = dict(zip(unknowns, x))
    return results

def main():
    a = np.array([[6, -1], [12, 8], [-5, 4]])
    b = np.array([[4, 0], [0.5, 2]])
    c = np.array([[2, -2], [3, 1]])

    describe(a)
    describe(b)
    describe(c)

    print(multiply(a, a))
    print(multiply(b, b))
    print(multiply(c, c))
    print(multiply(a, b))
    print(multiply(a, c))
    print(multiply(b, a))
    print(multiply(b, c))
    print(multiply(c, a))
    print(multiply(c, b))

    print(determinant(a))
    print(determinant(b))
    print(determinant(c))

    print(inverse(a))
    print(inverse(b))
    print(inverse(c))

    A = np.array([[0, -7, 5],[0, 4, 7],[-4, 3, -7]])
    B = np.array([50, -30, -40])
    unknowns = ["x1", "x2", "x3"]
    print(solve_linear_system(A, B, unknowns))

if __name__ == "__main__":
    main()