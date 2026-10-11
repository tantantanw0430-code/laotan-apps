# -*- coding: utf-8 -*-
"""把知识点+题库合并进练习器 HTML(正则替换,可重复执行)"""
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HTML = r'D:\老谭项目总览\04-工具脚本\六年级数学练习器.html'
points = json.load(open(r'D:\老谭项目总览\04-工具脚本\math_points.json', encoding='utf-8'))
bank_raw = json.load(open(r'D:\老谭项目总览\04-工具脚本\math_questions_raw.json', encoding='utf-8'))

units_js = json.dumps(points['units'], ensure_ascii=False)
bank = {x['id']: x['questions'] for x in bank_raw}
bank_js = json.dumps(bank, ensure_ascii=False)

# 清理 JS 源码里非法的行分隔符(mimo 生成的文本可能带 U+2028/U+2029,JSON 合法但 JS 字符串字面量非法)
def sanitize(s):
    return s.replace('\u2028', ' ').replace('\u2029', ' ').replace('\x0b', ' ').replace('\x0c', ' ').replace('\x85', ' ')
units_js = sanitize(units_js)
bank_js = sanitize(bank_js)

html = open(HTML, encoding='utf-8').read()
# 用 lambda 避免 re.sub 把 replacement 里的 \n 转义成真实换行
html = re.sub(r'var UNITS = .*?;\n', lambda m: 'var UNITS = ' + units_js + ';\n', html, count=1, flags=re.S)
html = re.sub(r'var BANK = .*?;\n', lambda m: 'var BANK = ' + bank_js + ';\n', html, count=1, flags=re.S)
open(HTML, 'w', encoding='utf-8').write(html)
print(f'合并完成: {len(bank)} 个知识点, 共 {sum(len(v) for v in bank.values())} 题')
