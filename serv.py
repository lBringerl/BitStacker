# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 16:56:11 2021

@author: lbrin
"""

import asyncio

import websockets


async def echo(websocket, path):
    async for msg in websocket:
        await websocket.send(message=msg)
        print(msg)
        
start_server = websockets.serve(echo, 'localhost', 8080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
