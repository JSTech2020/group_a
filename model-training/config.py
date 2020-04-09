"""
config.ini parser file
"""
from configparser import ConfigParser
import os


class Config:
    """
    Interact with configuration variables.
    """

    config_parser = ConfigParser()
    config_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config.ini")

    @classmethod
    def initialize(cls):
        """
        Start config by reading config.ini.
        """
        cls.config_parser.read(cls.config_file_path)

    @classmethod
    def get(cls, env, key):
        """
        Get values from config.ini.
        """
        return cls.config_parser.get(env, key)