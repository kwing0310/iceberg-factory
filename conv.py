import signal
import argparse
import sys
import os
from pathlib import Path

from ImageGoNord import GoNord

from rich.console import Console
from rich.panel import Panel

def main():

    signal.signal(signal.SIGINT, signal_handler)
    console = Console()

    ib_factory = GoNord()
    ib_factory.reset_palette()
    add_ib_palette(ib_factory)

    # Checks if there's an argument
    if len(sys.argv) > 1:
        image_paths = fromCommandArgument(console)
    else:
        image_paths = fromTui(console)

    for image_path in image_paths:
        if os.path.isfile(image_path):
            process_image(image_path, console, ib_factory)
        else:
            console.print(
                f"❌ [red]We had a problem in the pipeline! \nThe image at '{image_path}' could not be found! \nSkipping... [/]"
            )
            continue

# Gets the file path from the Argument
def fromCommandArgument(console):
    command_parser = argparse.ArgumentParser(
        description="A simple cli to manufacture Iceberg themed wallpapers."
    )
    command_parser.add_argument(
        "Path", metavar="path", nargs="+", type=str, help="The path(s) to the image(s)."
    )
    args = command_parser.parse_args()

    return args.Path

# Gets the file path from user input
def fromTui(console):

    console.print(
        Panel(
            " [bold magenta] Iceberg Factory [/] ", expand=False, border_style="magenta"
        )
    )

    return [
        os.path.expanduser(path)
        for path in console.input(
            "[bold yellow]Which image(s) do you want to manufacture? (image paths separated by spaces):[/] "
        ).split()
    ]

def process_image(image_path, console, ib_factory):
    image = ib_factory.open_image(image_path)
    
    console.print(f"[blue]manufacturing '{os.path.basename(image_path)}'...[/]")

    # TODO: might be a better idea to save the new Image in the same directory the command is being run from
    save_path = os.path.join(
        os.path.dirname(image_path), "ib-" + os.path.basename(image_path)
    )

    ib_factory.convert_image(image, save_path=(save_path))
    console.print(f"[bold green]Done![/] [green](saved at '{save_path}')[/]")

def add_ib_palette(ib_factory):

    ibPalette = ["#161821","#1e2132","#353a50","#6b7089","#e27878","#e98989","#b4be82","#c0ca8e","#e2a478","#e9b189","#84a0c6","#91acd1","#a093c7","#ada0d3","#89b8c2","#95c4c2","#c6c8c1","#d2d4de"]

    for color in ibPalette:
        ib_factory.add_color_to_palette(color)

## handle CTRL + C
def signal_handler(signal, frame):
    print()
    sys.exit(0)

if __name__ == "__main__":
    main()
