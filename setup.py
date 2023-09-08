# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vannotator']

package_data = \
{'': ['*']}

install_requires = \
['PyVCF>=0.6.8,<0.7.0',
 'Sphinx>=7.2.5,<8.0.0',
 'dataclasses>=0.8,<0.9',
 'tenacity>=8.2.3,<9.0.0']

setup_kwargs = {
    'name': 'vannotator',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'bio-comp',
    'author_email': 'mike.hamilton7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.6.13',
}


setup(**setup_kwargs)

