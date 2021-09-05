# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 15:46:39 2021

@author: lbrin
"""

from abc import ABCMeta, abstractmethod
from typing import Union


class Strategy(metaclass=ABCMeta):
    """ """
    
    @abstractmethod
    def run(self) -> None:
        pass


class DummyStrategy(Strategy):
    """ """
    
    def __init__(self):
        """ """
        print('Init dummy strategy')
    
    def run(self) -> None:
        """ """
        print('Run dummy strategy')


class Context:
    """ """
    
    supported_strategies = ('dummy',)
    
    def __init__(self):
        """ """
        self._strategy = None
    
    @classmethod
    def strategy_type_from_string(cls, strategy_name: str) -> \
        Union[Strategy, None]:
        """ """
        if strategy_name not in cls.supported_strategies:
            print(f'Strategy "{strategy_name}" is not supported. '
                  f'Supported strategies are: {cls.supported_strategies}')
            return None
        if strategy_name == 'dummy':
            return DummyStrategy
        
    def set_strategy(self, strategy: Strategy):
        """ """
        self._strategy = strategy()
    
    def run_strategy(self):
        """ """
        self._strategy.run()
    
    def get_strategy(self):
        """ """
        return self._strategy
    
