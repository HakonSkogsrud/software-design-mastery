# Finance App Examples

Code examples for the Software Design Mastery lesson: **Organizing Code into Modules and Folders**.

## Run the example

```bash
PYTHONPATH=src python main.py
```

Expected output:

```text
Spending report
---------------
Total spent: €74.34
Transactions: 4

By category:
- Food: €45.60
- Transport: €8.75
- Education: €19.99
```

## Run the operational script

```bash
PYTHONPATH=src python scripts/import_old_transactions.py
```

## Run tests

```bash
PYTHONPATH=src pytest
```
