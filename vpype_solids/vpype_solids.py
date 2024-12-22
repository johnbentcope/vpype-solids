import vpype as vp
import vpype_cli


@vpype_cli.cli.command(group="Plugins")
@vpype_cli.generator
def vpype_solids() -> vp.LineCollection:
    """
    Insert documentation here...
    """
    lc = vp.LineCollection()
    return lc
