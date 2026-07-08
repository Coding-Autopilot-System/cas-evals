import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

from cas_evals.registry_check import RegistryCheckError, check_registry_urls, main


def _fake_response(status_code):
    response = MagicMock()
    response.status = status_code
    response.read.return_value = b""
    response.__enter__.return_value = response
    response.__exit__.return_value = False
    return response


class RegistryCheckTests(unittest.TestCase):
    def test_all_paths_return_200(self):
        with patch("cas_evals.registry_check.urlopen", return_value=_fake_response(200)) as urlopen:
            results = check_registry_urls(
                "https://coding-autopilot-system.github.io/cas-contracts/registry",
                ["index.json", "v0.1/manifest.json"],
            )
        self.assertEqual(
            results,
            [("index.json", 200), ("v0.1/manifest.json", 200)],
        )
        self.assertEqual(urlopen.call_count, 2)

    def test_one_path_returns_404(self):
        responses = [_fake_response(200), _fake_response(404)]

        def side_effect(*args, **kwargs):
            return responses.pop(0)

        with patch("cas_evals.registry_check.urlopen", side_effect=side_effect):
            with self.assertRaises(RegistryCheckError) as ctx:
                check_registry_urls(
                    "https://coding-autopilot-system.github.io/cas-contracts/registry",
                    ["index.json", "v0.1/manifest.json"],
                )
        self.assertIn("v0.1/manifest.json", str(ctx.exception))
        self.assertIn("404", str(ctx.exception))

    def test_network_unavailable_raises_distinguishable_error(self):
        with patch("cas_evals.registry_check.urlopen", side_effect=URLError("no route to host")):
            with self.assertRaises(RegistryCheckError) as ctx:
                check_registry_urls(
                    "https://coding-autopilot-system.github.io/cas-contracts/registry",
                    ["index.json"],
                )
        self.assertIn("unavailable", str(ctx.exception).lower())
        self.assertNotIn("404", str(ctx.exception))

    def test_http_error_raises_registry_check_error(self):
        error = HTTPError("https://example.com/index.json", 500, "Internal Server Error", {}, None)
        with patch("cas_evals.registry_check.urlopen", side_effect=error):
            with self.assertRaises(RegistryCheckError) as ctx:
                check_registry_urls(
                    "https://coding-autopilot-system.github.io/cas-contracts/registry",
                    ["index.json"],
                )
        self.assertIn("500", str(ctx.exception))

    def test_main_exits_zero_on_success(self):
        with patch("cas_evals.registry_check.check_registry_urls") as mocked:
            mocked.return_value = [
                ("index.json", 200),
                ("v0.1/manifest.json", 200),
                ("v0.1/common.schema.json", 200),
                ("v0.1/evaluation-result.schema.json", 200),
            ]
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                exit_code = main([])
        self.assertEqual(exit_code, 0)
        output = buffer.getvalue()
        self.assertIn("index.json", output)
        self.assertIn("200", output)

    def test_main_exits_nonzero_on_failure(self):
        with patch(
            "cas_evals.registry_check.check_registry_urls",
            side_effect=RegistryCheckError("v0.1/manifest.json returned HTTP 404"),
        ):
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                exit_code = main([])
        self.assertEqual(exit_code, 1)


if __name__ == "__main__":
    unittest.main()
