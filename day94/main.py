import time

import pyautogui
from PIL import ImageOps

# ------------------------------ CONFIG ------------------------------ #
# Tune these values if your browser zoom/resolution differs.
START_DELAY_SECONDS = 3
SCAN_WIDTH = 210
LOW_SCAN_HEIGHT = 45
HIGH_SCAN_HEIGHT = 35
LOW_DARK_PIXEL_THRESHOLD = 35
HIGH_DARK_PIXEL_THRESHOLD = 25
JUMP_COOLDOWN_SECONDS = 0.06
DUCK_HOLD_SECONDS = 0.18
LOOP_SLEEP_SECONDS = 0.01


def dark_pixel_count(image, darkness_cutoff=95):
    """
    Count how many pixels are darker than darkness_cutoff.
    Lower cutoff means only very dark pixels are counted.
    """
    grayscale = ImageOps.grayscale(image)
    return sum(1 for pixel in grayscale.getdata() if pixel < darkness_cutoff)


def main():
    print("Open https://elgoog.im/dinosaur-game/ in your browser.")
    print("Make sure the game tab is focused and visible.")
    print(f"Starting in {START_DELAY_SECONDS} seconds...")
    time.sleep(START_DELAY_SECONDS)
    
    # Start/restart game.
    pyautogui.press("space")
    time.sleep(0.2)

    # Dino anchor: use current mouse location as dino position.
    # Move mouse over the dinosaur body before countdown ends.
    dino_x, dino_y = pyautogui.position()
    print(f"Using dino anchor at screen coordinates: ({dino_x}, {dino_y})")
    print("Move mouse to top-left corner to trigger PyAutoGUI failsafe and stop.")

    last_jump_time = 0.0
    ducking = False
    duck_release_time = 0.0

    while True:
        now = time.time()

        # # Get mouse cursor position
        # dino_x, dino_y = pyautogui.position()

        # Fixed dino position (his nose is at 210, 651)
        dino_x = 210                                                                          
        dino_y = 651

        # Regions in front of dino:      
        # - low region catches cactus
        # - high region catches flying birds
        low_region = (   
            dino_x + 35,              
            dino_y - 5,
            SCAN_WIDTH,     
            LOW_SCAN_HEIGHT,
        )
        high_region = (
            dino_x + 45,
            dino_y - 55,
            SCAN_WIDTH - 40,
            HIGH_SCAN_HEIGHT,
        )

        low_shot = pyautogui.screenshot(region=low_region)
        high_shot = pyautogui.screenshot(region=high_region)

        low_dark_pixels = dark_pixel_count(low_shot)
        high_dark_pixels = dark_pixel_count(high_shot)

        low_obstacle = low_dark_pixels > LOW_DARK_PIXEL_THRESHOLD
        high_obstacle = high_dark_pixels > HIGH_DARK_PIXEL_THRESHOLD

        # If bird is detected high, duck briefly.
        if high_obstacle and not low_obstacle:         
            if not ducking:
                pyautogui.keyDown("down")
                ducking = True
                duck_release_time = now + DUCK_HOLD_SECONDS
        else:
            # Release duck when hold time passes.
            if ducking and now >= duck_release_time:
                pyautogui.keyUp("down")
                ducking = False

            # Jump for low obstacle if cooldown passed.
            if low_obstacle and (now - last_jump_time) >= JUMP_COOLDOWN_SECONDS:
                pyautogui.press("space")
                last_jump_time = now        

        time.sleep(LOOP_SLEEP_SECONDS)


if __name__ == "__main__":
    # PyAutoGUI safety: moving mouse to top-left raises FailSafeException.
    pyautogui.FAILSAFE = True
    main()
