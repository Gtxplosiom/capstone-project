import math


## CALCULATE THE DISTANCE BETWEEN TWO PIXELS IN 2-DIMENSION

def calculate_pixel_distance(pixel_width1, pixel_height1, pixel_width2, pixel_height2):
    pixel_distance = math.sqrt((pixel_width2 - pixel_width1)**2 + (pixel_height2 - pixel_height1)**2)
    return pixel_distance

# Example coordinates
pixel_width1, pixel_height1 = 960, 540
pixel_width2, pixel_height2 = 1920, 540

# Calculate pixel distance
distance = calculate_pixel_distance(pixel_width1, pixel_height1, pixel_width2, pixel_height2)

# Print the result
print(f"The pixel distance between pixels ({pixel_width1}, {pixel_height1}) and ({pixel_width2}, {pixel_height2}) is approximately {distance:.2f} pixels.")