import numpy as np

def neville(inputs, outputs, x, degree=0):
    input_size = len(inputs)
    n = np.zeros([input_size, input_size])

    for i in range(0, input_size):
        n[i][0] = outputs[i]

    for i in range(1, input_size):
        for j in range(1, i + 1):
            term1 = (x - inputs[i - j]) * n[i][j - 1]
            term2 = (x - inputs[i]) * n[i - 1][j - 1]

            n[i][j] = (term1 - term2) / (inputs[i] - inputs[i - j])

    if degree > 0:
        degree = min(degree, input_size - 1)
        return n[degree][degree]
    
    for i in range(0, input_size):
        for j in range(0, i + 1):
            print(n[i][j], end=" ")
        print()

def newton_forward(inputs, outputs, x=None, degree=0):
    input_size = len(inputs)
    diffs = np.zeros([input_size, input_size])

    for i in range(0, input_size):
        diffs[i][0] = outputs[i]

    for i in range(1, input_size):
        for j in range(1, i + 1):
            diffs[i][j] = (diffs[i][j - 1] - diffs[i - 1][j - 1]) / (inputs[i] - inputs[i - j])

    if degree > 0 and x == None:
        degree = min(degree, input_size - 1)
        return diffs[degree][degree]
    
    if x != None:
        y = 0
        for i in range(0, input_size):
            temp = diffs[i][i]
            for j in range(0, i):
                temp *= x - inputs[j]
            y += temp
        return y
        
    
    for i in range(0, input_size):
        for j in range(0, i + 1):
            print(diffs[i][j], end=" ")
        print()

def hermite_matrix(inputs, outputs, outputs_d, x=None, degree=0):
    input_size = len(inputs)
    diffs = np.zeros([input_size*2, input_size*2])

    for i in range(0, input_size*2):
        diffs[i][0] = outputs[i//2]
    
    for i in range(0, input_size):
        diffs[i*2 + 1][1] = outputs_d[i]

    for i in range(1, input_size*2):
        for j in range(1, i + 1):
            if diffs[i][j] != 0.0:
                continue
            diffs[i][j] = (diffs[i][j - 1] - diffs[i - 1][j - 1]) / (inputs[i//2] - inputs[(i - j)//2])

    if degree > 0 and x == None:
        degree = min(degree, input_size - 1)
        return diffs[degree][degree]
    
    if x != None:
        y = 0
        for i in range(0, input_size):
            temp = diffs[i][i]
            for j in range(0, i):
                temp *= x - inputs[j]
            y += temp
        return y
        
    print(diffs)
    # for i in range(0, input_size*2):
    #     print(diffs[i])
    #     # for j in range(0, i + 1):
    #     #     print(diffs[i][j], end=" ")
    #     print()

def cubic_spline_A(inputs, outputs):
    input_size = len(inputs)
    A = np.zeros([input_size, input_size])

    A[0][0] = 1
    A[input_size - 1][input_size - 1] = 1
    for i in range(1, input_size - 1):
        h_0 = inputs[i] - inputs[i - 1]
        h_1 = inputs[i + 1] - inputs[i]
        A[i][i - 1] = h_0
        A[i][i] = 2 * (h_0 + h_1)
        A[i][i + 1] = h_1

    print(A)

def cubic_spline_b(inputs, outputs):
    input_size = len(inputs)
    b = np.zeros([input_size])

    for i in range(1, input_size - 1):
        h_0 = inputs[i] - inputs[i - 1]
        h_1 = inputs[i + 1] - inputs[i]
        b[i] = (3 / h_1) * (outputs[i+1] - outputs[i]) - (3 / h_0) * (outputs[i] - outputs[i-i])

    print(b)


if __name__ == "__main__":
    neville_method = neville(
        [3.6, 3.8, 3.9],
        [1.675, 1.436, 1.318],
        3.7,
        2
    )
    print(neville_method)
    print()
    for i in range(1, 3 + 1):
        newton_method = newton_forward(
            [7.2, 7.4, 7.5, 7.6],
            [23.5492, 25.3913, 26.8224, 27.4589],
            degree=i
        )
        print(newton_method)
    print()
    newton_method = newton_forward(
        [7.2, 7.4, 7.5, 7.6],
        [23.5492, 25.3913, 26.8224, 27.4589],
        x=7.3
    )
    print(newton_method)
    print()
    hermite_method = hermite_matrix(
        [3.6, 3.8, 3.9],
        [1.675, 1.436, 1.318],
        [-1.195, -1.188, -1.182]
    )
    print()
    cubic_spline_A([2,5,8,10], [3,5,7,9])
    cubic_spline_b([2,5,8,10], [3,5,7,9])