# /usr/bin/env python

import sys
from PIL import Image
from pathlib import Path

ALL_PNGS_FOUND_IN_PATH: list[str] = []
PNGS_PATH: Path


def reset_console_color() -> None:
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


def parse_args() -> None:
    """Parse & return the arguments passed by the user."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="png-colorscripts",
        description="CLI utility that prints out unicode images from PNGs located in a user-specified directory",
        usage="png-colorscripts -l '[PATH_TO_PNGS]' [-r | -n 'filename' | -rn 'image1,image2,image3' ]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
    )

    parser.add_argument(
        "-h", "--help", action="help", help="Show this help message and exit"
    )
    parser.add_argument(
        "-l",
        "--location",
        type=Path,
        required=True,
        help="The path containing all of your PNGs.",
    )

    group = parser.add_argument_group("modes")

    group.add_argument(
        "-r",
        "--random",
        action="store_true",
        help="Print a random PNG from directory",
    )
    group.add_argument(
        "-n",
        "--name",
        type=str,
        nargs=1,
        help="Print a PNG by name from directory; do not include file-type",
    )
    group.add_argument(
        "-rn",
        "--random-name",
        type=str,
        nargs=1,
        help="Print a random PNG by name from a list of names, comma-separated WITHOUT whitespace or file-types (e.g. 'image1,image2,image3')",
    )

    args = parser.parse_args()
    return parser, args


def handle_args(parser, args) -> None:
    """Run the script according to the mode the user selected."""
    if args.random:
        print_random_image()
    elif args.name:
        print_image_by_name(args.name[0])
    elif args.random_name:
        names = args.random_name[0].split(",")
        print_random_image_from_names(names)
    else:
        parser.print_help()


def find_images() -> None:
    """Search "pngs_path"" for all PNGs & assign them to a global variable."""
    import os

    global ALL_PNGS_FOUND_IN_PATH, PNGS_PATH

    os.chdir(PNGS_PATH)
    for filename in os.listdir("."):
        ALL_PNGS_FOUND_IN_PATH.append(filename) if filename.endswith(".png") else None

    if len(ALL_PNGS_FOUND_IN_PATH) == 0:
        print(f"There are no PNGs located in ${PNGS_PATH}.")
        print("Please go put some there, you dingus.")
        sys.exit(1)


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
    import random

    global ALL_PNGS_FOUND_IN_PATH

    print_png_to_console(Image.open(random.choice(ALL_PNGS_FOUND_IN_PATH)))


def print_image_by_name(name: str) -> None:
    """Calls `print_image_array_to_console` with an image from the PNGs directory by filename."""
    global ALL_PNGS_FOUND_IN_PATH
    check_png_exists(name)
    print_png_to_console(Image.open(f"{name}.png"))


def print_random_image_from_names(names: list[str]) -> None:
    """Calls `print_image_array_to_console` with a random image from a string list of filenames in the PNGs directory."""
    import random

    global ALL_PNGS_FOUND_IN_PATH
    # Check to see that all of these names are actually in the PNGs directory
    for filename in names:
        check_png_exists(filename)

    print_png_to_console(Image.open(f"{random.choice(names)}.png"))


def check_png_exists(name: str) -> None:
    """Checks to see if the specified PNG was found when location was scanned."""
    global ALL_PNGS_FOUND_IN_PATH, PNGS_PATH
    if f"{name}.png" not in ALL_PNGS_FOUND_IN_PATH:
        print(f"'{name}.png' isn't in {PNGS_PATH}. Stop it.")
        sys.exit(1)


def main() -> None:
    """Entry point to the program."""
    # Parse the command-line arguments
    parser, args = parse_args()

    # If no arguments were provided, print help & quit
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Make the user-provided path globally-known
    global PNGS_PATH
    PNGS_PATH = args.location.expanduser()

    # Find all images in said directory
    find_images()

    # Perform the rest of the script based on mode
    handle_args(parser, args)

    # Reset console color after printing the image
    reset_console_color()


if __name__ == "__main__":
    main()
