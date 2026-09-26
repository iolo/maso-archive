"""CD3 reading-display normalization, separate from preserved source formatting."""


def reading_run(run):
    """Remove the pervasive CD3 underline without changing the source run.

    The decoder RTF underlines 4,463,116 of 4,478,600 article characters across
    all 968 candidates: HELPDECO mistakes the character-set byte for double
    underline. This is a display workaround, not a decoder correction; it also
    hides genuine underline. Generated RTF/blocks retain the erroneous flags.
    See docs/CD3-HELPDECO-UNDERLINE-BUG.md for evidence and the deferred fix.
    """
    return {**run, 'underline': False} if run.get('underline') else run
