from setuptools import setup

setup(
    name='datadownloader',
    version='1.1',
    packages=[
        'datadownloader'
    ],
    install_requires=[
        'requests',
        'tqdm',
        'paramiko'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-mock',
    ],

    author='Pamin Rangsikunpum',
    description='A program that can be used to download data from multiple sources and protocols to local disk.',
    entry_points={
        'console_scripts': [
            'datadownloader = datadownloader.cli:main_cli',
        ],
    },
)
