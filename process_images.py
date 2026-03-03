import cv2
import numpy as np
import os

def remove_background(input_path, output_path):
    # Read the image
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Error: Could not read {input_path}")
        return

    # Convert to BGRA if not already
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    # Define the white color range
    # Assuming white background (255, 255, 255)
    # We create a mask for pixels that are very close to white
    lower_white = np.array([240, 240, 240, 0])
    upper_white = np.array([255, 255, 255, 255])
    
    mask = cv2.inRange(img, lower_white, upper_white)
    
    # Set the alpha channel to 0 for the masked pixels
    img[mask == 255, 3] = 0

    # Save the result
    cv2.imwrite(output_path, img)
    print(f"Saved transparent image to {output_path}")

# Paths
steering_in = r"C:\Users\USRE\.gemini\antigravity\brain\5ce31067-23c5-48ef-a0d4-0ef4aa971879\steering_wheel_icon_1772530814875.png"
nitro_in = r"C:\Users\USRE\.gemini\antigravity\brain\5ce31067-23c5-48ef-a0d4-0ef4aa971879\nitro_icon_1772530834369.png"

steering_out = r"d:\Downloads\Racing-CV\assets\steering.png"
nitro_out = r"d:\Downloads\Racing-CV\assets\nitro.png"

remove_background(steering_in, steering_out)
remove_background(nitro_in, nitro_out)
