import os
from dataclasses import dataclass

@dataclass
class TracerConfig:
    host: str = os.getenv("LANGFUSE_HOST", "")
    public_key: str = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    secret_key: str = os.getenv("LANGFUSE_SECRET_KEY", "")