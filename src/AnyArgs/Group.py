from argparse import ArgumentParser
from configparser import ConfigParser
from typing import Dict, List
from os import environ
from re import findall, RegexFlag

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
        
        # If no CLI flags are defined, auto generate
        if len(cli_flags) < 1:
            # e.g. -
            short_flag = "-" + "".join(findall(r"^\S|[ -]\S", name.lower()))
            long_flag = "--" + name.lower().replace(" ", "-")
            cli_flags += [short_flag, long_flag]

        try:
            self.arg_group.add_argument(*cli_flags,
                                        dest=name,
                                        help=help_text)
        except ValueError as e:
            print("[ERR] ValueError raised when adding argument. Double check that you're not adding duplicate cli_flags")
            raise e
        
        # If a default is defines, save it
        if default is not None:
            self.defaults[name.lower()] = default

        return self

    

    def _get_conf_value(self, arg_id: str):
        return self.config_parser[self.conf_group][arg_id] if arg_id in self.config_parser[self.conf_group] else None

    def _get_argparse_value(self, arg_id: str):
        args = self.args
        return getattr(args, arg_id) if hasattr(args, arg_id) else None

    def _get_env_value(self, arg_id: str):
        return environ.get(arg_id)


    def get_argument(self, human_readable_name: str):
        """
        Gets the arg, no matter where it comes from

        Priority:
        - Highest: CLI arg
        - Middle: env variable/.env
        - Lower: conf file
        - Fallback: default
        """

        # CLI arg
        value = self._get_argparse_value(human_readable_name.lower())
        # env variable/.env
        if value is None:
            value = self._get_env_value(human_readable_name)
        # conf file
        if value is None:
            value = self._get_conf_value(human_readable_name)
        # default
        if value is None:
            value = self.defaults.get(human_readable_name.lower(), None)

        if False:
            # If it should be saved, do that
            #conf[section_id][value_id] = str(value)
            pass
            
        return value
