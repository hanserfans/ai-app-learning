"""本机 HTTP 请求演示，无外网依赖，不使用真实模型接口。"""

import json
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import Request, urlopen


class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parts = urlsplit(self.path)
        if parts.path == "/lesson":
            topic = parse_qs(parts.query).get("topic", ["HTTP"])[0]
            status = 200
            payload = {"topic": topic, "minutes": 30}
        else:
            status = 404
            payload = {"error": "not_found"}
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # 让教学输出聚焦于请求结果。
        pass


@contextmanager
def local_server():
    # 仅监听本机；端口 0 表示由操作系统分配可用端口。
    server = ThreadingHTTPServer(("127.0.0.1", 0), DemoHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def get_json(url: str) -> dict:
    request = Request(url, headers={"Accept": "application/json"}, method="GET")
    with urlopen(request, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    with local_server() as base_url:
        query = urlencode({"topic": "Python 入门"})
        print("GET 成功：", get_json(f"{base_url}/lesson?{query}"))
        try:
            get_json(f"{base_url}/missing")
        except HTTPError as error:
            print(f"HTTP 失败：{error.code}")
            error.close()
        except (URLError, TimeoutError) as error:
            print(f"连接失败：{error}")
        except (ValueError, UnicodeError) as error:
            print(f"响应内容无法解析：{error}")


if __name__ == "__main__":
    main()
