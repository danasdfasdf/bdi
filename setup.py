from setuptools import setup

setup(
    name='bdi',
    version='1.0.0',
    py_modules=['bdi'],
    data_files=[('Lib/site-packages', ['postcodes.csv'])],
    install_requires=[
        'pandas>=1.3.0',
        'requests>=2.26.0',
        'pyperclip>=1.8.2',
    ],
    entry_points={
        'console_scripts': [
            'bdi=bdi:main',
        ],
    },
) 