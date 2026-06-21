#!/usr/bin/env python3
"""拉取 Hanzi Writer 字符数据并生成内嵌 JS。"""
import json
import urllib.request
import urllib.parse
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
CHAR_LIST_PATH = ROOT / 'scripts' / 'char_list.json'
DATA_DIR = ROOT / 'data'
DATA_DIR.mkdir(exist_ok=True)

def main():
    with open(CHAR_LIST_PATH, 'r', encoding='utf-8') as f:
        levels = json.load(f)['levels']

    unique_chars = sorted({c for lvl in levels for c in lvl['chars']})
    print(f'共 {len(unique_chars)} 个唯一汉字: {", ".join(unique_chars)}')

    data = {}
    failed = []
    for i, char in enumerate(unique_chars, 1):
        url = f'https://cdn.jsdelivr.net/npm/hanzi-writer-data@latest/{urllib.parse.quote(char)}.json'
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                data[char] = json.loads(resp.read().decode('utf-8'))
            print(f'[{i}/{len(unique_chars)}] ✓ {char}')
        except Exception as e:
            print(f'[{i}/{len(unique_chars)}] ✗ {char}: {e}')
            failed.append(char)

    if failed:
        print(f'失败 {len(failed)} 个: {failed}')
        return 1

    # 保存完整数据
    data_path = DATA_DIR / 'hanzi_data.json'
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    print(f'已保存 {data_path}, 大小 {data_path.stat().st_size} bytes')

    # 生成可内嵌的 JS 字符串片段
    js_path = DATA_DIR / 'hanzi_data.js'
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write('const HANZI_DATA = ')
        f.write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
        f.write(';\n')
    print(f'已保存 {js_path}, 大小 {js_path.stat().st_size} bytes')

    return 0

if __name__ == '__main__':
    raise SystemExit(main())
