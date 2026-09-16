#!/usr/bin/env python3
"""把 ccc115a/se _more/mybook 的分節 md 依 README 目錄組成單一本書。"""
import re, sys, pathlib

LINK = re.compile(r'^(\s*)- \[(.+?)\]\((.+?\.md)\)\s*$')

def demote(txt: str) -> str:
    """標題降兩級，但跳過 fenced code block（裡面的 # 是 shell 註解不是標題）。"""
    out, fence = [], False
    for l in txt.splitlines():
        if l.lstrip().startswith(('```', '~~~')):
            fence = not fence          # ponytail: 單純開關，本書沒有巢狀 fence
        elif not fence:
            l = re.sub(r'^(#{1,4}) ', r'\1## ', l)
        out.append(l)
    return '\n'.join(out)

def build(src: pathlib.Path, out: pathlib.Path) -> int:
    lines = (src / 'README.md').read_text(encoding='utf-8').splitlines()
    title = next(l[2:].strip() for l in lines if l.startswith('# '))
    body, missing = [], 0
    for l in lines:
        m = LINK.match(l)
        if m:
            f = src / m.group(3)
            if not f.exists():
                missing += 1
                continue
            body += ['', demote(f.read_text(encoding='utf-8')).strip(), '']
        elif l.startswith('## '):                      # 篇
            body += ['', '# ' + l[3:].strip(), '']
        elif l.startswith('- ') and '](' not in l:      # 章
            body += ['', '## ' + l[2:].strip(), '']
    # 目錄裡的 1.1.md 連結在合併後失效，拆成純文字
    toc = re.sub(r'\[(.+?)\]\(.+?\.md\)', r'\1',
                 '\n'.join(l for l in lines if not l.startswith('# ')))
    out.write_text(f'# {title}\n\n## 目錄\n{toc}\n\n' + '\n'.join(body) + '\n', encoding='utf-8')
    return missing

def demo():
    assert demote('# A\n```\n# not a heading\n```\n## B') == '### A\n```\n# not a heading\n```\n#### B'
    assert demote('#nospace') == '#nospace'
    print('demote ok')

if __name__ == '__main__':
    if sys.argv[1] == 'demo':
        demo(); sys.exit()
    root, dest = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    dest.mkdir(parents=True, exist_ok=True)
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        o = dest / f'{d.name}.md'
        miss = build(d, o)
        print(f'{o.name}: {len(o.read_text(encoding="utf-8").splitlines())} 行, {o.stat().st_size//1024} KB'
              + (f', 缺 {miss} 個檔' if miss else ''))
