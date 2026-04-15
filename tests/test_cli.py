from __future__ import annotations

import json

import pytest

from czm_cli import cli as cli_module
from czm_cli.errors import EXIT_CONFLICT, EXIT_USAGE


class FakeClient:
    def __init__(self, responses: dict[tuple[str, str], object]):
        self.responses = responses
        self.requests = []

    def get(self, path, params=None):
        self.requests.append(("GET", path, params))
        response = self.responses[("GET", path)]
        if isinstance(response, Exception):
            raise response
        return response

    def post(self, path, json=None, params=None):
        self.requests.append(("POST", path, json))
        response = self.responses[("POST", path)]
        if isinstance(response, Exception):
            raise response
        return response

    def patch(self, path, json=None, params=None):
        self.requests.append(("PATCH", path, json))
        response = self.responses[("PATCH", path)]
        if isinstance(response, Exception):
            raise response
        return response

    def delete(self, path, json=None, params=None):
        self.requests.append(("DELETE", path, json))
        response = self.responses[("DELETE", path)]
        if isinstance(response, Exception):
            raise response
        return response

    def close(self):
        pass


class DummyConfig:
    base_url = "http://example"
    api_key = "k"
    timezone = "UTC"

    def normalized_base_url(self):
        return "http://example"


def test_cli_json_output(monkeypatch, capsys):
    fake = FakeClient(
        {
            ("GET", "/subjects"): {"subjects": [{"id": 1, "display_name": "Child"}]},
        }
    )
    monkeypatch.setattr(cli_module, "CzmClient", lambda *args, **kwargs: fake)
    monkeypatch.setattr(cli_module, "resolve_runtime_config", lambda **kwargs: DummyConfig())
    exit_code = cli_module.main(["--json", "--base-url", "http://example", "--api-key", "k", "subject", "list"])
    assert exit_code == 0
    output = capsys.readouterr().out.strip()
    assert json.loads(output) == {"subjects": [{"id": 1, "display_name": "Child"}]}


def test_cli_missing_config_exit_code(monkeypatch, capsys):
    monkeypatch.delenv("CZM_BASE_URL", raising=False)
    monkeypatch.delenv("CZM_API_KEY", raising=False)
    exit_code = cli_module.main(["subject", "list"])
    assert exit_code == EXIT_USAGE
    assert "missing required configuration" in capsys.readouterr().err


def test_cli_conflict_exit_code_json(monkeypatch, capsys):
    fake = FakeClient({("GET", "/subjects"): cli_module.CzmError("conflict happened", exit_code=EXIT_CONFLICT)})
    monkeypatch.setattr(cli_module, "CzmClient", lambda *args, **kwargs: fake)
    monkeypatch.setattr(cli_module, "resolve_runtime_config", lambda **kwargs: DummyConfig())
    exit_code = cli_module.main(["--json", "--base-url", "http://example", "--api-key", "k", "subject", "list"])
    assert exit_code == EXIT_CONFLICT
    assert json.loads(capsys.readouterr().out) == {"error": {"code": "conflict", "message": "conflict happened"}}


def test_cli_setup_command(monkeypatch, tmp_path, capsys):
    from czm_cli.commands import setup as setup_module

    config_path = tmp_path / "config.toml"

    def fake_bootstrap_config(**kwargs):
        config_path.write_text("base_url = \"http://localhost:8000\"\napi_key = \"secret\"\ntimezone = \"UTC\"\n", encoding="utf-8")
        assert kwargs["base_url"] == "http://localhost:8000"
        assert kwargs["username"] == "admin"
        assert kwargs["password"] == "admin"
        assert kwargs["api_key_name"] == "czm-cli"
        assert kwargs["config_path"] == config_path
        return type("R", (), {"config_path": config_path, "base_url": kwargs["base_url"], "username": kwargs["username"], "api_key_name": kwargs["api_key_name"], "timezone": kwargs["timezone"]})()

    monkeypatch.setattr(setup_module, "bootstrap_config", fake_bootstrap_config)
    exit_code = cli_module.main(["setup", "--base-url", "http://localhost:8000", "--config", str(config_path)])
    assert exit_code == 0
    assert "Wrote config to" in capsys.readouterr().out
    assert config_path.exists()
