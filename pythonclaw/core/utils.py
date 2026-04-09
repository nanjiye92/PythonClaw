"""
PythonClaw 的共享工具函数。
"""

from __future__ import annotations


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """
    从 *content* 中解析由 '---' 分隔的 YAML 风格前置内容。

    返回 (metadata_dict, body_string)。
    如果没有找到前置内容，返回 ({}, content)。

    支持：
      - 简单的 ``key: value`` 键值对
      - 带有缩进续行的 YAML 块标量（``>``, ``|``）
      - 裸多行值（没有 ``>`` / ``|`` 的缩进续行）
    """
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    metadata: dict[str, str] = {}
    current_key: str | None = None
    current_lines: list[str] = []
    block_mode: str | None = None  # ">" (折叠) 或 "|" (字面)

    def _flush() -> None:
        if current_key is not None and current_lines:
            text = " ".join(current_lines) if block_mode == ">" else "\n".join(current_lines)
            metadata[current_key] = text.strip()

    for line in parts[1].strip().splitlines():
        stripped = line.strip()

        # 续行（以空白字符开头且当前有键）
        if line and line[0] in (" ", "\t") and current_key is not None:
            current_lines.append(stripped)
            continue

        # 新的键值对
        if ":" in stripped:
            _flush()
            key, _, value = stripped.partition(":")
            current_key = key.strip()
            value = value.strip()

            if value in (">", "|"):
                block_mode = value
                current_lines = []
            elif value:
                block_mode = None
                current_lines = [value]
            else:
                block_mode = None
                current_lines = []

    _flush()

    return metadata, parts[2].strip()
