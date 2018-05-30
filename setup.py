from setuptools import setup, find_packages

requires = [
    'selenium',
    'configparser'
]

setup(
    name='automate-ticket-buy',
    version='0.0.1',
    description='Some automation for the lazy people',
    author="Jake",
    author_email="vandongenjake@gmail.com",
    packages=find_packages(),
    install_requires=requires
)
