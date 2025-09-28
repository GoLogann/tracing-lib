import logging
from typing import Optional, Dict, Any, Callable
from langfuse import Langfuse, observe

logger = logging.getLogger(__name__)


class TracerService:
    def __init__(self, host: str, public_key: str, secret_key: str):
        """
        Inicializa o cliente Langfuse.
        """
        self.enabled = all([host, public_key, secret_key])
        if self.enabled:
            try:
                self.client = Langfuse(
                    host=host,
                    public_key=public_key,
                    secret_key=secret_key,
                )
                logger.info("[TracerService] Langfuse inicializado com sucesso.")
            except Exception as e:
                logger.error("[TracerService] Falha ao inicializar Langfuse: %s", e)
                self.enabled = False
        else:
            self.client = None
            logger.warning("[TracerService] Langfuse não habilitado (sem config).")


    def start_trace(self, name: str, metadata: Optional[Dict[str, Any]] = None):
        if not self.enabled:
            return None
        return self.client.start_as_current_span(name=name, metadata=metadata or {})


    def start_observation(
        self, as_type: str, name: str,
        input: Optional[Any] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        if not self.enabled:
            return None
        return self.client.start_as_current_observation(
            as_type=as_type, name=name, input=input, metadata=metadata or {}
        )


    def start_generation(
        self, name: str, model: str,
        input: Optional[Any] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        if not self.enabled:
            return None
        return self.client.start_as_current_generation(
            name=name, model=model, input=input, metadata=metadata or {}
        )


    def add_score(
        self,
        trace_or_obs,
        name: str,
        value: float | int | str | bool,
        comment: Optional[str] = None,
    ):
        """
        Adiciona score diretamente ao trace ou observation passado.
        """
        if not self.enabled or not trace_or_obs:
            return
        try:
            trace_or_obs.score(name=name, value=value, comment=comment)
        except Exception as e:
            logger.error(f"[TracerService] Falha ao adicionar score ({name}): {e}")


    def observe(self, as_type: str, name: Optional[str] = None) -> Callable:
        """Decorator para instrumentar funções automaticamente."""
        def wrapper(func):
            return observe(as_type=as_type, name=name or func.__name__)(func)
        return wrapper
