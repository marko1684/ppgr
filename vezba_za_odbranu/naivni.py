import numpy as np
from numpy import linalg as la

np.set_printoptions(precision=5, suppress=True)

def proveraOpstegPolozaja(points):
   n = len(points)
   for i in range(n):
      for j in range(i + 1, n):
         for k in range(j + 1, n):
            M = np.array([points[i], points[j], points[k]])
            det = la.det(M)
            if det == 0:
               return False
   return True

def naivni(origs, imgs):
   if not proveraOpstegPolozaja(origs):
      return "Losi originali!"
   if not proveraOpstegPolozaja(imgs):
      return "Lose slike!"
   
   A, B, C, D = origs
   A_, B_, C_, D_ = imgs

   A = np.array(A)
   B = np.array(B)
   C = np.array(C)
   D = np.array(D)

   A_ = np.array(A_)
   B_ = np.array(B_)
   C_ = np.array(C_)
   D_ = np.array(D_)   

   mat = np.array([A, B, C]).T
   mat1 = np.array([D, B, C]).T
   mat2 = np.array([A, D, C]).T
   mat3 = np.array([A, B, D]).T
   detMat = la.det(mat)
   lam1 = la.det(mat1)/detMat.T
   lam2 = la.det(mat2)/detMat.T
   lam3 = la.det(mat3)/detMat.T

   mat_ = np.array([A_, B_, C_])
   mat1_ = np.array([D_, B_, C_])
   mat2_ = np.array([A_, D_, C_])
   mat3_ = np.array([A_, B_, D_])
   detMat_ = la.det(mat_)
   lam1_ = la.det(mat1_)/detMat_
   lam2_ = la.det(mat2_)/detMat_
   lam3_ = la.det(mat3_)/detMat_

   P1 = np.column_stack([lam1 * A, lam2 * B, lam3 * C])
   P2 = np.column_stack([lam1_ * A_, lam2_ * B_, lam3_ * C_])

   P = np.matmul(P2, la.inv(P1))
   
   return P/P[2,2]

trapez = [[- 3, - 1, 1], [3, - 1, 1], [1, 1, 1], [- 1, 1, 1]] 
pravougaonik = [[- 2, - 1, 1], [2, - 1, 1], [2, 1, 1], [- 2, 1, 1]]
print(naivni(trapez, pravougaonik))

origs = [[- 3, - 1, 1], [3, - 1, 1], [1, 1, 1], [- 1, 1, 1]] 
imgs = [[- 2, - 5, 1], [2, - 5, 1], [2, 1, 1], [6, -3, 3]]   #primetite da nisu u opstem polozaju
print(naivni(origs, imgs))