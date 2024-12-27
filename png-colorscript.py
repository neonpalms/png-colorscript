# /usr/bin/env python

from PIL import Image
import numpy as np
from pathlib import Path

CONFIG_DIR: Path = Path("~/.config/png-colorscript").expanduser()
IMAGES_DIR: Path = CONFIG_DIR.joinpath("pngs")


def verify_config() -> None:
    """Check to see: 1. if the config dir exists and 2. if there are any PNGs in said folder."""
    global IMAGES_DIR
    run_first_time_config() if not Path.exists(CONFIG_DIR) else None

    import os, os.path

    if (
        len(
            [
                filename
                for filename in os.listdir(IMAGES_DIR)
                if filename.endswith(".png")
            ]
        )
        == 0
    ):
        print(f"There are no PNGs located in ${IMAGES_DIR}; go put some there, dingus.")
        exit(1)


def rgb_to_colored_pixel(r: int, g: int, b: int) -> str:
    """Returns a ▀ character preceded by an escape sequence that changes the rgb color of the terminal."""
    ESC = "\x1b"
    PXL = "▀"
    return f"{ESC}[38;2;{r};{g};{b}m{PXL}"


def reset_console_color():
    """Resets the console color back to normal."""
    print("\x1b[0m")


def print_image_array_to_console(img: Image) -> None:
    """Takes an array of pixels and prints a space for every alpha pixel and a colored character for every other pixel."""
    # TODO Implement
    raise NotImplementedError()


def get_random_image() -> Image:
    """Returns a random image from the config directory."""
    # TODO Implement
    raise NotImplementedError()


def get_image_by_name(img_name: str) -> Image:
    """Returns an image from the config directory by filename."""
    # TODO Implement
    print(img_name)
    raise NotImplementedError()


def get_random_image_from_names(img_names: list[str]) -> Image:
    """Returns a random image from a string list of filenames."""
    # TODO Implement
    print(img_names)
    raise NotImplementedError()


def run_first_time_config() -> None:
    """Initialize the program by creating a .config folder and a folder for images to go."""
    global CONFIG_DIR, IMAGES_DIR
    print(f"Performing first-time set up ...")
    Path.mkdir(CONFIG_DIR)  # Make both directories since they don't exist
    Path.mkdir(IMAGES_DIR)
    print(f"Please put some PNGs to print in ${IMAGES_DIR} then run again!")
    exit(0)


def main() -> None:
    """Entry point to the program."""
    verify_config()

    import argparse

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

    if args.random:
        get_random_image()
    elif args.name:
        get_image_by_name(args.name)
    elif args.random_name:
        names = args.random_name[0].split(",")
        get_random_image_from_names(names)
    else:
        parser.print_help()

    reset_console_color()


# region DEBUG CLEAR SCREEN BEFORE RUNNING ------------
import os

os.system("clear")  # ! DEBUG
# endregion -------------------------------------------


if __name__ == "__main__":
    main()
