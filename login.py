# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 16:23:56 2021

@author: lbrin
"""

from abc import ABCMeta, abstractmethod
import argparse
import datetime
import logging
import time

import bitmex

import api_keys


class Shell:
    """ """
    
    supported_cmds = ('init_client',
                      'get_last_quote', 
                      'get_deposit_address',
                      'get_open_orders',
                      'set_limit_order',
                      'exit')
    
    def __init__(self):
        """ """
        self.current_controller = ManualControl()
        self.init_client = InitClientCommand(self, self.current_controller)
        self.get_last_quote = GetLastQuoteCommand(
            self, self.current_controller)
        self.get_deposit_address = GetDepositAddressCommand(
            self, self.current_controller)
        self.get_open_orders = GetOpenOrdersCommand(
            self, self.current_controller)
        self.set_limit_order = SetLimitOrderCommand(
            self, self.current_controller)
        self.exit = ExitCommand(self, self.current_controller)
    
    def run_shell(self):
        """ """
        logging.info('shell is running')
        self.running = True
        exit_code = self.init_client.execute(
            f'--public_key {api_keys.PUBLIC_KEY} '
            f'--private_key {api_keys.PRIVATE_KEY}')
        while self.running:
            self.run_cmd(input('>> '))
    
    def run_cmd(self, inp):
        """ """
        inp_split = inp.split(' ', 1)
        cmd_name = inp_split[0]
        unproc_args = ''
        if len(inp_split) > 1:
            unproc_args = inp_split[1] 
        if cmd_name not in self.supported_cmds:
            print(f'Command "{cmd_name}" is not supported. Supported commands'
                  f'are: {self.supported_cmds}')
            return 0
        elif cmd_name == 'get_last_quote':
            return self.get_last_quote.execute(unproc_args)
        elif cmd_name == 'get_deposit_address':
            return self.get_deposit_address.execute(unproc_args)
        elif cmd_name == 'get_open_orders':
            return self.get_open_orders.execute(unproc_args)
        elif cmd_name == 'set_limit_order':
            return self.set_limit_order.execute(unproc_args)
        elif cmd_name == 'exit':
            return self.exit.execute(unproc_args)
    
    def shell_print(self, data):
        """ """
        print(data)
    
    def shell_exit(self):
        """ """
        self.running = False


class ManualControl():
    """ """
    
    def __init__(self):
        """ """
        self.client = None
        
    def init_client(self, public_key, private_key):
        """ """
        logging.debug('invoke init_client of ManualControl')
        self.client = bitmex.bitmex(api_key=public_key, api_secret=private_key)
    
    def get_last_quote(self):
        """ """
        logging.debug('invoke get_last_quote of ManualControl')
        result = None
        cur_timestamp = time.time()
        cur_time = datetime.datetime.fromtimestamp(cur_timestamp,
                                                   tz=datetime.timezone.utc)
        result_lst, response = self.client.Quote.Quote_get(
            symbol='XBTUSD',
            count=1,
            reverse=True,
            endTime=cur_time).result()
        if result_lst:
            result = result_lst[0]
        return result
    
    def get_deposit_address(self):
        """ """
        logging.debug('invoke get_deposit_address of ManualControl')
        deposit_addr, response = self.client.User.\
            User_getDepositAddress().result()
        return deposit_addr
    
    def get_open_orders(self):
        """ """
        logging.debug('invoke get_open_orders of ManualControl')
        orders, response = self.client.Order.Order_getOrders(
            filter='{"open":true}',
            symbol='XBTUSD',
            count=100).result()
        return orders
    
    def set_limit_order(self, quantity, price):
        """ """
        logging.debug('invoke set_limit_order of ManualControl')
        order, response = self.client.Order.Order_new(
            symbol='XBTUSD',
            orderQty=quantity,
            price=price,
            ordType='Limit').result()


class Command(metaclass=ABCMeta):
    """ """
    
    args_names = []
    
    def __init__(self, shell: Shell, manual_control: ManualControl) -> None:
        self.shell = shell
        self.manual_control = manual_control
        if self.args_names:
            self.arg_parser = argparse.ArgumentParser()
            for arg in self.args_names:
                self.arg_parser.add_argument(arg, type=str)
    
    @abstractmethod
    def execute(self, args_string: str) -> None:
        pass


class InitClientCommand(Command):
    """ """
    
    args_names = ['--public_key', '--private_key']
    
    def execute(self, args_string: str) -> None:
        args = self.arg_parser.parse_args(args_string.split())
        self.manual_control.init_client(**vars(args))


class GetLastQuoteCommand(Command):
    """ """
    
    def execute(self, args_string: str) -> None:
        price = self.manual_control.get_last_quote()
        self.shell.shell_print(f'Last quote: {price}')


class GetDepositAddressCommand(Command):
    """ """
    
    def execute(self, args_string: str) -> None:
        addr = self.manual_control.get_deposit_address()
        self.shell.shell_print(f'Deposit address: {addr}')
        
        
class ExitCommand(Command):
    """ """
    
    def execute(self, args_string: str) -> None:
        self.shell.shell_print('Exit shell')
        self.shell.shell_exit()


class GetOpenOrdersCommand(Command):
    """ """
    
    def execute(self, args_string: str) -> None:
        orders = self.manual_control.get_open_orders()
        self.shell.shell_print(f'Open orders: {orders}')


class SetLimitOrderCommand(Command):
    """ """
    
    args_names = ['--quantity', '--price']
    
    def execute(self, args_string: str) -> None:
        args = self.arg_parser.parse_args(args_string.split())
        order = self.manual_control.set_limit_order(**vars(args))


def main():
    """ """
    shell = Shell()
    shell.run_shell()
    
    return 0


if __name__ == '__main__':
    main()



