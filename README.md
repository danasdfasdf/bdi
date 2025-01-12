# BDI (British Deprivation Index) Lookup Tool

A command-line tool to quickly look up ONS stats for any UK postcode or location. Very useful when buying a house and wanting to know more about the area.

## Features

- Look up ONS data using postcodes directly
- Extract location data from Google Maps URLs
- Support for clipboard content (just press Enter)
- Opens three key ONS maps

## Installation

1. Ensure you have Python 3.6+ installed
2. Clone this repository or download the files
3. The postcodes.csv file is required and must be in the same directory as the script. This file is a renamed copy of the [ONS postcode lookup file](https://geoportal.statistics.gov.uk/datasets/068ee476727d47a3a7a0d976d4343c59/about)
4. Run: `pip install .` to install the required dependencies

## Usage

Simply run bdi.py on the command line.

You can then:
- Enter a UK postcode directly (e.g., "CM1 6GN")
- Paste a Google Maps URL
- Press Enter to use a URL from your clipboard

This will open three browser tabs showing different ONS demographic maps for the specified location.

## Requirements

- All requirements will be automatically installed when you run `pip install .`
- The postcodes.csv file is required and must be in the same directory as the script. This file is a renamed copy of the [ONS postcode lookup file](https://geoportal.statistics.gov.uk/datasets/068ee476727d47a3a7a0d976d4343c59/about)

