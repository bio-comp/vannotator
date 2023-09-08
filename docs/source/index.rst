.. Vannatator documentation master file, created by
   sphinx-quickstart on Mon Sep  4 18:42:51 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Vannatator's documentation!
======================================



Introduction
============

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


modules
=======
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
