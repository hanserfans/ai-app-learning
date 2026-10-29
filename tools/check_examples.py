"""离线检查教学示例：语法、运行结果和关键失败边界。"""

import ast
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_example(name):
    path = ROOT / "examples" / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    examples = sorted((ROOT / "examples").glob("*.py"))
    for path in [*examples, Path(__file__).resolve()]:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    environment = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    with tempfile.TemporaryDirectory() as temporary:
        data_path = Path(temporary) / "records.json"
        for path in examples:
            command = [sys.executable, str(path)]
            if path.name == "03_files_and_errors.py":
                command.extend(["--path", str(data_path)])
            result = subprocess.run(
                command, cwd=ROOT, env=environment,
                capture_output=True, text=True, encoding="utf-8", timeout=20,
            )
            require(result.returncode == 0, f"{path.name} failed: {result.stderr}")
            require(bool(result.stdout.strip()), f"{path.name} produced no output")
            print(f"PASS run: {path.name}")

        functions = load_example("02_functions.py")
        require(functions.summarize_minutes([30, 45, 60], 120)["total"] == 135, "wrong total")
        require(functions.summarize_minutes([])["average"] == 0, "empty input failed")
        try:
            functions.summarize_minutes([-1])
        except ValueError:
            pass
        else:
            raise RuntimeError("negative input accepted")

        files = load_example("03_files_and_errors.py")
        require(files.load_records(Path(temporary) / "missing.json") == [], "missing file failed")
        require(files.load_records(data_path)[0]["minutes"] == 30, "roundtrip failed")
        for invalid in ["{broken", "{}", '[{"topic":"x","minutes":-1}]']:
            data_path.write_text(invalid, encoding="utf-8")
            try:
                files.load_records(data_path)
            except ValueError:
                pass
            else:
                raise RuntimeError("invalid file accepted")

        http = load_example("04_http_demo.py")
        with http.local_server() as base_url:
            require(http.get_json(f"{base_url}/lesson")["minutes"] == 30, "GET failed")
            query = http.urlencode({"topic": "中文主题"})
            require(http.get_json(f"{base_url}/lesson?{query}")["topic"] == "中文主题", "query failed")
            try:
                http.get_json(f"{base_url}/missing")
            except HTTPError as error:
                require(error.code == 404, "wrong HTTP status")
                require(json.loads(error.read())["error"] == "not_found", "wrong error body")
                error.close()
            else:
                raise RuntimeError("404 did not raise")

    print("PASS boundaries: functions, JSON files, HTTP 200/404 and Chinese query")
    print("All example checks passed.")


if __name__ == "__main__":
    main()
