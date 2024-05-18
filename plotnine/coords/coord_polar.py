from __future__ import annotations

import typing
from types import SimpleNamespace
import numpy as np
from ..iapi import panel_view
from ..positions.position import transform_position
from .coord import coord

if typing.TYPE_CHECKING:
    from typing import Optional
    import pandas as pd
    from plotnine.iapi import scale_view
    from plotnine.scales.scale import scale
    from plotnine.typing import (
        FloatArray,
        FloatSeries,
        TupleFloat2,
    )


class coord_polar(coord):
    """
    Polar coordinate system

    Parameters
    ----------
    theta : str, default='x'
        Variable to map angle to (`'x'` or `'y'`).
    start : float, default=0
        Offset of starting point from 12 o'clock in radians.
    direction : int, default=1
        1 for clockwise, -1 for anticlockwise.
    expand : bool, default=True
        If `True`, expand the coordinate axes by some factor. If `False`,
        use the limits from the data.
    """

    is_linear = True

    def __init__(
        self,
        theta: str = "x",
        start: float = 0,
        direction: int = 1,
        expand: bool = True,
    ):
        self.theta = theta
        self.start = start
        self.direction = direction
        self.expand = expand

    def transform(
        self, data: pd.DataFrame, panel_params: panel_view, munch: bool = False
    ) -> pd.DataFrame:
        from mizani.bounds import squish_infinite

        arc = self.start + np.array([0, 2 * np.pi])

        def rescale(arr, to):
            return (arr - np.min(arr)) / (np.max(arr) - np.min(arr)) * (to[1] - to[0]) + to[0]

        if self.theta == "x":
            data["theta"] = rescale(data["x"], arc)
            data["r"] = rescale(data["y"], (0, 0.45))
        else:
            data["theta"] = rescale(data["y"], arc)
            data["r"] = rescale(data["x"], (0, 0.45))

        data["x"] = data["r"] * np.sin(data["theta"]) + 0.5
        data["y"] = data["r"] * np.cos(data["theta"]) + 0.5

        return data

    def setup_panel_params(self, scale_x: scale, scale_y: scale) -> panel_view:
        """
        Compute the range and break information for the panel
        """
        from mizani.transforms import identity_trans

        def get_scale_view(
            scale: scale, coord_limits: TupleFloat2
        ) -> scale_view:
            expansion = scale.default_expansion(expand=self.expand)
            ranges = scale.expand_limits(
                scale.limits, expansion, coord_limits, identity_trans
            )
            sv = scale.view(limits=coord_limits, range=ranges.range)
            return sv

        out = panel_view(
            x=get_scale_view(scale_x, None),
            y=get_scale_view(scale_y, None),
        )
        return out

    def distance(
        self,
        x: FloatSeries,
        y: FloatSeries,
        panel_params: panel_view,
    ) -> FloatArray:
        max_dist = np.max(np.sqrt(panel_params.x.range**2 + panel_params.y.range**2))
        dist = np.sqrt(x**2 + y**2)
        return dist / max_dist
