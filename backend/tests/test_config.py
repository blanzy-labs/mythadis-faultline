from app.config import Settings


def test_default_models_when_environment_is_absent(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    monkeypatch.delenv("GEMINI_MODEL", raising=False)

    settings = Settings(_env_file=None)

    assert settings.OPENAI_MODEL == "gpt-4.1-mini"
    assert settings.GEMINI_MODEL == "gemini-2.5-flash"
    assert settings.OPENAI_API_KEY == ""
    assert settings.GEMINI_API_KEY == ""
    assert settings.LOCAL_LLM_ENABLED is False
    assert settings.LOCAL_LLM_BASE_URL == ""
    assert settings.LOCAL_LLM_MODEL == ""
    assert settings.LOCAL_LLM_API_KEY == ""
    assert settings.LOCAL_LLM_TIMEOUT_SECONDS == 120


def test_model_overrides_are_read_from_environment(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_MODEL", "openai-test-model")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-test-model")

    settings = Settings(_env_file=None)

    assert settings.OPENAI_MODEL == "openai-test-model"
    assert settings.GEMINI_MODEL == "gemini-test-model"


def test_local_llm_config_overrides_are_read_from_environment(monkeypatch) -> None:
    monkeypatch.setenv("LOCAL_LLM_ENABLED", "true")
    monkeypatch.setenv("LOCAL_LLM_BASE_URL", "http://localhost:11434/v1")
    monkeypatch.setenv("LOCAL_LLM_MODEL", "test-local-model")
    monkeypatch.setenv("LOCAL_LLM_API_KEY", "")
    monkeypatch.setenv("LOCAL_LLM_TIMEOUT_SECONDS", "45")

    settings = Settings(_env_file=None)

    assert settings.LOCAL_LLM_ENABLED is True
    assert settings.LOCAL_LLM_BASE_URL == "http://localhost:11434/v1"
    assert settings.LOCAL_LLM_MODEL == "test-local-model"
    assert settings.LOCAL_LLM_API_KEY == ""
    assert settings.LOCAL_LLM_TIMEOUT_SECONDS == 45
