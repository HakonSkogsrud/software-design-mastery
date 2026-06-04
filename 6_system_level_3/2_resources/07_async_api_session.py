import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator


class BankApiSession:
    async def fetch_transactions(self) -> list[dict[str, str]]:
        print("Fetching transactions from bank API")
        await asyncio.sleep(0.2)

        return [
            {
                "id": "tx-001",
                "description": "Coffee",
                "amount": "3.50",
            }
        ]

    async def close(self) -> None:
        print("Closing bank API session")


@asynccontextmanager
async def api_session() -> AsyncIterator[BankApiSession]:
    print("Opening bank API session")
    session = BankApiSession()

    try:
        yield session
    finally:
        await session.close()


async def synchronize_transactions() -> None:
    async with api_session() as session:
        transactions = await session.fetch_transactions()
        print(transactions)


if __name__ == "__main__":
    asyncio.run(synchronize_transactions())
