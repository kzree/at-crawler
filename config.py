import argparse
from typing import NamedTuple

class Config(NamedTuple):
    name: str
    min: int
    max: int

def init_parser():
    """
    Initializes the parser and the arguments used in the application.
    """
    parser = argparse.ArgumentParser(description="Crawler for Arvutitark website for checking prices")
    parser.add_argument("item_name", type=str, help="Name of the item the program will look for")
    parser.add_argument("-min", type=int, help="Minimum value of item (default: 0)")
    parser.add_argument("-max", type=int, help="Maximum value of item")
    return parser

def check_args_for_errors(parser, parsed_args):
    """
    Checks for false input from the user

    @param parser: Active parser object
    @param parsed_args: User input from the parser
    """
    if (parsed_args.min is not None):
        if (parsed_args.min < 0):
            parser.error("Argument min cannot be negative")
    if (parsed_args.max is not None):
        if(parsed_args.max < parsed_args.min):
            parser.error("Argument max cannot be smaller than min")
        if (parsed_args.max < 0):
            parser.error("Argument max cannot be negative")

def get_application_arguments():
    """
    Gets the application arguments from user input, checks them and returns a Config object.

    @returns config: A NamedTuple containing input from the user. Default values are None or 0.
    """
    parser = init_parser()
    parsed_args = parser.parse_args()
    check_args_for_errors(parser, parsed_args)
    config = Config(
            parsed_args.item_name.replace(" ", "+"), 
            0 if parsed_args.min is None else parsed_args.min, 
            parsed_args.max
            )
    return config
