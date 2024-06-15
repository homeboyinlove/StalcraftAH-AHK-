import mss.tools
import pytesseract
from PIL import Image
import json
import time
import pyautogui
import os
import ahk
import cv2
import numpy as np

pyautogui.FAILSAFE = False
time.sleep(3)

# Function to detect colors in a specified area
def detect_colors_in_area(left, top, width, height):
    with mss.mss() as sct:
        monitor = {"left": left, "top": top, "width": width, "height": height}
        sct_img = sct.grab(monitor)

        # Convert the screenshot to a NumPy array
        screenshot_np = cv2.cvtColor(np.array(sct_img), cv2.COLOR_RGB2BGR)

        # Convert the image to HSV color space
        hsv_image = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2HSV)

        # Define color thresholds
        color_thresholds = {
            'white': ((0, 0, 200), (180, 30, 255)),
            'blue': ((100, 50, 50), (130, 255, 255)),
            'green': ((40, 50, 50), (80, 255, 255)),
            'yellow': ((20, 100, 100), (40, 255, 255)),
            'red': ((0, 50, 50), (10, 255, 255)),
            'purple': ((130, 50, 50), (160, 255, 255)),
        }

        detected_colors = []

        # Detect colors in the specified area
        for color_name, (lower_bound, upper_bound) in color_thresholds.items():
            mask = cv2.inRange(hsv_image, np.array(lower_bound), np.array(upper_bound))
            result = cv2.bitwise_and(screenshot_np, screenshot_np, mask=mask)
            average_color = cv2.mean(result)[:3]

            # Check if the average color is non-zero (color detected)
            if any(average_color):
                detected_colors.append((color_name, average_color))

        # Return the detected colors
        return detected_colors
def screen(monitor):
    with mss.mss() as sct:
        output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        return output

def main():
    with open("sc_prices.json", encoding="utf-8") as file:
        sc_prices = json.load(file)
    print(sc_prices)

    while True:
        pyautogui.moveTo(x=1798, y=440)
        ahk.run_script("""
         PostMessage, 0x201, 0x00000000, 0x01f0010f, , STALCRAFT ; Down
           sleep, 5
           PostMessage, 0x202, 0x00000000, 0x01f0010f, , STALCRAFT ; UP
        """)
        time.sleep(0.01)

        # Call detect_colors_in_area after taking a screenshot
        detected_colors = detect_colors_in_area(left=1235, top=515, width=275, height=25)

        # Print the detected colors
        print("Detected Colors:", detected_colors)

        # Check if the 'white' color is detected
        if any(color_name == 'white' for color_name, _ in detected_colors):
            print("White color detected. Perform your actions here.")

        monitor = {"top": 515, "left": 1235, "width": 275, "height": 25}
        screen(monitor)
        detected_colors = detect_colors_in_area(left=1235, top=515, width=275, height=25)
        img = Image.open(r'sct-380x925_185x30.png')
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        name = pytesseract.image_to_string(img, lang='rus+eng')
        name_final = name.strip()
        print(name_final)

        monitor = {"top": 525, "left": 1660, "width": 185, "height": 50}
        screen(monitor)
        img = Image.open('sct-390x1235_130x35.png')
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        price = pytesseract.image_to_string(img, lang='rus')
        word = price.strip()
        if word != '':
            hlp = ''
            for i in word:
                if i.isdigit():
                    hlp += i
            price_final = int(hlp)
            print(int(hlp))
            if name_final in sc_prices.keys():
                print('- Проверка цены..')
                if price_final <= int(sc_prices[name_final]):
                    pyautogui.moveTo(x=1732, y=540)
                    os.system('1buy.ahk')
                    time.sleep(0.4)
                    pyautogui.moveTo(x=1765, y=586)
                    os.system('2buy.ahk')
                    time.sleep(0.4)
                    print('- Покупаю..')
            else:
                print('- Не подходит/Отмена')

        else:
            print(word)

if __name__ == "__main__":
    main()
