from warnings import warn

from ..doctools import document
from ..exceptions import PlotnineError, PlotnineWarning
from ..utils import alias
from .scale_continuous import scale_continuous
from .scale_discrete import scale_discrete

LINETYPES = ["solid", "dashed", "dashdot", "dotted"]


@document
class scale_linetype(scale_discrete):
    """
    Scale for line patterns

    Parameters
    ----------
    {superclass_parameters}

    Notes
    -----
    The available linetypes are
    ``'solid', 'dashed', 'dashdot', 'dotted'``
    If you need more custom linetypes, use
    :class:`~plotnine.scales.scale_linetype_manual`
    """

    _aesthetics = ["linetype"]

    def __init__(self, **kwargs):
        from mizani.palettes import manual_pal

        self.palette = manual_pal(LINETYPES)
        super().__init__(**kwargs)


@document
class scale_linetype_ordinal(scale_linetype):
    """
    Scale for line patterns

    Parameters
    ----------
    {superclass_parameters}
    """

    _aesthetics = ["linetype"]

    def __init__(self, **kwargs):
        warn(
            "Using linetype for an ordinal variable is not advised.",
            PlotnineWarning,
        )
        super().__init__(**kwargs)


class scale_linetype_continuous(scale_continuous):
    """
    Linetype scale
    """

    def __init__(self):
        raise PlotnineError(
            "A continuous variable can not be mapped to linetype"
        )


scale_linetype_discrete = alias("scale_linetype_discrete", scale_linetype)
