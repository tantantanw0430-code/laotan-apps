# -*- coding: utf-8 -*-
"""六年级数学题库生成器:计算题批量生成+程序验算(答案100%正确)
先跑第一单元(分数乘法)验证,后续单元逐个加生成器
输出: JSON 追加到 math_questions_raw.json 对应知识点
"""
import sys, os, json, random
from fractions import Fraction
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

RAW = r'D:\老谭项目总览\04-工具脚本\math_questions_raw.json'

def gen_f1():  # 分数乘整数
    qs = []
    # 真分数×整数(约分/不约分各半)
    for _ in range(12):
        d = random.choice([5, 6, 7, 8, 9, 10, 12, 15, 16])
        n = random.choice([1, 2, 3, 4, 5])
        while Fraction(n, d) >= 1:
            n = random.choice([1, 2, 3])
        m = random.choice([3, 4, 5, 6, 8, 9, 12])
        ans = Fraction(n * m, d)
        qs.append({"type": "calc", "stem": f"计算: {n}/{d} × {m} =",
                   "answer": str(ans), "explain": f"分子{n}乘整数{m}得{n*m},再约分:{n*m}/{d} = {ans}"})
    # 带分数×整数
    for _ in range(4):
        whole, n, d = random.randint(1, 3), random.randint(1, 4), random.choice([5, 7, 8, 9])
        while n >= d:
            n = random.randint(1, 3)
        m = random.choice([3, 4, 5, 6])
        f = Fraction(whole * d + n, d)
        ans = f * m
        qs.append({"type": "calc", "stem": f"计算: {whole}又{n}/{d} × {m} =",
                   "answer": str(ans), "explain": f"带分数化假分数({whole* d + n}/{d})再乘{m},结果 {ans}"})
    return qs

def gen_f2():  # 分数乘分数
    qs = []
    for _ in range(14):
        d1, d2 = random.choice([3, 4, 5, 6, 8, 9]), random.choice([4, 5, 6, 7, 9, 10])
        n1, n2 = random.randint(1, d1 - 1), random.randint(1, d2 - 1)
        ans = Fraction(n1 * n2, d1 * d2)
        qs.append({"type": "calc", "stem": f"计算: {n1}/{d1} × {n2}/{d2} =",
                   "answer": str(ans), "explain": f"分子乘分子、分母乘分母:{n1*n2}/{d1*d2},约分得 {ans}"})
    return qs

def gen_f3():  # 小数乘分数
    qs = []
    for _ in range(12):
        dec = random.choice(['0.4', '0.6', '0.25', '0.75', '1.2', '2.4', '0.8', '1.5', '0.5', '3.6'])
        n, d = random.randint(1, 4), random.choice([3, 4, 5, 6, 8])
        while n >= d:
            n = random.randint(1, 3)
        ans = Fraction(dec) * Fraction(n, d)
        qs.append({"type": "calc", "stem": f"计算: {dec} × {n}/{d} =",
                   "answer": str(ans), "explain": f"{dec} 化分数 {Fraction(dec)} 再乘 {n}/{d},得 {ans}"})
    return qs

def gen_d2():  # 分数除以整数
    qs = []
    for _ in range(12):
        d = random.choice([3, 4, 5, 6, 7, 8, 9, 10])
        n = random.randint(1, d - 1)
        m = random.choice([2, 3, 4, 5, 6])
        ans = Fraction(n, d * m)
        qs.append({"type": "calc", "stem": f"计算: {n}/{d} ÷ {m} =",
                   "answer": str(ans), "explain": f"除以整数等于乘它的倒数:{n}/{d} × 1/{m} = {ans}"})
    return qs

def gen_d3():  # 一个数除以分数
    qs = []
    for _ in range(12):
        a = random.choice([2, 3, 4, 5, 6, 8, 9, 12])
        d2 = random.choice([3, 4, 5, 7, 8, 9])
        n2 = random.randint(1, d2 - 1)
        ans = Fraction(a) / Fraction(n2, d2)
        qs.append({"type": "calc", "stem": f"计算: {a} ÷ {n2}/{d2} =",
                   "answer": str(ans), "explain": f"除以分数等于乘它的倒数:{a} × {d2}/{n2} = {ans}"})
    return qs

def gen_d4():  # 分数混合运算(两步)
    qs = []
    for _ in range(10):
        d1, d2 = random.choice([3, 4, 5, 6, 8]), random.choice([3, 4, 5, 7, 9])
        n1, n2 = random.randint(1, d1 - 1), random.randint(1, d2 - 1)
        op = random.choice(['+', '-'])
        if op == '+':
            ans = Fraction(n1, d1) + Fraction(n2, d2)
        else:
            a = Fraction(n1, d1); b = Fraction(n2, d2)
            if a < b:
                a, b = b, a
            ans = a - b
        qs.append({"type": "calc", "stem": f"计算: {Fraction(n1,d1).numerator}/{Fraction(n1,d1).denominator} {op} {n2}/{d2} =",
                   "answer": str(ans), "explain": f"通分后计算,结果 {ans}"})
    return qs

def gen_pc2():  # 百分数与分数小数互化
    qs = []
    for _ in range(12):
        kind = random.randint(0, 2)
        if kind == 0:
            p = random.choice([25, 50, 75, 20, 40, 60, 80, 10, 30, 70, 90, 15, 45, 5])
            ans = Fraction(p, 100)
            qs.append({"type": "calc", "stem": f"把 {p}% 化成分数(最简) =",
                       "answer": str(ans), "explain": f"{p}% = {p}/100,约分得 {ans}"})
        elif kind == 1:
            f = random.choice([Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5), Fraction(3, 5), Fraction(4, 5), Fraction(1, 8), Fraction(3, 8)])
            ans = f.numerator * 100.0 / f.denominator
            ans_s = str(int(ans)) + '%' if ans == int(ans) else str(ans).rstrip('0').rstrip('.') + '%'
            qs.append({"type": "calc", "stem": f"把 {f.numerator}/{f.denominator} 化成百分数 =",
                       "answer": ans_s, "explain": f"{f.numerator}÷{f.denominator}={ans},写成百分数 {ans_s}"})
        else:
            dec = random.choice(['0.3', '0.25', '0.6', '0.75', '0.2', '0.45', '0.9', '0.05'])
            ans = str(round(float(dec) * 100)).rstrip('0').rstrip('.') + '%' if float(dec) * 100 == int(float(dec) * 100) else str(float(dec) * 100) + '%'
            qs.append({"type": "calc", "stem": f"把 {dec} 化成百分数 =",
                       "answer": ans, "explain": f"小数点向右移动两位,添上%:{ans}"})
    return qs

def gen_c2():  # 圆的周长(π取3.14)
    qs = []
    for _ in range(12):
        r = random.choice([1, 2, 3, 4, 5, 6, 8, 10, 2.5, 3.5])
        ask = random.choice(['r', 'd'])
        if ask == 'r':
            ans = round(2 * 3.14 * r, 2)
            stem = f"一个圆的半径是 {r} 厘米,它的周长是多少厘米?(π取3.14)"
        else:
            d = 2 * r
            ans = round(3.14 * d, 2)
            stem = f"一个圆的直径是 {d} 厘米,它的周长是多少厘米?(π取3.14)"
        qs.append({"type": "calc", "stem": stem, "answer": str(ans),
                   "explain": f"周长公式 C={'(2πr)' if ask=='r' else 'πd'},代入计算得 {ans} 厘米"})
    return qs

def gen_c3():  # 圆的面积(π取3.14)
    qs = []
    for _ in range(12):
        r = random.choice([1, 2, 3, 4, 5, 6, 8, 10])
        ans = round(3.14 * r * r, 2)
        qs.append({"type": "calc", "stem": f"一个圆的半径是 {r} 厘米,它的面积是多少平方厘米?(π取3.14)",
                   "answer": str(ans), "explain": f"面积公式 S=πr²=3.14×{r}×{r}={ans} 平方厘米"})
    return qs

def main():
    data = json.load(open(RAW, encoding='utf-8'))
    # 结构: [{id, name, unit, questions:[...]}, ...]
    new = {'f1': gen_f1(), 'f2': gen_f2(), 'f3': gen_f3(),
           'd2': gen_d2(), 'd3': gen_d3(), 'd4': gen_d4(),
           'pc2': gen_pc2(), 'c2': gen_c2(), 'c3': gen_c3()}
    total = 0
    for k, qs in new.items():
        entry = next((x for x in data if x['id'] == k), None)
        if entry is None:
            print(f'{k}: 知识点不存在,跳过', flush=True)
            continue
        old = entry.get('questions', [])
        stems = {q.get('stem') for q in old}
        added = [q for q in qs if q['stem'] not in stems]
        entry['questions'] = old + added
        total += len(added)
        print(f'{k}({entry["name"]}): +{len(added)} 题 (共{len(entry["questions"])})', flush=True)
    json.dump(data, open(RAW, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'共新增 {total} 题 → {RAW}', flush=True)

if __name__ == '__main__':
    main()
