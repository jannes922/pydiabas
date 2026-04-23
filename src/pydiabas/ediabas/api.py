# Copyright (c) 2024 Aljoscha Greim <aljoscha@bembelbytes.com>
# MIT License

"""EDIABAS API loader.

Loads api32.dll on 32-bit Python and api64.dll on 64-bit Python, and exposes the
EDIABAS API entry points as module-level attributes regardless of bitness.

Pointer-sized arguments and return values (the result-scope handle returned by
apiResultsNew and passed back to apiResultsScope / apiResultsDelete) are
declared as c_void_p so they are not truncated to 32 bits on 64-bit builds.
"""

import ctypes
from ctypes.util import find_library


# 8 on 64-bit interpreters, 4 on 32-bit interpreters
_IS_64BIT = ctypes.sizeof(ctypes.c_void_p) == 8

_LIB_NAME = "api64" if _IS_64BIT else "api32"

_lib_path = find_library(_LIB_NAME)
if _lib_path is None:
    raise OSError(
        f"Unable to locate the EDIABAS '{_LIB_NAME}.dll' library. "
        "Make sure EDIABAS is installed and its 'bin' directory is on the system PATH."
    )

_api = ctypes.WinDLL(_lib_path)


# Extract functions from DLL
enableServer = _api.enableServer  # Not implemented in api.py
closeServer = _api.closeServer  # Not implemented in api.py
enableMultiThreading = _api.enableMultiThreading  # Not implemented in api.py

apiInit = _api.__apiInit
apiInitExt = _api.__apiInitExt  # Not implemented in api.py
apiBreak = _api.__apiBreak
apiEnd = _api.__apiEnd

apiSwitchDevice = _api.__apiSwitchDevice  # Not implemented in api.py

apiState = _api.__apiState
apiStateExt = _api.__apiStateExt  # Not implemented in api.py

apiTrace = _api.__apiTrace

apiCheckVersion = _api.__apiCheckVersion
apiGetConfig = _api.__apiGetConfig
apiSetConfig = _api.__apiSetConfig

apiErrorCode = _api.__apiErrorCode
apiErrorText = _api.__apiErrorText

apiJob = _api.__apiJob
apiJobData = _api.__apiJobData
apiJobExt = _api.__apiJobExt
apiJobInfo = _api.__apiJobInfo

apiResultSets = _api.__apiResultSets
apiResultNumber = _api.__apiResultNumber
apiResultName = _api.__apiResultName
apiResultFormat = _api.__apiResultFormat

apiResultBinary = _api.__apiResultBinary
apiResultBinaryExt = _api.__apiResultBinaryExt
apiResultByte = _api.__apiResultByte
apiResultChar = _api.__apiResultChar
apiResultDWord = _api.__apiResultDWord
apiResultInt = _api.__apiResultInt
apiResultLong = _api.__apiResultLong
apiResultReal = _api.__apiResultReal
apiResultText = _api.__apiResultText
apiResultVar = _api.__apiResultVar
apiResultWord = _api.__apiResultWord

apiResultsNew = _api.__apiResultsNew
apiResultsScope = _api.__apiResultsScope
apiResultsDelete = _api.__apiResultsDelete


# The result-scope handle is a native pointer (void *). ctypes defaults return
# and argument types to c_int, which would silently truncate a 64-bit pointer
# to 32 bits and corrupt the handle on 64-bit Python. Declare them as c_void_p
# so ctypes marshals the full-width pointer on both architectures.
_APIHANDLE = ctypes.c_uint  # APIHANDLE is a 32-bit unsigned int in both api32 and api64

apiResultsNew.restype = ctypes.c_void_p
apiResultsScope.argtypes = [_APIHANDLE, ctypes.c_void_p]
apiResultsDelete.argtypes = [_APIHANDLE, ctypes.c_void_p]


# Functions that only exist in api64.dll. Expose them when present so callers
# on 64-bit builds can use them; on 32-bit builds these attributes are absent.
if _IS_64BIT:
    apiResultLongLong = _api.__apiResultLongLong
    apiResultQWord = _api.__apiResultQWord
    apiXSysSetConfig = _api.__apiXSysSetConfig
