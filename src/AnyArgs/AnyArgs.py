from argparse import ArgumentParser
from configparser import ConfigParser
from dotenv import load_dotenv
from os import environ, getcwd
from os.path import exists, join
from glob import glob
from typing import Dict, List, Union
from pathlib import Path

from .Group import Group


def _glob_from_cwd(glob_string: str):
    cwd = getcwd()
    return glob(join(cwd, glob_string))

class AnyArgs:
    """A class to allow args to be configured through .conf, .env, env variables OR """
    def __init__(self) -> None:
        self._argument_parser = ArgumentParser()
        self._config_parser = ConfigParser()
        self._env = environ

        self.groups: Dict[str, Group] = dict()


    """GROUP & ARG DEFINITIONS"""
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
    
    def get_group(self, group_name) -> Union[Group, None]:
        print(self.groups)
        print(group_name)
        print("---")
        return self.groups.get(group_name, None)

    def get_argument(self, group_name, argument_name):
        group = self.get_group(group_name)
        if group is not None:
            return group.get_argument(argument_name)
        else:
            return None
    

    """ARG LOADING"""
    def _load_conf_file(self, filepath):
        self._config_parser.read(filepath)
    
    def _load_env_file(self, filepath):
        load_dotenv(filepath)

    def _determine_args_type_and_load(self, filepath):
        filepath = Path(filepath)
        filename = filepath.name.lower()
        if filename.endswith("conf"):
            self._load_conf_file(filepath)
        elif filename.startswith(".env"):
            self._load_env_file(filepath)
            

    @property
    def _load_argument_parser(self):
        """Get argument_parser args"""
        return self.argument_parser.parse_args()
        

    def load_args(self, load_from_cwd = True, filepaths: Union[str, List[str]]= []):
        """Load data from passed file paths, if they exist"""
        if isinstance(filepaths, str):
            filepaths = [filepaths]
        

        if load_from_cwd:
            filepaths += _glob_from_cwd("*.conf")
            filepaths += _glob_from_cwd(".env*")

        for filepath in filepaths:
            if exists(filepath):
                self._determine_args_type_and_load(filepath)
        

            

            
            
            

