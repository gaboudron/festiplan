from sqlalchemy.orm import Session
from app.ports.outbound.transaction.transaction_outbound_port import (
    TransactionOutboundPort,
)


class SqlAlchemyTransactionAdapter(TransactionOutboundPort):
    def __init__(self, db: Session):
        self.db = db

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()
