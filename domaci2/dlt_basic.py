import numpy as np
from numpy import linalg as la

np.set_printoptions(precision=5, suppress=True)


def corespondece(a, a_):
   return [[0, 0, 0, -a_[2] * a[0], -a_[2] * a[1], -a_[2] * a[2], a_[1] * a[0], a_[1] * a[1], a_[1] * a[2]],
                    [a_[2] * a[0], a_[2] * a[1], a_[2] * a[2], 0, 0, 0, -a_[0] * a[0], -a_[0] * a[1], -a_[0] * a[2]]]


def DLT(origs, imgs):
   A = []
   n = len(origs)
   for i in range(n):
      A.extend(corespondece(origs[i], imgs[i]))

   _, _, V_t = la.svd(A)

   dlt = V_t[len(V_t) - 1].reshape(3, 3)

   return dlt / dlt[2, 2]

trapez = [[- 3, - 1, 1], [3, - 1, 1], [1, 1, 1], [- 1, 1, 1], [1,2,3], [-8,-2,1]] 
pravougaonik1 = [[- 2, - 1, 1], [2, - 1, 1], [2, 1, 1], [- 2, 1, 1], [2,1,5], [-16,-5,5]]
print(DLT(trapez, pravougaonik1))