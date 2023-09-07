"""Handles API requests

    moduleauthor: Mike Hamilton
"""
import requests
from tenacity import retry, stop, wait
from typing import List
from argparse import ArgumentParser, Namespace, Action
from collections.abc import Sequence
from pathlib import Path
from os import access, W_OK, path

import logging
logger = logging.getLogger(__name__)

POST = 'POST'
GET = 'GET'
BASE_URL = 'https://rest.ensembl.org/vep/homo_sapiens/region/'
HEADERS = {'Content-Type': 'application/json',
          'hgvs': 'true', 'CADD': 'true', 'pick': 'true', 'LoF': 'true'}

# Settings for retrying functions
RETRY_SETTINGS = {
    'wait': wait.wait_random_exponential(multiplier=1.0, exp_base=2),
    'stop': stop.stop_after_attempt(10)
}

@retry(RETRY_SETTINGS)
def get_payload(url: str, action: str, headers: dict = HEADERS) -> List or None:
    """Gets the payload for the provided request

    :param url: URL of endpoint
    :type url: str
    :param action: GET or POST
    :type action: str
    :param headers: Headers for the request
    :type headers: dict
    :return: List of JSON records
    :rtype: List or None
    """
    logging.debug(f'{action} request to {url}')
    if action  == GET:  
        response = requests.get(url, headers=headers)
    elif action == POST:
        response = requests.post(url, headers=headers)
    else:
        logging.warning(f'{action} is not supported')
        return None
    logging.debug('Recieved status {response.status_code}')
    if response.status_code == 200:
        return response.json()
        
def url_builder(chrom: int, start: int, end: int, variant: str = HEADERS) -> str:
    """Builds the URL to query variant

    :param start: _description_
    :type start: int
    :param end: _description_
    :type end: int
    :param chrom: _description_
    :type chrom: int
    :return: _description_
    :rtype: str
    """
    return ''.join([BASE_URL, f'{chrom}:{start}-{end}/{variant}'])


class Writable_Dir_Exception(Exception):
    """Raised if a directory does not exist or is unwritable

    :param Exception: Default exception class
    :type Exception: Exeption
    """
    
    def __init__(self, dir_path: str):
        """Constructor for writable_dir_exception

        :param dir_path: Directory that is not writable or does not exist
        :type dir_path: str
        """
        self.dir_path = dir_path
        self.message = f'Directory {dir_path} does not exist or is unwritable'
        
        
class ValidateInputExists(Action):
    """Validate if input file exists

    :param Action: Inherited class for to check arguments when argument is added
    :type Action: args.Action
    """
    def __call__(self, parser: ArgumentParser, 
                 namespace: Namespace, values: str or list or None, 
                 option_string: str or None = None) -> None:
        """Checks if the input file is accessible

        :param parser: Current parser state
        :type parser: ArgumentParser
        :param namespace: Namespace of arguments
        :type namespace: Namespace
        :param values: The value to check
        :type values: str or Sequence[Any] or None
        :param option_string: Options if present, defaults to None
        :type option_string: str or None, optional
        :raises FileNotFoundError: Raised if input file is not accessible
        """
        if not Path(values).is_file:
            raise FileNotFoundError
        setattr(namespace, self.dest, values)
        
class ValidateOutputWriteable(Action):
    """Validate if output file/dir is writeable

    :param Action: Inherited class for to check arguments when argument is added
    :type Action: args.Action
    """
    def __call__(self, parser: ArgumentParser, 
                 namespace: Namespace, values: str or list or None, 
                 option_string: str or None = None) -> None:
        """_summary_

        :param parser: Current parser state
        :type parser: ArgumentParser
        :param namespace: Namespace of arguments
        :type namespace: Namespace
        :param values: The directory to test if it is writable
        :type values: str or Sequence[Any] or None
        :param option_string: Options if present, defaults to None
        :type option_string: str or None, optional
        :raises Writable_Dir_Exception: Raised if directory is not writeable
        """
        
        if len(path.split(values)[0]) == 0:
            values = './' + values
        if not access(path.dirname(values), W_OK):
            raise Writable_Dir_Exception(values)
        setattr(namespace, self.dest, values)
