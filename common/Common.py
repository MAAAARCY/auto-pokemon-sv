#import pyocr as ocr
#import pyocr.builders
import logging
import asyncio
import time
import cv2

from PIL import Image
from JoycontrolPlugin import JoycontrolPlugin

logger = logging.getLogger(__name__)

DEVICE_ID = 1

CAP_WIDTH = 1920
CAP_HEIGHT = 1080

class Common(JoycontrolPlugin):
    def __init__(self, controller_state, options):
        super().__init__(controller_state, options)
        self.setup_video()
    
    def setup_video(self):
        #カメラのセットアップ
        self.cap = cv2.VideoCapture(DEVICE_ID)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAP_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAP_HEIGHT)
    
    async def get_threshold_img(self, frame, x_point, y_point, x_size, y_size):
        #トリミング
        trim_img = frame[y_point : y_point + y_size, x_point : x_point + x_size]
        #グレースケール化
        gray_img = cv2.cvtColor(trim_img, cv2.COLOR_RGB2GRAY)
        #二値化
        thresh_img = cv2.adaptiveThreshold(gray_img)
        return thresh_img
    """
    async def get_ocr_text(self, thresh_img):
        tools = pyocr.get_available_tools()

        if len(tools) == 0:
            print('OCR tools not found.')
            sys.exit(1)
    """ 
    async def start_picnic(self):
        #メニューを開く
        logger.info('メニューを開きました')
        await self.button_ctl('x', wait_sec=2.0)
        #ピクニックを選択
        logger.info('ピクニックが選択されました')
        await self.button_ctl('down')
        await self.button_ctl('down')
        await self.button_ctl('a', wait_sec=10.0)
        #少し下に歩いてサンドイッチ制作へ
        logger.info('サンドイッチの制作を開始しました')
        await self.down_walking(press_sec=0.5)
        await self.button_ctl('a', wait_sec=3.0)
        await self.button_ctl('a', wait_sec=6.0)
        await self.button_ctl('right')
        await self.button_ctl('down', wait_sec=1.0)
        await self.button_ctl('down', wait_sec=1.0)
        await self.button_ctl('down', wait_sec=1.0)
        await self.button_ctl('a', wait_sec=3.0)
        await self.button_ctl('a', wait_sec=10.0)
    
    async def make_sandwich(self):
        await self.move_hands(tilt_angle=180, move_sec=0.4)
        await self.grab_and_drop_ingredients(tilt_angle=45)
        await self.move_hands(tilt_angle=0, move_sec=0.4)
        await self.grab_and_drop_ingredients(tilt_angle=90)
        await self.move_hands(tilt_angle=0, move_sec=0.4)
        await self.grab_and_drop_ingredients(tilt_angle=135)
        await self.move_hands(tilt_angle=180, move_sec=0.4, wait_sec=5.0)
        #バンズを置く
        await self.button_ctl('a', wait_sec=3.0)
        #ピックを刺す
        await self.button_ctl('a', wait_sec=8.0)
        #食事画面へ移行
        await self.button_ctl('a', wait_sec=25.0)
        #サンドイッチ終了
        await self.button_ctl('a', wait_sec=1.0)
        logger.info('サンドイッチの制作を終了します')
    
    async def grab_and_drop_ingredients(self, tilt_angle=90):
        #具材へ手を運ぶ
        await self.move_hands(tilt_angle=tilt_angle)
        #具材をつかんで落とす
        await self.button_press('a')
        await self.wait(0.5)
        await self.left_stick(angle=tilt_angle+180)
        await self.wait(0.5)
        await self.left_stick('center')
        await self.wait(0.5)
        await self.button_release('a')
        await self.wait(0.5)

    async def move_hands(self, tilt_angle=180, move_sec=0.6, wait_sec=0.5):
        await self.left_stick(angle=tilt_angle)
        await self.wait(move_sec)
        await self.left_stick('center')
        await self.wait(wait_sec)

    async def down_walking(self, press_sec=0.45, wait_sec=0.05):
        await self.left_stick(angle=270)
        await self.wait(press_sec)
        await self.left_stick('center')
        await self.wait(wait_sec)

    async def button_ctl(self, button, press_sec=0.05, wait_sec=0.05):
        await self.button_push(button)
        await self.wait(wait_sec)