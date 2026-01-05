import pyautogui
import time
import sys
from pynput import keyboard

IMAGES = [f"{i}.png" for i in range(1, 11)]
LOADING_IMAGE = "loading.png"

CONFIDENCE = 0.7
CLICK_DELAY = 0.2
SCAN_DELAY = 0.5
MOVE_DELAY = 0.15

pyautogui.FAILSAFE = True
running = True


def on_press(key):
    global running
    if key == keyboard.Key.esc:
        running = False
        return False


keyboard.Listener(on_press=on_press).start()


def is_loading():
    try:
        return pyautogui.locateOnScreen(
            LOADING_IMAGE,
            confidence=CONFIDENCE
        ) is not None
    except Exception:
        return False


def image_still_exists(img, region):
    try:
        return pyautogui.locateOnScreen(
            img,
            confidence=CONFIDENCE,
            region=region
        ) is not None
    except Exception:
        return False


def log_action(img):
    if img == "1.png":
        print("entering stage")
    elif img in ("5.png", "8.png"):
        print("skipping stage")
    else:
        print("next step")


def find_and_click():
    if is_loading():
        return

    for img in IMAGES:
        try:
            loc = pyautogui.locateOnScreen(img, confidence=CONFIDENCE)
        except Exception:
            continue

        if loc is None:
            continue

        log_action(img)

        if not image_still_exists(img, loc):
            continue

        x, y = pyautogui.center(loc)

        if img == "1.png":
            y += 30

        pyautogui.moveTo(x, y, duration=0)
        time.sleep(MOVE_DELAY)

        if is_loading():
            return

        if not image_still_exists(img, loc):
            continue

        pyautogui.click()
        time.sleep(CLICK_DELAY)


print("Running (ESC to stop)")

while running:
    find_and_click()
    time.sleep(SCAN_DELAY)

sys.exit(0)
