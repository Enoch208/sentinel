from __future__ import annotations

import resource
import sys


def footprint_mb() -> float:
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    scale = 1.0 if sys.platform == "darwin" else 1024.0
    return peak * scale / (1024.0 * 1024.0)
