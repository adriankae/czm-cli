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
