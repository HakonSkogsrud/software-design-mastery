import asyncio
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Trade:
    id: str
    symbol: str
    quantity: int
    price: Decimal


class TransactionLedger:
    def __init__(self) -> None:
        self._trades: list[Trade] = []

    def record(self, trade: Trade) -> None:
        self._trades.append(trade)

    def contains(self, trade_id: str) -> bool:
        return any(trade.id == trade_id for trade in self._trades)


class PortfolioView:
    def __init__(self) -> None:
        self._holdings: dict[str, int] = {}

    def apply(self, trade: Trade) -> None:
        current_quantity = self._holdings.get(trade.symbol, 0)
        self._holdings[trade.symbol] = current_quantity + trade.quantity

    def quantity_for(self, symbol: str) -> int:
        return self._holdings.get(symbol, 0)


class ReportingView:
    def __init__(self) -> None:
        self._invested_amount = Decimal("0.00")

    def apply(self, trade: Trade) -> None:
        self._invested_amount += trade.price * trade.quantity

    @property
    def invested_amount(self) -> Decimal:
        return self._invested_amount


async def update_portfolio(
    trade: Trade,
    portfolio: PortfolioView,
) -> None:
    await asyncio.sleep(1)
    portfolio.apply(trade)
    print("Portfolio view updated")


async def update_reporting(
    trade: Trade,
    reporting: ReportingView,
) -> None:
    await asyncio.sleep(2)
    reporting.apply(trade)
    print("Reporting view updated")


async def execute_trade(
    trade: Trade,
    ledger: TransactionLedger,
    portfolio: PortfolioView,
    reporting: ReportingView,
) -> None:
    ledger.record(trade)
    print("Trade recorded in the authoritative ledger")

    # In a real system, these tasks would normally be handed to a durable
    # queue rather than created directly inside the process.
    async with asyncio.TaskGroup() as task_group:
        task_group.create_task(update_portfolio(trade, portfolio))
        task_group.create_task(update_reporting(trade, reporting))

        await asyncio.sleep(0)

        print("\nImmediately after recording the trade:")
        print(f"Ledger contains trade: {ledger.contains(trade.id)}")
        print(f"Portfolio quantity: {portfolio.quantity_for(trade.symbol)}")
        print(f"Reported investment: €{reporting.invested_amount:.2f}")


async def main() -> None:
    ledger = TransactionLedger()
    portfolio = PortfolioView()
    reporting = ReportingView()

    trade = Trade(
        id="trade-789",
        symbol="ACME",
        quantity=10,
        price=Decimal("25.00"),
    )

    print(
        "The previous lesson showed why work may be performed "
        "asynchronously.\n"
        "This example shows the consistency consequence.\n"
    )

    await execute_trade(
        trade,
        ledger,
        portfolio,
        reporting,
    )

    print("\nAfter synchronization finishes:")
    print(f"Ledger contains trade: {ledger.contains(trade.id)}")
    print(f"Portfolio quantity: {portfolio.quantity_for(trade.symbol)}")
    print(f"Reported investment: €{reporting.invested_amount:.2f}")


if __name__ == "__main__":
    asyncio.run(main())
