"""
logger config file
"""
import logging


class Log:
    """
    logging instance
    """

    @classmethod
    def base_config(cls, level=logging.INFO):
        """
        setup config for logger if verbose set to debug
        :param name:
        :param level:
        """
        logging.basicConfig(
            level=level,
            format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
            handlers=[logging.StreamHandler()],
        )