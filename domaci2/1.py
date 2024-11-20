import numpy as np
from numpy import linalg as la

np.set_printoptions(precision=5, suppress=True)

def check_minor(points):
    minors = []
    for i in range(4):
        for j in range(i+1, 4):
            for k in range(j + 1, 4):
                submatrix = points[[i, j, k]]
                minor = np.linalg.det(submatrix)
                minors.append(abs(minor))
    return min(minors)
    
def arrange_the_matrix(M):
    for i in range(3):
        for j in range(3):
            if(M[i][j] > -0.000001 and M[i][j] <= 0):
                M[i][j] = 0
    return M
    
def calculate_coefficients(M):
    a = M[0]
    b = M[1]
    c = M[2]
    d = M[3]
    A = [[a[0], b[0], c[0]],
         [a[1], b[1], c[1]],
         [a[2], b[2], c[2]]]
    invA = la.inv(A)
    
    B = [d[0], d[1], d[2]]
    X = np.matmul(invA, B)
    return X

def naivni(origs, imgs):
    if check_minor(np.array(origs)) < 1e-6:
        return "Losi originali!"
    elif check_minor(np.array(imgs)) < 1e-6:
        return "Lose slike!"
    coeff_orig = calculate_coefficients(origs)
    coeff_img = calculate_coefficients(imgs)
    
    M_orig = [
        [coeff_orig[0] * i for i in origs[0]],
        [coeff_orig[1] * i for i in origs[1]],
        [coeff_orig[2] * i for i in origs[2]]
    ]

    M_img = [
        [coeff_img[0] * i for i in imgs[0]], 
        [coeff_img[1] * i for i in imgs[1]], 
        [coeff_img[2] * i for i in imgs[2]]  
    ]

    M_orig = np.transpose(M_orig)
    M_img = np.transpose(M_img)
    
    naive_matrix = np.matmul(M_img, la.inv(M_orig))
    
    naive_matrix = arrange_the_matrix(naive_matrix)
    naive_matrix /= naive_matrix[2,2] * 1.0
    
    
    
    return naive_matrix

 
origs = [[- 3, - 1, 1], [3, - 1, 1], [1, 1, 1], [- 1, 1, 1]] 
imgs = [[- 2, - 5, 1], [2, - 5, 1], [2, 1, 1], [6, -3, 3]]   #primetite da nisu u opstem polozaju
print(naivni(origs, imgs))

trapez = [[- 3, - 1, 1], [3, - 1, 1], [1, 1, 1], [- 1, 1, 1]] 
pravougaonik = [[- 2, - 1, 1], [2, - 1, 1], [2, 1, 1], [- 2, 1, 1]]
print(naivni(trapez, pravougaonik))