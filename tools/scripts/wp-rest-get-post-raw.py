#!/usr/bin/env python3
import base64
import json
import sys
import urllib.request
from pathlib import Path


def load_dotenv(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        env[key.strip()] = val.strip().strip('"').strip("'")
    return env


post_id = int(sys.argv[1])
env = load_dotenv(Path(__file__).resolve().parents[2] / ".env")
auth = base64.b64encode(
    f"{env['ROOTSANDFRUIT_MCP_USERNAME']}:{env['ROOTSANDFRUIT_MCP_PASSWORD']}".encode()
).decode()
req = urllib.request.Request(
    f"https://rootsandfruit.com/wp-json/wp/v2/posts/{post_id}?context=edit",
    headers={"Authorization": f"Basic {auth}"},
)
post = json.loads(urllib.request.urlopen(req, timeout=60).read().decode("utf-8"))
content = post.get("content", {}).get("raw", "")
out = Path(__file__).resolve().parent / f".tmp-post-{post_id}-raw.txt"
out.write_text(content, encoding="utf-8")
print("raw len", len(content))
markers = {
    "code-block-pro": content.count("code-block-pro"),
    "wp-block-code": content.count("wp-block-code"),
    "is-style-stripes": content.count("is-style-stripes"),
    "shiki": content.count("shiki"),
}
print(json.dumps(markers))
