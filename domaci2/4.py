import numpy as np
from numpy import linalg as la
np.set_printoptions(precision=5, suppress=True)


def transform(t, M):
    n = len(t)
    transformed_t = []

    for i in range(n):
        transformed_t.append(
            np.matmul(M, t[i])
        )

    return transformed_t

def affine_transform(t):
    return [t[0]/t[2], t[1]/t[2]]

def homogeneous_transform(t):
    return [t[0], t[1], 1]

def normMatrix(points):
    n = len(points)

    centroid_x = 0
    centroid_y = 0
    affine_points = []
    for i in range(n):
        affine_points.append(affine_transform(points[i]))
        centroid_x = centroid_x + affine_points[i][0]
        centroid_y = centroid_y + affine_points[i][1]

    centroid_x = centroid_x/n
    centroid_y = centroid_y/n

    O = [[1, 0, -centroid_x],
        [0, 1, -centroid_y],
        [0, 0, 1]
    ]
    for i in range(n):
        affine_points[i] = np.matmul(O, homogeneous_transform(affine_points[i]))

    d = 0 
    for i in range(n):
        tmp = np.square(affine_points[i][0]) + np.square(affine_points[i][1])
        d = d + np.sqrt(tmp)
    d = d/n

    H = [
        [np.sqrt(2)/d, 0, 0],
        [0, np.sqrt(2)/d, 0],
        [0, 0, 1]
    ]
    for i in range(n):
        affine_points[i] = np.matmul(H, homogeneous_transform(affine_points[i]))

    return np.matmul(H, O)


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

    U, D, V_tr = la.svd(M)


    dlt = V_tr[len(V_tr) - 1].reshape(3, 3)
    dlt /= dlt[2, 2] * 1.0
    return dlt

def DLTwithNormalization(origs, imgs):
    n = len(origs)

    M_norm_for_t = normMatrix(origs)
    norm_t = transform(origs, M_norm_for_t)

    M_norm_for_pt = normMatrix(imgs)
    norm_pt = transform(imgs, M_norm_for_pt)

    P_dlt = DLT(norm_t, norm_pt)

    P_norm_dlt = np.matmul(P_dlt, M_norm_for_t)
    P_norm_dlt = np.matmul(la.inv(M_norm_for_pt), P_norm_dlt)
    matrix = np.round(P_norm_dlt, decimals=10)
    matrix /= matrix[2, 2] * 1.0
    return matrix