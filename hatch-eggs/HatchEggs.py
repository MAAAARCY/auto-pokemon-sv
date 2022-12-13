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
        NOW_COUNT = 0
        HATCH_COUNT = 3

        while NOW_COUNT < HATCH_COUNT:
            logger.info('{}回目の孵化厳選を開始します'.format(NOW_COUNT+1))
            await self.hatch_egg()
            await self.button_ctl('x', wait_sec=5.0) #メニューを開く
            await self.button_ctl('a', wait_sec=8.0) #ボックスを選択
            await self.release_pokemon(now_count=NOW_COUNT)
            
            if NOW_COUNT + 1 != HATCH_COUNT:
                await self.get_eggs(now_count=NOW_COUNT)
            
            await self.button_ctl('b', wait_sec=5.0) #ボックスを閉じる
            await self.button_ctl('x', wait_sec=5.0) #メニューを閉じる
            logger.info('{}回目の孵化厳選を終了しました'.format(NOW_COUNT+1))
            NOW_COUNT += 1

    async def hatch_egg(self):
        await self.button_ctl('plus', wait_sec=2.0)

        limit_time = time.time() + 300 #孵化歩数が長いポケモンで4分半だったのでこの数値にした
        notice_time = time.time() + 60

        await self.left_stick('right')
        await self.wait(0.05)
        await self.right_stick('left')
        await self.wait(0.05)

        while time.time() < limit_time:
            await self.button_ctl('a', wait_sec=4.0)
            
            if notice_time < time.time():
                logger.info('あと{}秒です'.format(round(limit_time-notice_time)))
                notice_time += 60

        await self.button_ctl('plus')
        await self.left_stick('center')
        await self.wait(0.05)
        await self.right_stick('center')
        await self.wait(5.0)
    
    async def release_pokemon(self, now_count=0):
        await self.button_ctl('left')
        await self.button_ctl('down')
        await self.button_ctl('minus', wait_sec=1.0)
        
        for n in range(4):
            await self.button_ctl('down')
        
        await self.button_ctl('a')
        await self.button_ctl('up')

        for n in range(now_count+1):
            await self.button_ctl('right')
        
        await self.button_ctl('a')
        await self.wait(3.0)
    
    async def get_eggs(self, now_count=0):
        #await self.button_ctl('x', wait_sec=3.0)
        #await self.button_ctl('a', wait_sec=5.0)
        
        #release_pokemonで右にずれてるので一回分のみ
        await self.button_ctl('right')

        await self.button_ctl('minus', wait_sec=1.0)
        
        for n in range(4):
            await self.button_ctl('down')
        
        await self.button_ctl('a')

        for n in range(now_count+2):
            await self.button_ctl('left')
        
        await self.button_ctl('down')
        await self.button_ctl('a')
        await self.wait(3.0)