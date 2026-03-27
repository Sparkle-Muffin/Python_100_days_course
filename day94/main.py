import time
import pyautogui
from PIL import ImageOps

# ------------------------------ CONFIG ------------------------------ #
# Tune these values if your browser zoom/resolution differs.
START_DELAY_SECONDS = 3
SCAN_HEIGHT = 100
DARK_PIXEL_THRESHOLD = 35
LOOP_SLEEP_SECONDS = 0.01
FIRST_PERIOD = 6 # seconds
SECOND_PERIOD = 10 # seconds
THIRD_PERIOD = 20 # seconds


def dark_pixel_count(image, darkness_cutoff=95):
    """
    Count how many pixels are darker than darkness_cutoff.
    Lower cutoff means only very dark pixels are counted.
    """
    grayscale = ImageOps.grayscale(image)
    return sum(1 for pixel in grayscale.getdata() if pixel < darkness_cutoff)


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
        if now - start_time >= FIRST_PERIOD:
            offset = 50
            scan_width = 230
        if now - start_time >= SECOND_PERIOD:
            offset = 80
        if now - start_time >= THIRD_PERIOD:
            offset = 150

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
        dark_pixels = dark_pixel_count(shot)
        obstacle = dark_pixels > DARK_PIXEL_THRESHOLD                  

        if obstacle:
            pyautogui.press("space")

        time.sleep(LOOP_SLEEP_SECONDS)


if __name__ == "__main__":
    # PyAutoGUI safety: moving mouse to top-left raises FailSafeException.
    pyautogui.FAILSAFE = True
    main()
