from py_validate.api import *  # noqa
import warnings


msg = ("validator has been deprecated in favor of api. "
       "Please import from that module instead.")
warnings.warn(msg, FutureWarning)
