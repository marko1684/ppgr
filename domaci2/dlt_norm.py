import numpy as np
from numpy import linalg as la
import math

np.set_printoptions(precision=5, suppress=True)

def transform(points, M):
   n = len(points)
   transformed_t = []
   
   for i in range(n):
      transformed_t.append(np.matmul(M, points[i]))

   return np.array(transformed_t)

def affine_transform(point):
   return np.array([point[0] / point[2], point[1] / point[2]])

def homogeneous_transform(point):
   return np.array([point[0], point[1], 1])

def normMatrix(points):
   n = len(points)
   points = np.array(points)

   centroid_x = 0
   centroid_y = 0
   affine_points = []

   # Transform points to affine (2D)
   for i in range(n):
      affine_points.append(affine_transform(points[i]))
      centroid_x += affine_points[i][0]
      centroid_y += affine_points[i][1]

   affine_points = np.array(affine_points)

   # Calculate centroid
   centroid_x /= n
   centroid_y /= n

   # Translation matrix
   trans = [[1, 0, -centroid_x],
            [0, 1, -centroid_y],
            [0, 0, 1]]
   
   trans = np.array(trans)

   # Apply translation to affine points (using homogeneous coordinates)
   translated_points = []
   for i in range(n):
      translated_points.append(np.matmul(trans, homogeneous_transform(affine_points[i])))

   translated_points = np.array(translated_points)

   # Calculate average distance to the origin
   d = 0
   for i in range(n):
      d = d + np.sqrt(np.square(translated_points[i, 0]) + np.square(translated_points[i, 1]))

   d = d / n

   # Scaling matrix
   H = [[np.sqrt(2) / d, 0, 0],
        [0, np.sqrt(2) / d, 0],
        [0, 0, 1]]

   # Apply scaling to affine points
   for i in range(n):
      translated_points[i] = np.matmul(H, homogeneous_transform(translated_points[i]))

   # Return the normalization matrix
   return np.matmul(H, trans)


def correspondence(a, a_):
   return np.array([[0, 0, 0, -a_[2] * a[0], -a_[2] * a[1], -a_[2] * a[2], a_[1] * a[0], a_[1] * a[1], a_[1] * a[2]],
           [a_[2] * a[0], a_[2] * a[1], a_[2] * a[2], 0, 0, 0, -a_[0] * a[0], -a_[0] * a[1], -a_[0] * a[2]]])

def DLT(origs, imgs):
   n = len(origs)
   A = []

   for i in range(n):
      A.extend(correspondence(origs[i], imgs[i]))

   _, _, V_t = la.svd(A)

   dlt = V_t[len(V_t) - 1].reshape(3, 3)
   dlt /= dlt[2, 2]
   return dlt

def DLTWithNormalization(origs, imgs):
   n = len(origs)

   normMatrixForOrigs = normMatrix(origs)
   normMatrixForImgs = normMatrix(imgs)
   normalized_origs = transform(origs, normMatrixForOrigs)
   normalized_imgs = transform(imgs, normMatrixForImgs)

   P_dlt = DLT(normalized_origs, normalized_imgs)

   P_norm_dlt = np.matmul(P_dlt, normMatrixForOrigs)
   P_norm_dlt = np.matmul(la.inv(normMatrixForImgs), P_norm_dlt)

   P_norm_dlt /= P_norm_dlt[2, 2]
   return P_norm_dlt

trapez = [[- 3, - 1, 1], [3, - 1, 1], [1, 1, 1], [- 1, 1, 1], [1,2,3], [-8,-2,1]] 
pravougaonik1 = [[- 2, - 1, 1], [2, - 1, 1], [2, 1, 1], [- 2, 1, 1], [2,1,5], [-16,-5,5]]
print(DLTWithNormalization(trapez, pravougaonik1))