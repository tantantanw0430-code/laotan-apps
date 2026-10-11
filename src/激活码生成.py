# -*- coding: utf-8 -*-
"""六年级练习器·专属版生成器
用法: python 激活码生成.py <买家昵称>
输出: 04-工具脚本/发货/<昵称>-六年级数学练习器.html(内含唯一激活码+水印)
登记: 07-交易日志/激活码登记.txt
"""
import sys, os, random, string, datetime
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC = r'D:\老谭项目总览\04-工具脚本\六年级数学练习器.html'
OUT_DIR = r'D:\老谭项目总览\04-工具脚本\发货'
REG = r'D:\老谭项目总览\07-交易日志\激活码登记.txt'

ALPHABET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'  # 去掉 0O1I 易混淆

def gen_code():
    return '-'.join(''.join(random.choices(ALPHABET, k=4)) for _ in range(3))

def main():
    owner = sys.argv[1] if len(sys.argv) > 1 else ''
    if not owner:
        print('用法: python 激活码生成.py <买家昵称>')
        sys.exit(1)
    code = gen_code()
    html = open(SRC, encoding='utf-8').read()
    old = 'var ACTIVATION = {};'
    new = 'var ACTIVATION = {' + f'"{code}": {{ owner: "{owner}", devices: 3 }}' + '};'
    if old not in html:
        print('[错误] 源文件里没找到码表占位,检查激活系统代码', flush=True)
        sys.exit(1)
    html = html.replace(old, new, 1)

    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, f'{owner}-六年级数学练习器.html')
    open(out, 'w', encoding='utf-8').write(html)

    with open(REG, 'a', encoding='utf-8') as f:
        f.write(f'{datetime.date.today().strftime("%Y-%m-%d")}\t{owner}\t{code}\t3台\n')
    print(f'[生成] {out}', flush=True)
    print(f'[激活码] {code} (限3台设备)', flush=True)
    print(f'[登记] 已记入 {REG}', flush=True)

if __name__ == '__main__':
    main()
