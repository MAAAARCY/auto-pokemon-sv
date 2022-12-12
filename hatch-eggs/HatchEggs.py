import logging
import time
import sys
import os

from JoycontrolPlugin import JoycontrolPlugin

sys.path.append(os.getcwd() + '/common')
from Common import Common

logger = logging.getLogger(__name__)

class HatchEggs(Common):
    def __init__(self, controller_state, options):
        super().__init__(controller_state, options)

    async def run(self):
        await self.hatch_egg()

    async def hatch_egg(self):
        await self.button_ctl('plus', wait_sec=2.0)

        limit_time = time.time() + 300 #孵化歩数が長いポケモンで4分半だったのでこの数値にした
        notice_time = time.time() + 60

        while time.time() < limit_time:
            await self.left_stick(angle=270)
            await self.wait(3.0)
            await self.left_stick(angle=90)
            await self.wait(3.0)
            await self.button_ctl('a')
            
            if notice_time < time.time():
                logger.info('あと{}秒です'.format(round(limit_time-notice_time)))
                notice_time += 60

        await self.button_ctl('plus')