from importlib.metadata import version, PackageNotFoundError

from .config import TracerSettings
from .tracer_service import TracerService

__all__ = ["TracerSettings", "TracerService", "__version__"]

try:
    __version__ = version("tracing-lib")
except PackageNotFoundError:
    __version__ = "0.0.0"
