import click
from .main import main


@click.command()
@click.option('--scale', default=1.0, help='Scale sizes by this factor.')
@click.option('--in-file', help='ASCII file to convert.')
@click.option('--time-direction', default=0, help='Direction of the time arrow (0, 90, 180, or 270).')
def cli(scale, in_file, time_direction):
    svg = main(scale, in_file, time_direction)
    print(svg)
