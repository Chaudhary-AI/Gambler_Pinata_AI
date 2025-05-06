import cv2
import numpy as np

def detect_glow(frame):
    """
    Detects glow patterns in the given frame using OpenCV.
    """
    if frame is None:
        print("❌ No frame provided for glow detection.")
        return

    # Step 1: Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Step 2: Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)

    # Step 3: Apply thresholding to isolate bright regions
    _, thresholded = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)

    # Step 4: Find contours of the bright regions
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Step 5: Draw contours on the original frame
    output = frame.copy()
    cv2.drawContours(output, contours, -1, (0, 255, 0), 2)

    # Step 6: Display results
    cv2.imshow("Original Frame", frame)
    cv2.imshow("Thresholded", thresholded)
    cv2.imshow("Glow Detection", output)

    print(f"🔍 Detected {len(contours)} glow regions.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Example: Load a test image
    test_image_path = "test_image.png"  # Replace with your test image path
    frame = cv2.imread(test_image_path)

    if frame is not None:
        detect_glow(frame)
    else:
        print("❌ Test image not found.")