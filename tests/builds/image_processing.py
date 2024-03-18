import cv2
import numpy as np

# Read the image
img = cv2.imread('media/sample_image.png', cv2.IMREAD_GRAYSCALE)

# Thresholding
_, binary_img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

# Adaptive Thresholding #include
adaptive_threshold_img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# Dilation and Erosion
kernel = np.ones((5, 5), np.uint8)
dilated_img = cv2.dilate(binary_img, kernel, iterations=1)
eroded_img = cv2.erode(dilated_img, kernel, iterations=1)

# Contrast Stretching #include
min_intensity, max_intensity = np.percentile(img, (5, 95))
contrast_stretched_img = np.clip((img - min_intensity) / (max_intensity - min_intensity) * 255, 0, 255).astype(np.uint8)

# Histogram Equalization
equalized_img = cv2.equalizeHist(img)

# Blur and Sharpen #include
blurred_img = cv2.GaussianBlur(img, (5, 5), 0)
sharpened_img = cv2.addWeighted(img, 1.5, blurred_img, -0.5, 0)

# Display the original and enhanced images
cv2.imshow('Original Image', img)
cv2.imshow('Binary Image', binary_img)
cv2.imshow('Adaptive Thresholding', adaptive_threshold_img)
cv2.imshow('Dilated Image', dilated_img)
cv2.imshow('Eroded Image', eroded_img)
cv2.imshow('Contrast Stretched Image', contrast_stretched_img)
cv2.imshow('Equalized Image', equalized_img)
cv2.imshow('Sharpened Image', sharpened_img)

# Wait for a key press and close all windows
cv2.waitKey(0)
cv2.destroyAllWindows()
