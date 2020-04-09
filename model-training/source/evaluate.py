"""
cli module
usage: Basic Hello world 
"""
import argparse
from argparse import Namespace, ArgumentParser

import pkg_resources  # part of setuptools
from config import Config
from util.logs import Log
import logging


def setup_parser() -> ArgumentParser:
    """
    setup for argparse cli
    :return:
    """
    parser = argparse.ArgumentParser(description="This script runs the task for model training")

    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging.")

    return parser


def setup_log_config(verbose: bool):

    if verbose:
        Log.base_config(logging.DEBUG)
    else:
        Log.base_config(logging.INFO)



def main():
    """
    main function called from cli
    :return:
    """
    Config.initialize()
    parser = setup_parser()  # get user inputs from command line
    args: Namespace = parser.parse_args()
    setup_log_config(args.verbose)
    logging.info("model traning repo")