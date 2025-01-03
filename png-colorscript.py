# /usr/bin/env python

import sys
import random
from PIL import Image
from pathlib import Path
import configparser

CONFIG_DIR: Path = Path("~/.config/png-colorscript/").expanduser()
CONFIG_FILENM: str = "pngs.conf"

PNGS_PATH: Path = None
ALL_PNGS_FOUND_IN_PATH: list[str] = []


def load_config() -> None:
    """
    Load the settings from the config file into the global constants.
    """
    global CONFIG_DIR, CONFIG_FILENM, PNGS_PATH, ALL_PNGS_FOUND_IN_PATH
    
    config_path = CONFIG_DIR.joinpath(CONFIG_FILENM)
    config = configparser.ConfigParser()
    if (not Path.exists(CONFIG_DIR) or not Path.exists(config_path)):
        run_first_time_config()
    else:
        config.read(config_path)
        PNGS_PATH = Path(f"{config['DEFAULT'].get('PNGS_LOCATION')}").expanduser()

    import os, os.path

    os.chdir(PNGS_PATH)
    for filename in os.listdir("."):
        ALL_PNGS_FOUND_IN_PATH.append(filename) if filename.endswith(".png") else None

    if len(ALL_PNGS_FOUND_IN_PATH) == 0:
        print(f"There are no PNGs located in ${PNGS_PATH}; go put some there, dingus.")
        sys.exit(1)


def reset_console_color():
    """Resets the console color back to normal."""
    print("\x1b[0m")


class Color:
    r: int
    g: int
    b: int
    a: int

    def __init__(self, rgba: list[int]):
        self.r, self.g, self.b, self.a = rgba

    def __str__(self):
        return f"{self.r};{self.g};{self.b}"


def print_png_to_console(png: Image) -> None:
    """Prints a PNG image to the console using colored characters based on RGBA values."""
    ALPHA_CUTOFF = 128  # Threshold below which alpha is considered fully transparent
    ESC = "\x1b"
    RES = "\x1b[0m"
    TOP_PXL_CH = "▀"
    BTM_PXL_CH = "▄"

    out = ""  # The output string to be printed

    for y in range(0, png.height, 2):  # Process two rows at a time (top and bottom)
        for x in range(png.width):
            # For every two rows, get the top & bottom pixel colors
            top_color = Color(png.getpixel((x, y)))
            btm_color = Color(png.getpixel((x, y + 1))) if y + 1 < png.height else None

            # If both pixels are transparent, print a space
            if top_color.a < ALPHA_CUTOFF and (
                btm_color is None or btm_color.a < ALPHA_CUTOFF
            ):
                out += " "
            else:
                # Handle the bottom pixel first if it exists and is not transparent
                if btm_color and btm_color.a >= ALPHA_CUTOFF:
                    out += f"{ESC}[38;2;{btm_color}m"  # Set bottom pixel color
                    if top_color.a >= ALPHA_CUTOFF:
                        out += (
                            f"{ESC}[48;2;{top_color}m"  # Set top pixel background color
                        )
                    out += BTM_PXL_CH
                elif top_color.a >= ALPHA_CUTOFF:
                    out += (
                        f"{ESC}[38;2;{top_color}m" + TOP_PXL_CH
                    )  # Set top pixel color and print character

            out += RES  # Reset the color for the next pixel

        out += "\n"  # Move to the next line after processing a row of pixels

    print(out)


def print_random_image() -> None:
    """Calls `print_image_array_to_console` with a random image from the PNGs directory."""
    global ALL_PNGS_FOUND_IN_PATH
    print_png_to_console(Image.open(random.choice(ALL_PNGS_FOUND_IN_PATH)))


def print_image_by_name(png_name: str) -> None:
    """Calls `print_image_array_to_console` with an image from the PNGs directory by filename."""
    check_png_exists(png_name)
    print_png_to_console(Image.open(f"{png_name}.png"))


def print_random_image_from_names(png_names: list[str]) -> None:
    """Calls `print_image_array_to_console` with a random image from a string list of filenames in the PNGs directory."""
    # Check to see that all of these names are actually in the PNGs directory
    global ALL_PNGS_FOUND_IN_PATH, PNGS_PATH
    for filename in png_names:
        check_png_exists(filename)

    print_png_to_console(Image.open(f"{random.choice(png_names)}.png"))


def check_png_exists(png_filename) -> None:
    """Checks to see if the specified PNG filename was located in the config dir. Will halt execution if it's not found."""
    global ALL_PNGS_FOUND_IN_PATH, PNGS_PATH
    if f"{png_filename}.png" not in ALL_PNGS_FOUND_IN_PATH:
        print(f"Dude. '{png_filename}.png' isn't in {PNGS_PATH}. Stop it.")
        sys.exit(1)


def run_first_time_config() -> None:
    """Initialize the program by creating a .config folder and a default .conf file."""
    global CONFIG_DIR, CONFIG_FILENM
    print(f"Performing first-time set up ...")
    
    Path.mkdir(CONFIG_DIR, exist_ok=True)
    config_path = CONFIG_DIR.joinpath(CONFIG_FILENM)

    DEFAULT_PNGS_LOCATION = "~/Pictures/Sprites"
    with open(config_path, "w") as file:
        file.write(f"[DEFAULT]\nPNGS_LOCATION = {DEFAULT_PNGS_LOCATION}\n")
    
    print(f"'{config_path}' has been established with default PNGs location at '{DEFAULT_PNGS_LOCATION}'.")
    print(f"Either go put some PNGs there and run this again or change the config file to make the program look for images somewhere else!")
    sys.exit(0)


def main() -> None:
    """Entry point to the program."""
    load_config()

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
        print_random_image()
    elif args.name:
        print_image_by_name(args.name[0])
    elif args.random_name:
        names = args.random_name[0].split(",")
        print_random_image_from_names(names)
    else:
        parser.print_help()

    reset_console_color()


if __name__ == "__main__":
    main()
