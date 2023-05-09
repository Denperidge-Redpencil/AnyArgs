from argparse import ArgumentParser
from configparser import ConfigParser
from typing import Dict, List

from .typestrings import TYPESTRING_BOOLEAN, TYPESTRING_STRING

class Group:
    def __init__(self, argument_parser: ArgumentParser, config_parser: ConfigParser, group_name: str) -> None:
        self.argument_parser = argument_parser
        self.arg_group = self.argument_parser.add_argument_group(group_name)
        
        self.config_parser = config_parser
        self.conf_group = group_name
        self.config_parser.add_section(self.conf_group)
        
        self.defaults = dict()

    @property
    def args(self):
        """Get argument_parser args"""
        return self.argument_parser.parse_args()
        

    def add_argument(self, 
                     name: str, 
                     typestring: str=TYPESTRING_STRING, 
                     help_text: str="", 
                     cli_flags: List = [], 
                     default: any = None):
        """
        Name should be human readable

        
        """
        

        self.arg_group.add_argument(*cli_flags,
                                    dest=name,
                                    help=help_text)
    
        if default is not None:
            self.defaults[name.lower()] = default

        return self

    

    def _get_conf_value(self, arg_id: str):
        return self.config_parser[self.conf_group][arg_id] if arg_id in self.config_parser[self.conf_group] else None

    def _get_argparse_value(self, arg_id: str):
        args = self.args
        return getattr(args, arg_id) if hasattr(args, arg_id) else None


    def get_argument(self, human_readable_name: str):
        """Gets the arg, whether it be from the config file or CLI"""
        # Get the value from cli if defined. Cli > conf
        value = self._get_argparse_value(human_readable_name.lower())
        # If it's undefined in the CLI, check if conf can be used
        if value is None:
            value = self._get_conf_value(human_readable_name.lower())

        if value is None:
            value = self.defaults[human_readable_name.lower()]

        if False:
            # If it should be saved, do that
            #conf[section_id][value_id] = str(value)
            pass
            
        return value
