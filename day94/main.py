import time
import pyautogui
from PIL import ImageOps

# ------------------------------ CONFIG ------------------------------ #
# Tune these values if your browser zoom/resolution differs.
START_DELAY_SECONDS = 3
SCAN_HEIGHT = 100
CONTRAST_PIXEL_THRESHOLD = 35
LOOP_SLEEP_SECONDS = 0.01
FIRST_PERIOD = 6 # seconds
SECOND_PERIOD = 10 # seconds
THIRD_PERIOD = 20 # seconds


def detect_dark_theme(image, darkness_cutoff=95, dark_ratio_threshold=0.5):
    """
    Determine if the game is in dark theme using the same screenshot.
    In dark theme, background is dark, so usually >50% of pixels are dark.
    Returns:
    - is_dark_theme (bool)
    - dark_pixels (int)
    - total_pixels (int)
    """
    grayscale = ImageOps.grayscale(image)
    pixels = list(grayscale.getdata())
    total_pixels = len(pixels)
    dark_pixels = sum(1 for pixel in pixels if pixel < darkness_cutoff)
    dark_ratio = dark_pixels / total_pixels if total_pixels else 0
    return dark_ratio > dark_ratio_threshold, dark_pixels, total_pixels


def main():
    time.sleep(START_DELAY_SECONDS)
    
    # Start/restart game.
    pyautogui.press("space")
    time.sleep(0.2)

    start_time = time.time()
    offset = 0
    scan_width = 100

    while True:
        pyautogui.failSafeCheck()
        now = time.time()
        if now - start_time >= THIRD_PERIOD:
            offset = 150
        elif now - start_time >= SECOND_PERIOD:
            offset = 80
        elif now - start_time >= FIRST_PERIOD:
            offset = 50
            scan_width = 230

        print(f"{now - start_time} seconds elapsed")
        print(f"Offset: {offset}")
        print(f"Scan width: {scan_width}")
        print("\n")

        # Fixed dino position (his nose is at 196, 654)
        dino_x = 200
        dino_y = 654

        region = (
            dino_x + offset,
            dino_y,
            scan_width,
            SCAN_HEIGHT,
        )

        shot = pyautogui.screenshot(region=region)
        is_dark_theme, dark_pixels, total_pixels = detect_dark_theme(shot)
        light_pixels = total_pixels - dark_pixels

        # Light theme: obstacles are dark.
        # Dark theme: obstacles are light.
        if is_dark_theme:
            obstacle = light_pixels > CONTRAST_PIXEL_THRESHOLD
        else:
            obstacle = dark_pixels > CONTRAST_PIXEL_THRESHOLD

        if obstacle:
            pyautogui.press("space")

        time.sleep(LOOP_SLEEP_SECONDS)


if __name__ == "__main__":
    # PyAutoGUI safety: moving mouse to top-left raises FailSafeException.
    pyautogui.FAILSAFE = True
    main()
