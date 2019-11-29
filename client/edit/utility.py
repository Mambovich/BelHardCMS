import logging
import re
from time import perf_counter

from client.edit.log_color import (log_info, log_verbose)


def check_input_str(string: str, title=True) -> str or None:  # TeamRome
    """ pattern: одно-два слова, слова с русскими и английскими буквами,
    апострафами, двойние слова, слова с цыфрами"""
    if re.match("^[a-zA-Zа-яА-Я0-9'-_]{1,100}[ ]?[-]?[a-zA-Zа-яА-Я0-9'-_]{0,100}$", string):
        log_info("\tcheck_input_str(): %s" % string)
        if title:
            return string.title()
        else:
            return string
    else:
        logger_me().error("\tcheck_input_str() Fail: %s" % string)
        return None


def check_telegram(string: str) -> str or None:  # TeamRome
    """ pattern: @tele, @123qwe, @qwe12, @asd11_sd1 """
    if re.match("^[@][a-zA-Zа-яА-Я_0-9]{1,100}$", string):
        log_info("\tcheck_telegram(): %s" % string)
        return string
    else:
        logger_me().error("\tcheck_telegram() Fail: %s" % string)
        return None


def check_home_number(string: str) -> str or None:  # TeamRome
    """ pattern: 12/4, 13-4, 1a, f/2, 5/e, 6-y """
    if re.match("^[0-9a-zA-Zа-яА-Я/-]{1,10}$", string):
        log_info("\tcheck_home_number(): %s" % string)
        return string
    else:
        logger_me().error("\tcheck_home_number() Fail: %s" % string)
        return None


def check_phone(phone: str) -> str or None:  # TeamRome
    """ pattern: +375291234567 """
    if re.match("^[+][0-9]{1,20}$", phone):
        log_info("\tcheck_phone(): %s" % phone)
        return phone
    else:
        logger_me().error("\tcheck_phone() Fail: %s" % phone)
        return None


def try_except(foo):  # TeamRome
    """ Handle exceptions in a selected function = foo_name. """

    def wrapper(*args, **kwargs):
        try:
            return foo(*args, **kwargs)
        except Exception as ex:
            logger_me().exception("Exception in - %s()\n\t%s" % (foo.__name__, ex))
            return None

    return wrapper


def time_it(foo):  # TeamRome
    """ Return the value (in fractional seconds) of a performance counter for a function = foo_name. """

    def wrapper(*args, **kwargs):
        time_0 = perf_counter()
        log_verbose("%s()" % foo.__name__)
        result = foo(*args, **kwargs)
        log_info('\t%s() - OK; TimeIt: %.6f sec.' % (foo.__name__, perf_counter() - time_0))
        return result

    return wrapper


def logger_me():
    # create logger with 'spam_application'
    logger = logging.getLogger('logger_edit_forms')
    logger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('logger_edit_forms.log')
    fh.setLevel(logging.INFO)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
