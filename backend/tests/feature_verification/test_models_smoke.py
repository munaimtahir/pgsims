import importlib
import pytest

@pytest.mark.parametrize("module", [
    "sims.users.models",
    "sims.cases.models",
    "sims.logbook.models",
    "sims.certificates.models",
    "sims.rotations.models",
])
def test_models_import(module):
    importlib.import_module(module)
