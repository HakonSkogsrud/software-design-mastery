# Finance app structure

This example organizes code by responsibility instead of technical type.

- `transactions/` owns transaction concepts, filtering, and sample loading.
- `reports/` owns report models, spending calculations, and presentation.
- `scripts/` contains operational tasks that can call application code.
- `tests/` mirrors the application structure.

Run the example with:

```bash
PYTHONPATH=src python main.py
```
