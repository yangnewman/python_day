# import cv2
# import numpy as np
# from matplotlib import pyplot as plt
#
# img = cv2.imread('messi5.jpg',0)
# edges = cv2.Canny(img,100,200)
#
# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
#
# plt.show()

import cv2
import numpy as np

img = cv2.imread("./sudoku.jpg", 0)
cv2.imwrite("./images/canny.jpg", cv2.Canny(img, 200, 300))
cv2.imshow("canny", cv2.imread("canny.jpg"))
cv2.waitKey()
cv2.destroyAllWindows()









