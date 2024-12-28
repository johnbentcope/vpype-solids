import click
import numpy as np
import vpype as vp
import vpype_cli

from vpype_cli.types import LayerType,LengthType

@click.command()
@click.argument("filename",type=vpype_cli.PathType(exists=True))
@click.argument("text",type=str)
@click.option(
    "-s",
    "--size",
    type=LengthType(),
    default=18,
    help="Text size (default: 18)."
)
@click.option(
    "-l",
    "--layer",
    type=LayerType(accept_new=True),
    default=1,
    help="Layer for text (default: 1)."
)
@vpype_cli.global_processor
def solids(document: vp.Document, layer: int, filename: str, text: str, size: float):
    """
    Load OBJ files into vpype.
    """
    target_layer = vpype_cli.single_to_layer_id(layer, document)
    lc = vp.LineCollection()
    document.add(lc, target_layer)
    return document

solids.help_group = "Input"