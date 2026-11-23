import pytest

import app as appli


@pytest.fixture(autouse=True)
def base_temporaire(tmp_path, monkeypatch):
    monkeypatch.setattr(appli, "DB", str(tmp_path / "test.db"))
    appli.init_db()
