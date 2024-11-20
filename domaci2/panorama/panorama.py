import cv2
import easygui
import numpy as np
import matplotlib.pyplot as plt

def panorama(img1, img2):
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)

    sift = cv2.SIFT.create()

    keypoints1, descriptors1 = sift.detectAndCompute(img2_gray, mask=None)
    keypoints2, descriptors2 = sift.detectAndCompute(img1_gray, mask=None)

    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    
    matches = bf.match(descriptors1, descriptors2)
  
    keypoints1 = np.float32([kp.pt for kp in keypoints1])
    keypoints2 = np.float32([kp.pt for kp in keypoints2])
        
    if len(matches) > 4:
        src_pts = np.float32([keypoints1[m.queryIdx] for m in matches])
        dst_pts = np.float32([keypoints2[m.trainIdx] for m in matches])

        homography, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 4)

    width = img2.shape[1] + img1.shape[1]
    height = img2.shape[0] + img1.shape[0]

    img_final = cv2.warpPerspective(img2, homography, (width, height))
    img_final[0:img1.shape[0], 0:img1.shape[1]] = img1

    # Convert to RGB for display in matplotlib
    img_final_rgb = cv2.cvtColor(img_final, cv2.COLOR_BGR2RGB)

    # Create a mask of non-black pixels
    non_black_mask = np.any(img_final != 0, axis=-1)

    # Find the bounding box of non-black pixels
    non_black_coords = np.column_stack(np.where(non_black_mask))

    # Get the min and max coordinates of the bounding box
    top_left = non_black_coords.min(axis=0)
    bottom_right = non_black_coords.max(axis=0)

    # Crop the image to the bounding box
    img_cropped = img_final[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1]

    # Show the cropped image
    plt.imshow(cv2.cvtColor(img_cropped, cv2.COLOR_BGR2RGB))
    plt.show()

if __name__ == "__main__":
    code1 = easygui.fileopenbox()
    img1 = cv2.imread(code1, 1)
    plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    plt.show()

    code2 = easygui.fileopenbox()
    img2 = cv2.imread(code2, 1)
    plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    plt.show()

    panorama(img1, img2)
