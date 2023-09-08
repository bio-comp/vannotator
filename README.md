# vannotator

## Introduction
This program annotates a VCF file using VEP. Given a VCF file, a CSV is generated containing the following fields:

1. **chrom**: The chromosome containing the variant.
2. **pos**: The position within the chromosome containing of the variant.
3. **ref**: The reference sequence of the variant.
4. **alt**: The alternate sequence of the variant.
5. **depth**: The depth, or total coverage of the region in scope.
6. **allele_depth**: The depth of the allele.
7. **ratio_perc**: The percentage of the reads that map to the variant vs those that map to the reference.
8. **var_type**: The type of the variant, i.e. SNP, insertion, deletion, CNV, etc.
9. **effect**: The coding effect of the variant, i.e. protein coding, intron variant, etc.
10. **minor_allele_freq**: The minor allele frequency, if present.

## Installation
This software was implemented to support both Anaconda and Poetry paradigms. 

## Brief Synopsis
Using a single HTTPS session for RESTful API calls, multiple requests are sent to annotate each variant in a VCF file