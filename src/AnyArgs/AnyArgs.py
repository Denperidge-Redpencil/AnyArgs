from argparse import ArgumentParser
from configparser import ConfigParser
from dotenv import load_dotenv
from os import environ
from typing import Dict, List


from .Group import Group




class AnyArgs:
    """A class to allow args to be configured through .conf, .env, env variables OR """
    def __init__(self) -> None:
        self._argument_parser = ArgumentParser()
        self._config_parser = ConfigParser()
        self._env = environ

        self.groups: Dict[str, Group] = dict()

    def add_group(self, group_name):
        """"""
        group = Group(self._argument_parser, self._config_parser, group_name)
        self.groups[group_name] = group

        return group

    def add_argument(self, 
                     group_name:str, 
                     argument_name: str, 
                     typestring: str="", 
                     help_text: str="", 
                     cli_flags=[], 
                     default=None):
        return self.groups[group_name].add_argument(
            name=argument_name, 
            typestring=typestring, 
            help_text=help_text, 
            cli_flags=cli_flags,
            default=default)

