# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 16:12:11 2021

@author: lbrin
"""

import asyncio

import websockets


async def hello():
    uri = 'ws://localhost:8080'
    async with websockets.connect(uri) as websocket:
        await websocket.send('Hello world!')
        await websocket.recv()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(hello())
    print('Done')
    while 1:
        pass
    