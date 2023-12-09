from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument(
        'Videos',
        nargs='+',
        help='Path de los videos')

args = parser.parse_args()