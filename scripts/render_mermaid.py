#!/usr/bin/env python3
"""把 markdown 裡的 ```mermaid 區塊換成 SVG 圖片連結。

為什麼不直接用 `mmdc -i book.md`：mermaid-cli 的 markdown 模式一張圖語法錯就整本中止，
而這三本書是 AI 寫的，256 張圖裡有幾張語法壞掉。這裡逐張渲染，壞的原樣保留成程式碼區塊。
渲染結果用內容 hash 快取，所以只有改過的圖會重畫。

用法：render_mermaid.py <in.md> <out.md> <svg 目錄> [mmdc 路徑]
"""
import hashlib, pathlib, re, subprocess, sys, os

BLOCK = re.compile(r'^```mermaid[^\n]*\n(.*?)^```\s*$', re.S | re.M)
# htmlLabels: WeasyPrint 不支援 SVG 的 <foreignObject>，不關的話圖上的字會不見。
# fontFamily: mermaid 預設 "trebuchet ms"，中文會 fallback 到蘋方 —— 而蘋方在 PDF 裡的
#   字型名是中文，正是一開始整份變方塊的原因。圖裡的字型也得一起釘死。
CONFIG = ('{"flowchart":{"htmlLabels":false},"htmlLabels":false,"theme":"neutral",'
          '"fontFamily":"Noto Sans CJK TC",'
          '"themeVariables":{"fontFamily":"Noto Sans CJK TC","fontSize":"15px"}}')
CHROME = os.environ.get('CHROME', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')


VIEWBOX = re.compile(r'<svg\b[^>]*?viewBox="[\d.]+ [\d.]+ ([\d.]+) ([\d.]+)"', re.S)

def fix_size(svg: pathlib.Path) -> None:
    """mermaid 吐的是 width="100%"，排進 PDF 會被撐滿整個版面寬，一張兩個框的圖佔掉半頁。
    改成 viewBox 的實際 px 尺寸，讓 CSS 的 max-width 只負責「太大才縮」。"""
    t = svg.read_text(encoding='utf-8')
    m = VIEWBOX.search(t)
    if not m or 'width="100%"' not in t:
        return
    w, h = float(m.group(1)), float(m.group(2))
    svg.write_text(t.replace('width="100%"', f'width="{w:.0f}px" height="{h:.0f}px"', 1), encoding='utf-8')

def render(code: str, out: pathlib.Path, mmdc: str, cfg: pathlib.Path) -> bool:
    if out.exists():
        fix_size(out)       # 舊快取也補上尺寸，不必為此重畫
        return True
    src = out.with_suffix('.mmd')
    src.write_text(code, encoding='utf-8')
    r = subprocess.run([mmdc, '-i', str(src), '-o', str(out), '-c', str(cfg), '-e', 'svg', '-q'],
                       capture_output=True, text=True,
                       env={**os.environ, 'PUPPETEER_EXECUTABLE_PATH': CHROME})
    if r.returncode != 0 or not out.exists():
        return False
    fix_size(out)
    return True

def main(inp, outp, svgdir, mmdc='mmdc'):
    svgdir = pathlib.Path(svgdir); svgdir.mkdir(parents=True, exist_ok=True)
    cfg = svgdir / 'mmdc.json'; cfg.write_text(CONFIG, encoding='utf-8')
    ok = bad = 0

    def sub(m):
        nonlocal ok, bad
        code = m.group(1)
        svg = svgdir / (hashlib.sha1((CONFIG + code).encode()).hexdigest()[:12] + '.svg')
        if render(code, svg, mmdc, cfg):
            ok += 1
            return f'![]({svgdir.name}/{svg.name})'
        bad += 1
        return m.group(0)          # 畫不出來就留原樣，至少讀者看得到圖的描述

    text = BLOCK.sub(sub, pathlib.Path(inp).read_text(encoding='utf-8'))
    pathlib.Path(outp).write_text(text, encoding='utf-8')
    print(f'    圖 {ok} 張 OK' + (f'，{bad} 張語法有問題（保留原始碼）' if bad else ''))

def demo():
    md = '```mermaid\nflowchart LR\n  A-->B\n```\n\n```python\n# 不是圖\n```\n'
    assert len(BLOCK.findall(md)) == 1, BLOCK.findall(md)
    assert BLOCK.findall(md)[0] == 'flowchart LR\n  A-->B\n'
    import tempfile
    d = pathlib.Path(tempfile.mkdtemp()) / 'x.svg'
    d.write_text('<svg width="100%" viewBox="0 0 300 150" style="max-width:300px"></svg>', encoding='utf-8')
    fix_size(d)
    assert 'width="300px" height="150px"' in d.read_text(encoding='utf-8'), d.read_text(encoding='utf-8')
    fix_size(d)   # 冪等
    assert d.read_text(encoding='utf-8').count('width=') == 1
    print('render_mermaid ok')

if __name__ == '__main__':
    if sys.argv[1] == 'demo':
        demo()
    else:
        main(*sys.argv[1:])
