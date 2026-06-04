from contextlib import contextmanager
from threading import Lock
from typing import Iterator

sync_lock = Lock()


@contextmanager
def synchronization_lock() -> Iterator[None]:
    print("Acquiring synchronization lock")
    sync_lock.acquire()

    try:
        yield
    finally:
        print("Releasing synchronization lock")
        sync_lock.release()


def synchronize_bank_import() -> None:
    print("Synchronizing transactions from bank API")


def run_scheduled_sync() -> None:
    with synchronization_lock():
        synchronize_bank_import()


if __name__ == "__main__":
    run_scheduled_sync()
