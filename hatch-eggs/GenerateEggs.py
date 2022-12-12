import logging
import time
import sys
import os

from JoycontrolPlugin import JoycontrolPlugin

sys.path.append(os.getcwd() + '/common')
from Common import Common

logger = logging.getLogger(__name__)

class GenerateEggs(Common):
    def __init__(self, controller_state, options):
        super().__init__(controller_state, options)
    
    async def run(self):
        await self.prepare_picnic()
        await self.start_picnic()
        await self.make_sandwich()
        await self.wait_hatcheggs()

    async def prepare_picnic(self):
        await self.left_stick(angle=270)
        await self.wait(1.5)
        await self.left_stick('center')
        await self.wait(3.0)
    
    async def wait_hatcheggs(self):
        half_power = self.max_stick_power / 2
        limit_time = time.time() + 1800
        notice_time = time.time() + 60
        #視点を遠目にすることで勝手に画面の向きが変わるのを抑制する
        logger.info('孵化の観察を開始します')
        await self.right_stick('down')
        await self.wait(1.0)
        await self.left_stick('left', power=half_power)
        await self.wait(1.0)
        await self.left_stick('down', power=half_power)
        await self.wait(1.4)
        await self.left_stick('right',power=half_power)
        await self.wait(0.6)
        await self.left_stick('center')
        await self.wait(0.3)

        while time.time() < limit_time:
            await self.button_ctl('a', wait_sec=1.0)

            if notice_time < time.time():
                logger.info('あと{}秒です'.format(round(limit_time-notice_time)))
                notice_time += 60
        
        logger.info('30分経過したので孵化の観察を終了します')