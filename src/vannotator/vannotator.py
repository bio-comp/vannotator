"""Annotates a VCF file using

    :author Mike Hamilton
"""

from argparse import ArgumentParser
from vcf import Reader
from csv import writer
from dataclasses import dataclass, field, asdict
from datetime import datetime
from requests import get, post, HTTPError


import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(message)s',
    handlers=[
        logging.FileHandler(f'vannotator_{datetime.now(format("%Y-%m-%d %H:%M:%S"))}.log'),
        logging.StreamHandler()
    ]
)

# Setup parser
parser = ArgumentParser(description='Annotate variants from VCF file')
parser.add_argument('-f', '--file', type=str, description='VCF file to annotate', required=True)
parser.add_argument('-o', '--output', type=str, description='output file', required=False, default='output.csv')

args = parser.parse_args()



@dataclass(frozen=True, slots=True)
class Variant:
    """Immutable container for a variant record
    """
    gene: str
    pos: int
    ref: str
    alt: str
    depth: int
    allele_freq: float = field(init=False, default=-1)

    
    def __post_init__(self):
        """Sets the ...
        """