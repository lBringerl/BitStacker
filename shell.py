# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 17:49:41 2021

@author: lbrin
"""

from abc import ABCMeta, abstractmethod
import argparse
import datetime
import logging
import time

import bitmex

import api_keys
from strategies import Context, Strategy


class ManualControl:
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
        return order


class Shell:
    """ """
    
    supported_cmds = ('init_client',
                      'get_last_quote', 
                      'get_deposit_address',
                      'get_open_orders',
                      'set_limit_order',
                      'exit',
                      'set_strategy',
                      'run_strategy',
                      'get_current_strategy')
    
    def __init__(self, manual_controller: ManualControl, \
                 strategy_context: Context):
        """ """
        self.init_client = InitClientShellCommand(
            self, manual_controller, strategy_context)
        self.get_last_quote = GetLastQuoteShellCommand(
            self, manual_controller, strategy_context)
        self.get_deposit_address = GetDepositAddressShellCommand(
            self, manual_controller, strategy_context)
        self.get_open_orders = GetOpenOrdersShellCommand(
            self, manual_controller, strategy_context)
        self.set_limit_order = SetLimitOrderShellCommand(
            self, manual_controller, strategy_context)
        self.exit = ExitShellCommand(
            self, manual_controller, strategy_context)
        self.set_strategy = SetStrategyShellCommand(
            self, manual_controller, strategy_context)
        self.run_strategy = RunStrategyShellCommand(
            self, manual_controller, strategy_context)
        self.get_current_strategy = GetCurrentStrategyShellCommand(
            self, manual_controller, strategy_context)
    
    def run_shell(self):
        """ """
        logging.info('shell is running')
        self.running = True
        self.init_client.execute(
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
            print(f'Shell command "{cmd_name}" is not supported. '
                  f'Supported commands are: {self.supported_cmds}')
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
        elif cmd_name == 'set_strategy':
            return self.set_strategy.execute(unproc_args)
        elif cmd_name == 'run_strategy':
            return self.run_strategy.execute(unproc_args)
        elif cmd_name == 'get_current_strategy':
            return self.get_current_strategy.execute(unproc_args)
    
    def shell_print(self, data):
        """ """
        print(data)
    
    def shell_exit(self):
        """ """
        self.running = False


class ShellCommand(metaclass=ABCMeta):
    """ """
    
    args_names = []
    
    def __init__(self, shell: Shell, manual_control: ManualControl, \
                 strategy_context: Strategy) -> None:
        self.shell = shell
        self.manual_control = manual_control
        self.strategy_context = strategy_context
        if self.args_names:
            self.arg_parser = argparse.ArgumentParser()
            for arg in self.args_names:
                self.arg_parser.add_argument(arg, type=str)
    
    @abstractmethod
    def execute(self, args_string: str) -> None:
        pass


class InitClientShellCommand(ShellCommand):
    """ """
    
    args_names = ['--public_key', '--private_key']
    
    def execute(self, args_string: str) -> None:
        args = vars(self.arg_parser.parse_args(args_string.split()))
        self.manual_control.init_client(**args)


class GetLastQuoteShellCommand(ShellCommand):
    """ """
    
    def execute(self, args_string: str) -> None:
        price = self.manual_control.get_last_quote()
        self.shell.shell_print(f'Last quote: {price}')


class GetDepositAddressShellCommand(ShellCommand):
    """ """
    
    def execute(self, args_string: str) -> None:
        addr = self.manual_control.get_deposit_address()
        self.shell.shell_print(f'Deposit address: {addr}')


class ExitShellCommand(ShellCommand):
    """ """
    
    def execute(self, args_string: str) -> None:
        self.shell.shell_print('Exit shell')
        self.shell.shell_exit()


class GetOpenOrdersShellCommand(ShellCommand):
    """ """
    
    def execute(self, args_string: str) -> None:
        orders = self.manual_control.get_open_orders()
        self.shell.shell_print(f'Open orders: {orders}')


class SetLimitOrderShellCommand(ShellCommand):
    """ """
    
    args_names = ['--quantity', '--price']
    
    def execute(self, args_string: str) -> None:
        args = vars(self.arg_parser.parse_args(args_string.split()))
        order = self.manual_control.set_limit_order(**args)
        self.shell.shell_print(f'Order set: {order}')


class SetStrategyShellCommand(ShellCommand):
    """ """
    
    args_names = ['--strategy']
    
    def execute(self, args_string: str) -> None:
        args = vars(self.arg_parser.parse_args(args_string.split()))
        args['strategy'] = Context.strategy_type_from_string(args['strategy'])
        self.strategy_context.set_strategy(**args)


class RunStrategyShellCommand(ShellCommand):
    """ """
    
    def execute(self, args_string: str) -> None:
        self.strategy_context.run_strategy()
        

class GetCurrentStrategyShellCommand(ShellCommand):
    """ """
    
    def execute(self, args_string: str) -> None:
        strategy = self.strategy_context.get_strategy()
        self.shell.shell_print(f'Current strategy is: {strategy}')
