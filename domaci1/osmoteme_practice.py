import numpy as np
import math

def crossProduct(a, b):
   return np.cross(a, b)

def osmoTeme(arr):
   # 7-8  6-5  1-2
   Xn1 = crossProduct(crossProduct(arr[5], arr[6]),crossProduct(arr[3], arr[4]))
   Xn1 = (Xn1[0]/Xn1[2], Xn1[1]/Xn1[2], 1)
   Xn2 = crossProduct(crossProduct(arr[5], arr[6]), crossProduct(arr[0], arr[1]))
   Xn2 = (Xn2[0]/Xn2[2], Xn2[1]/Xn2[2], 1)
   Xn3 = crossProduct(crossProduct(arr[3], arr[4]), crossProduct(arr[0], arr[1]))
   Xn3 = (Xn3[0]/Xn3[2], Xn3[1]/Xn3[2], 1)
   Xn = (((Xn1[0] + Xn2[0] + Xn3[0]) / 3), ((Xn1[1] + Xn2[1] + Xn3[1]) / 3), ((Xn1[2] + Xn2[2] + Xn3[2]) / 3))
   Xn = (Xn[0]/Xn[2], Xn[1]/Xn[2], 1)
   

   Yn1 = crossProduct(crossProduct(arr[0], arr[3]),crossProduct(arr[1], arr[4]))
   Yn1 = (Yn1[0]/Yn1[2], Yn1[1]/Yn1[2], 1)
   Yn2 = crossProduct(crossProduct(arr[0], arr[3]), crossProduct(arr[2], arr[5]))
   Yn2 = (Yn2[0]/Yn2[2], Yn2[1]/Yn2[2], 1)
   Yn3 = crossProduct(crossProduct(arr[1], arr[4]), crossProduct(arr[2], arr[5]))
   Yn3 = (Yn3[0]/Yn3[2], Yn3[1]/Yn3[2], 1)
   Yn = (((Yn1[0] + Yn2[0] + Yn3[0]) / 3), ((Yn1[1] + Yn2[1] + Yn3[1]) / 3), ((Yn1[2] + Yn2[2] + Yn3[2]) / 3))
   Yn = (Yn[0]/Yn[2], Yn[1]/Yn[2], 1)

   res = crossProduct(crossProduct(Xn, arr[2]), crossProduct(Yn, arr[6]))
   res = (res[0]/res[2], res[1]/res[2], 1)
   return res

# t5, t6, t7, t8, t1, t2, t3
# fali 4ta tacka :3
# tacke = [[32, 70], [195, 144], [195, 538], [30, 307], [251, 40], [454, 78], [455, 337]]
# tacke = [[639, 125], [472, 306], [131, 175], [407, 79], [605, 292], [445, 555], [166, 384]]
tacke = [[605, 292], [445, 555], [166, 387], [639, 125], [472, 306], [131, 175], [407, 79]]
      #      1           2           3           5           6           7          8
      #      0           1           2           3           4           5          6
for tacka in tacke:
   tacka.append(1)
missingPoint = osmoTeme(tacke)
print((np.floor(missingPoint[0]), np.floor(missingPoint[1])))