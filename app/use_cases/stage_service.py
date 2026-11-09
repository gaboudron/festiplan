"""Service applicatif pour les scènes."""

from app.domain.festival.entities import Stage
from app.ports.inbound.stage_inbound_port import StageInboundPort
from app.ports.outbound.repository.festival_repository_outbound_port import (
    FestivalRepositoryOutboundPort,
)
from app.ports.outbound.repository.stage_repository_outbound_port import (
    StageRepositoryOutboundPort,
)
from app.ports.outbound.transaction.transaction_outbound_port import (
    TransactionOutboundPort,
)
from app.use_cases._support import in_transaction, require_festival


class StageService(StageInboundPort):
    """Implémente ``StageInboundPort``."""

    def __init__(
        self,
        stages: StageRepositoryOutboundPort,
        festivals: FestivalRepositoryOutboundPort,
        transaction: TransactionOutboundPort,
    ) -> None:
        self._stages = stages
        self._festivals = festivals
        self._transaction = transaction

    def list_stages(self, festival_id: int) -> list[Stage]:
        return self._stages.list_by_festival_id(festival_id)

    def create_stage(self, stage: Stage) -> Stage:
        # Une scène ne peut être rattachée qu'à un festival existant.
        require_festival(self._festivals, stage.festival_id)
        return in_transaction(
            self._transaction, lambda: self._stages.save(stage)
        )
