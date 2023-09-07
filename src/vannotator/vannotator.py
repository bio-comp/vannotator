"""A module for annotating variants

.. module: vannotator
    :platform: Unix, Windows
    :synopsis: Annotate varaints using VEP.
.. moduleauthor:: Mike Hamilton (mike.hamilton7@gmail.com)
"""

from argparse import ArgumentParser, Namespace
from typing import Any
from vcf import Reader, model
from csv import writer
from dataclasses import dataclass, field, asdict
from datetime import datetime

import logging
import utils 
import math

HEADERS = ['chrom', 'pos', 'ref', 'alt', 'depth', 'allele_depth', 'ratio_perc', 'var_type', 'effect', 'minor_allele_freq']
      
    
# Setup parser
def setup_parser() -> Namespace:
    """Sets up and validates arguments

    :return: Arguments if they are valid
    :rtype: Namespace
    
    """
    parser = ArgumentParser(description='Annotate variants from VCF file')
    parser.add_argument('-f', '--file', dest='file', type=str, help='VCF file to annotate', 
                        required=True, action=utils.ValidateInputExists)
    parser.add_argument('-o', '--output', dest='output', type=str, help='output file',
                        required=False, default='output.csv', action=utils.ValidateOutputWriteable)
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', 
                        help='Provides more logging details.', default=False, required=False)
    return parser.parse_args()



@dataclass
class Variant:
    """Immutable container for a variant record
    """
    chrom: str #: The name of the chromosome
    gene: str or None #!:Gene containing the variant, if available
    pos: int #: Position of the variant
    ref: str #: Reference sequence of the variant
    alt: str #: Alternate allele 
    minor: str #: Minor allele, if available
    depth: int #: Total reads mapped to location
    allele_depth: int #: Number of reads mapped to allele
    var_type: str #: Type of variant (insertion, deletion, CNV, ...)
    minor_depth: int #: Number of reads mapped to minor allele, if available
    effect: str #: Coding effect of t
    allele_freq: float = field(init=False, default=None) #: Allele frequency
    minor_allele_freq: float = field(init=False, default=None) #: Minor allele frequency, if available
    ratio_perc: float = field(init=False, default=None) #: Percentage of allele depth vs ref depth
    
    def __post_init__(self):
        """Sets the allele frequecy, the ratio percentage, and if present, the minor allele frequency
        """
        self.allele_freq = self.allele_depth / self.depth
        ref_depth = (self.depth - self.allele_depth - self.minor_depth)
        if ref_depth == 0:
            self.ratio_perc = math.inf
        else:
            self.ratio_perc = self.allele_depth / (self.depth - self.allele_depth - self.minor_depth) * 100
        if self.minor:
            self.minor_allele_freq = self.minor_depth / self.depth


def create_variant(record: model._Record, payload: dict) -> Variant:
    """Creates a Variant instance from a VCF record and a VEP payload

    :param record: VCF record
    :type record: model._Record
    :param payload: VEP payload
    :type payload: dict
    :return: A populated dataclass instance of a variant
    :rtype: Variant
    """
    
    xscript = payload.get('transcript_consequences', [{}])[0]
    var_data = {'chrom': record.CHROM, 'pos': record.POS, 'ref': record.alleles[0], 'alt': record.alleles[1],
                'gene': xscript.get('gene_symbol', ''), 'depth': record.INFO['TC'],
                'allele_depth': record.INFO['TR'][0], 'effect': payload['most_severe_consequence']
                }
    # check if there is more than 1 variant present
    has_minor = len(record.ALT) > 1 
    
    if has_minor:
        var_data['minor'] = record.ALT[-1]
        var_data['minor_depth'] = record.INFO['TR'][-1]
    else:
        var_data['minor'] = ''
        var_data['minor_depth'] = 0
        
    if record.var_type == 'indel':
        var_data['var_type'] = {'ins': 'insertion', 'del': 'deletion', 'unknown': 'indel'}[record.var_subtype]
    elif record.var_type == 'snp':
        var_data['var_type'] = 'SNP'
    elif record.is_sv:
        var_data['var_type'] = 'CNV'
    else:
        var_data['var_type'] = 'Unknown'
    
    return Variant(**var_data)
    
def write_to_csv(items: list, csv_writer: writer) -> None:
    """Writes a row to a CSV file

    :param items: List of column headers
    :type items: list
    :param csv_writer: CSV wirter to write to
    :type csv_writer: writer
    """
    csv_writer.writerow(items)
    
    
def process_file(vcf_reader: Reader, csv_writer: writer, header: list = HEADERS) -> (int, int):
    variants = 0
    n_failed = 0
    write_to_csv(header, csv_writer)
    
    for record in vcf_reader:
        variants += 1
        url = utils.url_builder(record.CHROM, record.INFO['WS'], record.INFO['WE'], record.ALT[0])
        logging.debug(f'Processing record {record}')
        payload = utils.get_payload(url, utils.GET, utils.HEADERS)
        if not payload:
            logging.warn(f'Could not fetch annotations for {record}')
            n_failed += 1
            continue
        variant = create_variant(record, payload[0])
        write_to_csv([asdict(variant)[key] for key in header], csv_writer)
        
    return (variants, n_failed)


def main(args: Namespace) -> None:
    """Main execution

    :param args: Namespace of the parser
    :type args: Namespace
    """
    logging.info('Started')
    logging.info(f'Reading variants from {args.file}')
    logging.info(f'Writing to {args.output}')
    vcf_reader = Reader(open(args.file, 'r'))
    with open(args.output, 'w') as outfile:
        csv_writer = writer(outfile)
        variants, n_failed = process_file(vcf_reader, csv_writer)
        logging.info(f'Processed {variants}, {n_failed} failed to be annotated')
       
    logging.info('Finished')
if __name__ == '__main__':
    args = setup_parser()
    logging_level = logging.INFO
    if args.verbose: 
        logging_level = logging.DEBUG

    # Setup logging
    logging.basicConfig(
        level=logging_level,
        format='%(asctime)s [%(name)s] %(message)s',
        handlers=[
            logging.FileHandler(f'vannotator_{datetime.now(tz=None).strftime("%Y-%m-%d_%H:%M:%S")}.log'),
            logging.StreamHandler()
        ]
    )
    main(args)