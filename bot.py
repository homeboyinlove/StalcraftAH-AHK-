import mss.tools
import pytesseract
from PIL import Image
import json
import time
import pyautogui
import os
import ahk
pyautogui.FAILSAFE=False

time.sleep(5)
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
        time.sleep(0.1)

        monitor = {"top": 515, "left": 1235, "width": 275, "height": 25}
        screen(monitor)
        img = Image.open(r'sct-515x1235_275x25.png')
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        name = pytesseract.image_to_string(img, lang='rus+eng')
        name_final = name.strip()
        print(name_final)

        monitor = {"top": 525, "left": 1660, "width": 185, "height": 50}
        screen(monitor)
        img = Image.open('sct-525x1660_185x50.png')
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
