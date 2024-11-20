import numpy as np
from numpy import linalg  as LA
np.set_printoptions(precision=5, suppress=True)

def correspondence(t, pt):
    Mi = np.matrix([
        [0, 0, 0, -pt[2] * t[0], -pt[2] * t[1], -pt[2] * t[2], pt[1] * t[0], pt[1] * t[1], pt[1] * t[2]],
        [pt[2] * t[0], pt[2] * t[1], pt[2] * t[2], 0, 0, 0, -pt[0] * t[0], -pt[0] * t[1], -pt[0] * t[2]]])
    return Mi

def DLT(origs, imgs):
    n = len(origs)
    M = []

    for i in range(n):
        if i > 0:
            Mi = correspondence(origs[i], imgs[i])
            M = np.concatenate((M, Mi))
        else:
            M = correspondence(origs[i], imgs[i])

    U, D, V_tr = LA.svd(M)

    dlt = V_tr[len(V_tr) - 1].reshape(3, 3)
    dlt /= dlt[2, 2] * 1.0
    return dlt


trapez = [[- 3, - 1, 1], [3, - 1, 1], [1, 1, 1], [- 1, 1, 1], [1,2,3], [-8,-2,1]] 
pravougaonik1 = [[- 2, - 1, 1], [2, - 1, 1], [2, 1, 1], [- 2, 1, 1], [2,1,5], [-16,-5,5]]
print(DLT(trapez, pravougaonik1))