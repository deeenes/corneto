import sys
import warnings

from corneto import _plotting as pl
from corneto._constants import *
from corneto._graph import Attr, Attributes, EdgeType, Graph
from corneto._util import info
from corneto.backend import DEFAULT_BACKEND, DEFAULT_SOLVER, available_backends

# from corneto.backend import DEFAULT_BACKEND as K  # deprecate
# from corneto.backend import DEFAULT_BACKEND as ops  # deprecate
from corneto.backend import DEFAULT_BACKEND as opt
from corneto.backend._base import HammingLoss as hamming_loss
from corneto.backend._base import Indicator, NonZeroIndicator

# from corneto._core import GReNet as Graph
from corneto.methods import (
    create_flow_graph,
    default_sign_loss,
    signaling,
    signflow_constraints,
)
from corneto.utils import Attr, Attributes


def get_version():
    import os
    import re

    here = os.path.abspath(os.path.dirname(__file__))
    pyproject_path = os.path.join(here, "..", "pyproject.toml")

    with open(pyproject_path, "r") as f:
        content = f.read()

    # Regex to find the version number
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.M)
    if match:
        return match.group(1)
    raise RuntimeError("Version not found in pyproject.toml.")


class DeprecatedBackend:
    def __init__(self, backend):
        self._backend = backend

    def __getattr__(self, attr):
        warnings.warn(
            "'corneto.K' and 'corneto.ops' are deprecated and will be removed in a future version. Use 'corneto.opt' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return getattr(self._backend, attr)


# This way of accessing the backend is deprecated
K = DeprecatedBackend(opt)
ops = DeprecatedBackend(opt)


__all__ = [
    "Attr",
    "EdgeType",
    "Attributes",
    "Graph",
    "info",
    "DEFAULT_BACKEND",
    "available_backends",
    "K",
    "ops",
]


import_sif = Graph.from_sif

try:
    # Python 3.8 and newer
    from importlib.metadata import version
except ImportError:
    # Python < 3.8
    from importlib_metadata import version

__version__ = version("corneto")

sys.modules.update({f"{__name__}.{m}": globals()[m] for m in ["pl"]})

del sys
