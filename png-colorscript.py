#/usr/bin/env python

import argparse
from PIL import Image
import numpy as np

import jsonschema
import commentjson as jsonc


def parse_config() -> None:
    # TODO Implement
    raise NotImplementedError()


def print_image_array_to_console(img_arr: np.array) -> None:
    # TODO Implement
    raise NotImplementedError()


def get_random_image() -> np.array:
    # TODO Implement
    raise NotImplementedError()


def get_image_by_name(img_name: str) -> np.array:
    # TODO Implement
    print(img_name)
    raise NotImplementedError()


def get_random_image_from_names(img_names: list[str]) -> np.array:
    # TODO Implement
    print(img_names)
    raise NotImplementedError()


def run_first_time_config() -> None:
    # TODO Implement
    raise NotImplementedError()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="png-colorscripts",
        description="CLI utility that prints out unicode images from PNGs located in a configurable directory",
        usage="png-colorscripts [OPTION] [NAME(S)]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
    )

    parser.add_argument(
        "-h", "--help", action="help", help="Show this help message and exit"
    )
    parser.add_argument(
        "-r",
        "--random",
        action="store_true",
        help="Print a random PNG from configured directory",
    )
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        nargs=1,
        help="Print a PNG by name from configured directory; do not include file-type",
    )
    parser.add_argument(
        "-rn",
        "--random-name",
        type=str,
        nargs=1,
        help="Print a random PNG by name from a list of names, comma-separated WITHOUT whitespace or file-types (𝓮𝓰 'image1,image_2,image-3')",
    )

    args = parser.parse_args()

    parse_config()

    if args.random:
        get_random_image()
    elif args.name:
        get_image_by_name(args.name)
    elif args.random_name:
        names = args.random_name.split(",")
        get_random_image_from_names(names)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

