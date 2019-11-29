import argparse
import configparser

DEFAULT_CONFIG = 'config.ini'

import datetime
from pandas_datareader import get_data_tiingo
import pickle

def settings(args):
    # Settings configuration, defaults can be changed in the config file
    config = configparser.ConfigParser()
    if args.config_file is None:
        config.read(DEFAULT_CONFIG)
    else:
        config.read(args.config_file)

    if args.kapi is None:
        api_key = config['DEFAULT']['tiingoAPI']
    else:
        api_key = args.kapi

    if args.pickle_file is None:
        pickle_path = config['DEFAULT']['picklePath']
    else:
        pickle_path = args.pickle_file

    return api_key, pickle_path


def main():
    # Argument parser for simple settings changes
    parser = argparse.ArgumentParser()
    parser.add_argument('query', help='Search query', nargs='*')
    parser.add_argument('-s', '--start_date', nargs=3, type=int,
                        help='Start date for gathering stock data')
    parser.add_argument('-e', '--end_date', nargs=3, type=int,
                        help='End date for gathering stock data')

    parser.add_argument('-c', '--config_file',
                        help='Path to non-default config file')

    parser.add_argument('-kapi', '--kapi',
                        help='Use a different apu key then the default in config')
    parser.add_argument('-p', '--pickle_file',
                        help='use a different pickle file')

    args = parser.parse_args()

    api_key, pickle_path = settings(args)

    if args.start_date is None:
        start_date = None
    else:
        start_date = datetime.datetime(*map(int, args.start_date))

    if args.end_date is None:
        end_date = None
    else:
        end_date = datetime.datetime(*map(int, args.end_date))

    reader = get_data_tiingo(args.query, api_key=api_key, start=start_date, end=end_date)

    with open(pickle_path, 'wb') as file:
        pickle.dump(reader, file)


if __name__ == '__main__':
    main()
