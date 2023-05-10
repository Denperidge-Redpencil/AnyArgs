from argparse import ArgumentParser
from configparser import ConfigParser
from typing import Dict, List
from os import environ
from re import findall, sub

from .argtypes import ARGTYPE_BOOLEAN, ARGTYPE_STRING

def conf_id_from_string(name: str):
    
    #words = findall(r"[a-zA-Z]*", name)
    #id = ""
    #for word in words:
     #   id += word.capitalize()
    return "".join(findall("[a-zA-Z]*", name))
    

class Group:
    def __init__(self, argument_parser: ArgumentParser, config_parser: ConfigParser, group_name: str) -> None:
        self.argument_parser = argument_parser
        self.arg_group = self.argument_parser.add_argument_group(group_name)
        
        self.config_parser = config_parser
        self.conf_group = group_name
        self.config_parser.add_section(self.conf_group)

        self.cli_flags = ["-h"]
        self.set_arg_names = []
        
        self.defaults = dict()

    @property
    def argparse_args(self):
        """Get argument_parser args"""
        return self.argument_parser.parse_args()
        

    def add_argument(self, name: str, 
                     typestring: str=ARGTYPE_STRING, 
                     help_text: str="", 
                     cli_flags: List = [], 
                     default: any = None):
        """
        Name should be human readable

        
        """
        self.set_arg_names.append(name)
        # simply using cli_flags or flags = cli_flags breaks it idk who cares
        flags = [flag for flag in cli_flags]
        if typestring == ARGTYPE_STRING:
            action = None
        if typestring == ARGTYPE_BOOLEAN:
            action = "store_true"
            if default is None:
                default = False

        
        
        # If no CLI flags are defined, auto generate
        if len(flags) < 1:
            # e.g. -
            first_letters_dasherised = "".join(findall(r"^[a-z]|(?<=[^a-z])[a-z]", name.lower()))
            only_letters = "".join(findall(r"[a-z ]", name.lower()))
            
            short_flag = "-" + first_letters_dasherised
            long_flag = "--" + only_letters.replace(" ", "-")

            if short_flag not in self.cli_flags and typestring != ARGTYPE_BOOLEAN:
                flags.append(short_flag)
            if long_flag not in self.cli_flags:
                flags.append(long_flag)
            

        try:
            self.arg_group.add_argument(*flags,
                                        dest=name,
                                        action=action,
                                        help=help_text,
                                        default=None)  # Set Default none, as defaults are handled by AnyArgs
        
            self.cli_flags += flags
        except ValueError as e:
            print("[ERR] ValueError raised when adding argument. Double check that you're not adding duplicate cli_flags")
            raise e
        
        # If a default is defines, save it
        if default is not None:
            self.defaults[name.lower()] = default

        return self



    def _get_conf_value(self, arg_id: str):
        arg_id = conf_id_from_string(arg_id)
        return self.config_parser[self.conf_group][arg_id] if arg_id in self.config_parser[self.conf_group] else None

    def _set_conf_value(self, arg_id: str, value: any):
        arg_id = conf_id_from_string(arg_id)
        print(arg_id)
        value = str(value)
        self.config_parser.set(self.conf_group, arg_id, value)

    def _get_argparse_value(self, arg_id: str):
        args = self.argparse_args
        return getattr(args, arg_id) if hasattr(args, arg_id) else None

    def _get_env_value(self, arg_id: str):
        return environ.get(arg_id, None)


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
        value = self._get_argparse_value(human_readable_name)
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
