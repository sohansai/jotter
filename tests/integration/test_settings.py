from jotter.configuration.settings import get_db_path


def test_database_path_resolution(tmp_path, monkeypatch):
    # 1. JOTTER_DB is set
    monkeypatch.setenv("JOTTER_DB", str(tmp_path / "custom.db"))
    assert get_db_path() == tmp_path / "custom.db"

    # 2. Not set, default fallback
    monkeypatch.delenv("JOTTER_DB", raising=False)

    def mock_user_data_dir(appname):
        return str(tmp_path / "jotter")

    import jotter.configuration.settings as settings_mod

    monkeypatch.setattr(settings_mod, "user_data_dir", mock_user_data_dir)

    expected_default = tmp_path / "jotter" / "jotter.db"
    assert get_db_path() == expected_default
