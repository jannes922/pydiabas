# Copyright (c) 2024 Aljoscha Greim <aljoscha@bembelbytes.com>
# MIT License

"""Backward-compatible alias for the bitness-aware loader in :mod:`api`.

Historically this module unconditionally loaded ``api32.dll``. It now forwards
to :mod:`pydiabas.ediabas.api`, which picks ``api32.dll`` or ``api64.dll``
based on the running Python interpreter's bitness.
"""

from .api import *  # noqa: F401,F403
