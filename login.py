# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 16:23:56 2021

@author: lbrin
"""

from abc import ABCMeta, abstractmethod
import argparse
import logging

import bitmex


class Shell():
    """ """
    
    def __init__(self):
        """ """


class ManualControl():
    """ """
    
    def __init__(self):
        """ """
        self.client = None
        
    
    def login(self, public_key, private_key):
        """ """
        logging.info('invoke login of ManualControl')
        self.public_key = public_key
        self.private_key = private_key
        self.client = bitmex.bitmex(api_key=self.public_key,
                                    api_secret=self.private_key)
    
    def get_current_price(self):
        """ """
        logging.info('invoke get_current_price of ManualControl')
        pass
    
    def get_deposit_address(self):
        """ """
        logging.info('invoke get_deposit_address of ManualControl')
        deposit_addr, response = self.client.User.\
            User_getDepositAddress().result()
        return deposit_addr
    

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


class LoginCommand(Command):
    """ """
    
    args_names = ['--public_key', '--private_key']
    
    def execute(self, args_string: str) -> None:
        args = self.arg_parser.parse_args(args_string.split())
        self.manual_control.login(**vars(args))


class GetCurrentPiceCommand(Command):
    """ """
    
    def execute(self, args_string: str) -> None:
        self.manual_control.get_current_price()


class GetDepositAddressCommand(Command):
    """ """
    
    def execute(self, args_string: str) -> None:
        self.manual_control.get_deposit_address()



class Shell:
    """ """
    
    supported_cmds = ('login',
                      'get_current_price', 
                      'get_deposit_address')
    
    def __init__(self):
        """ """
        self.current_controller = ManualControl()
        self.login = LoginCommand(self, self.current_controller)
        self.get_current_price = GetCurrentPiceCommand(
            self, self.current_controller)
        self.get_deposit_address = GetDepositAddressCommand(
            self, self.current_controller)
    
    def run_shell(self):
        """ """
        logging.info('shell is running')
        while True:
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
            return
        if cmd_name == 'login':
            if len(inp_split) < 2:
                print('login requires arguments')
                return
            self.login.execute(unproc_args)
        elif cmd_name == 'get_current_price':
            self.get_current_price.execute(unproc_args)
        elif cmd_name == 'get_deposit_address':
            self.get_deposit_address.execute(unproc_args)
        
        
def main():
    """ """
    shell = Shell()
    shell.run_shell()


if __name__ == '__main__':
    main()

