# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 16:23:56 2021

@author: lbrin
"""


import bitmex


if __name__ == '__main__':
    print('Dummy log in and get deposit address')
    public_api_key = input('Public API key: ')
    private_api_key = input('Private API key: ')
    client = bitmex.bitmex(api_key=public_api_key,
                           api_secret=private_api_key)
    deposit_addr, response = client.User.User_getDepositAddress().result()
    print('Deposit BTC address: ', deposit_addr)
    
    
