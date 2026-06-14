from app.config import Settings


def test_default_models_when_environment_is_absent(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    monkeypatch.delenv("GEMINI_MODEL", raising=False)

    settings = Settings(_env_file=None)

    assert settings.OPENAI_MODEL == "gpt-4.1-mini"
    assert settings.GEMINI_MODEL == "gemini-2.5-flash"
    assert settings.OPENAI_API_KEY == ""
    assert settings.GEMINI_API_KEY == ""


def test_model_overrides_are_read_from_environment(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_MODEL", "openai-test-model")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-test-model")

    settings = Settings(_env_file=None)

    assert settings.OPENAI_MODEL == "openai-test-model"
    assert settings.GEMINI_MODEL == "gemini-test-model"
