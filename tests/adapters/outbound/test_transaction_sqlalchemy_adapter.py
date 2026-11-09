from unittest.mock import MagicMock
from app.adapters.outbound.transaction.transaction_sqlalchemy_adapter import (
    SqlAlchemyTransactionAdapter,
)
from app.ports.outbound.transaction.transaction_outbound_port import (
    TransactionOutboundPort,
)


def test_transaction_adapter_implements_port():
    mock_session = MagicMock()
    adapter = SqlAlchemyTransactionAdapter(mock_session)
    assert isinstance(adapter, TransactionOutboundPort)


def test_transaction_adapter_commit():
    mock_session = MagicMock()
    adapter = SqlAlchemyTransactionAdapter(mock_session)
    adapter.commit()
    mock_session.commit.assert_called_once()


def test_transaction_adapter_rollback():
    mock_session = MagicMock()
    adapter = SqlAlchemyTransactionAdapter(mock_session)
    adapter.rollback()
    mock_session.rollback.assert_called_once()


def test_transaction_adapter_context_manager_on_exception():
    mock_session = MagicMock()
    adapter = SqlAlchemyTransactionAdapter(mock_session)

    try:
        with adapter:
            raise ValueError("Erreur inattendue")
    except ValueError:
        pass

    mock_session.rollback.assert_called_once()
