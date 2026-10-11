# -*- coding: utf-8 -*-
"""题库大规模生成器 v2:计算题+应用题模板化生成,全部程序验算
目标:把32个知识点中可程序化的扩到每知识点30-50题
用法: python 题库生成器2.py
"""
import json, random, sys
from fractions import Fraction
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

RAW = r'D:\老谭项目总览\04-工具脚本\math_questions_raw.json'

def F(n, d=1):
    return Fraction(n, d)

def calc(stem, ans, explain):
    return {"type": "calc", "stem": stem, "answer": str(ans), "explain": explain}

def gen_many(kind, count):
    """kind: 生成函数(每次返回一道题 dict)"""
    return [kind() for _ in range(count)]

def q_f1():  # 分数乘整数(含应用)
    d = random.choice([5, 6, 7, 8, 9, 10, 12, 15, 16, 18])
    n = random.randint(1, d - 1)
    m = random.choice([3, 4, 5, 6, 7, 8, 9, 12])
    a = F(n * m, d)
    return calc(f"计算:{n}/{d} × {m} =", a, f"分子{n}乘整数{m}得{n*m},约分:{n*m}/{d} = {a}")

def q_f1app():  # 分数乘法应用题
    things = [('书', '页'), ('绳子', '米'), ('路', '千米'), ('糖果', '袋'), ('面粉', '千克')]
    t, u = random.choice(things)
    total = random.choice([18, 24, 30, 36, 40, 45, 48, 60])
    d = random.choice([3, 4, 5, 6, 8, 9])
    n = random.randint(1, d - 1)
    a = F(total * n, d)
    return calc(f"一{t}共 {total} {u},用了其中的 {n}/{d},用了多少{u}?",
                a, f"{total} × {n}/{d} = {total*n}/{d} = {a}{u}")

def q_f2():  # 分数乘分数
    d1 = random.choice([3, 4, 5, 6, 8, 9])
    d2 = random.choice([4, 5, 6, 7, 8, 9, 10])
    n1 = random.randint(1, d1 - 1)
    n2 = random.randint(1, d2 - 1)
    a = F(n1 * n2, d1 * d2)
    return calc(f"计算:{n1}/{d1} × {n2}/{d2} =", a, f"分子乘分子、分母乘分母:{n1*n2}/{d1*d2},约分得 {a}")

def q_f2app():  # 分数乘分数应用
    things = [('长方形地', '长', '米', '宽', '米', '面积', '平方米'),
              ('长方形桌布', '长', '分米', '宽', '分米', '面积', '平方分米')]
    t, l1, u1, l2, u2, rn, ru = random.choice(things)
    d1, d2 = random.choice([3, 4, 5, 6, 8]), random.choice([3, 4, 5, 6, 8])
    n1, n2 = random.randint(1, d1 - 1), random.randint(1, d2 - 1)
    a = F(n1 * n2, d1 * d2)
    return calc(f"一块{t}{l1}{n1}/{d1}{u1},{l2}{n2}/{d2}{u2},它的{rn}是多少{ru}?",
                a, f"{n1}/{d1} × {n2}/{d2} = {a} {ru}")

def q_d2():  # 分数除以整数
    d = random.choice([3, 4, 5, 6, 7, 8, 9, 10])
    n = random.randint(1, d - 1)
    m = random.choice([2, 3, 4, 5, 6])
    a = F(n, d * m)
    return calc(f"计算:{n}/{d} ÷ {m} =", a, f"除以整数等于乘它的倒数:{n}/{d} × 1/{m} = {a}")

def q_d3():  # 一个数除以分数
    a_int = random.choice([2, 3, 4, 5, 6, 8, 9, 12])
    d2 = random.choice([3, 4, 5, 7, 8, 9])
    n2 = random.randint(1, d2 - 1)
    a = F(a_int) / F(n2, d2)
    return calc(f"计算:{a_int} ÷ {n2}/{d2} =", a, f"除以分数等于乘它的倒数:{a_int} × {d2}/{n2} = {a}")

def q_d5app():  # 已知一个数的几分之几求这个数
    things = [('看书', '页', '全书'), ('修路', '米', '这条路'), ('卖水果', '千克', '这筐水果')]
    act, u, whole = random.choice(things)
    part = random.choice([12, 15, 18, 20, 24, 30, 36, 42])
    d = random.choice([3, 4, 5, 6, 7])
    n = random.randint(1, d - 1)
    a = F(part) / F(n, d)
    return calc(f"{act}用了 {part} {u},正好是{whole}的 {n}/{d},{whole}一共多少{u}?",
                a, f"{part} ÷ {n}/{d} = {part} × {d}/{n} = {a} {u}")

def q_b3app():  # 按比例分配
    ctx = [('果园种苹果树和梨树', '棵'), ('学校买篮球和足球', '个'), ('工地运水泥和沙子', '吨')]
    c, u = random.choice(ctx)
    total = random.choice([60, 90, 120, 150, 180, 240])
    x, y = random.choice([(2, 3), (3, 4), (2, 5), (3, 5), (4, 5), (1, 3)])
    a1 = F(total * x, x + y)
    a2 = F(total * y, x + y)
    return calc(f"{c}共 {total} {u},按 {x}:{y} 分配,各多少{u}?",
                f"第一种{a1}{u},第二种{a2}{u}",
                f"总份数 {x}+{y}={x+y},每份 {total}÷{x+y}={F(total,x+y)},{x}份={a1}{u},{y}份={a2}{u}")

def q_pc4app():  # 求一个数比另一个数多(少)百分之几
    ctx = [('原价', '现价', '元', '降价'), ('去年', '今年', '台', '增产')]
    b, c, u, act = random.choice(ctx)
    a1 = random.choice([100, 120, 150, 200, 240, 300])
    a2 = random.choice([80, 90, 96, 100, 125, 160])
    if act == '降价':
        a1, a2 = max(a1, a2), min(a1, a2)
    else:
        a1, a2 = min(a1, a2), max(a1, a2)
    diff = abs(a2 - a1)
    pct = F(diff * 100, a1)
    return calc(f"一件商品{b}{a1}{u},{c}{a2}{u},{act}了百分之几?",
                f"{pct}%",
                f"相差 {a2}-{a1}={diff},{diff}÷{a1}={pct}%")

def q_pc5app():  # 求比一个数多(少)百分之几的数
    p = random.choice([10, 20, 25, 30, 40, 50])
    base = random.choice([80, 100, 120, 200, 240])
    up = random.choice([True, False])
    a = F(base * (100 + p), 100) if up else F(base * (100 - p), 100)
    word = '涨' if up else '降'
    return calc(f"一件商品原价 {base} 元,价格{word}了 {p}%,现在的价格是多少元?",
                a, f"{base} × (1 ± {p}%) = {a} 元")

def q_c2():  # 圆周长
    r = random.choice([1, 2, 3, 4, 5, 6, 8, 10, 2.5, 3.5, 4.5])
    ask = random.choice(['r', 'd'])
    if ask == 'r':
        ans = round(2 * 3.14 * r, 2)
        return calc(f"一个圆的半径是 {r} 厘米,它的周长是多少厘米?(π取3.14)",
                    ans, f"C=2πr=2×3.14×{r}={ans} 厘米")
    d = 2 * r
    ans = round(3.14 * d, 2)
    return calc(f"一个圆的直径是 {d} 厘米,它的周长是多少厘米?(π取3.14)",
                ans, f"C=πd=3.14×{d}={ans} 厘米")

def q_c2app():  # 圆周长应用(车轮)
    d = random.choice([40, 50, 60, 70, 80])
    circles = random.choice([100, 200, 500, 1000])
    dist_cm = 3.14 * d * circles
    a = round(dist_cm / 100, 1)
    return calc(f"一辆自行车车轮直径 {d} 厘米,车轮转了 {circles} 圈,前进了多少米?(π取3.14)",
                a, f"一圈长 3.14×{d}={round(3.14*d,1)} 厘米,{circles} 圈共 {round(dist_cm,1)} 厘米 = {a} 米")

def q_c3():  # 圆面积
    r = random.choice([2, 3, 4, 5, 6, 8, 10])
    a = round(3.14 * r * r, 2)
    return calc(f"一个圆的半径是 {r} 厘米,它的面积是多少平方厘米?(π取3.14)",
                a, f"S=πr²=3.14×{r}×{r}={a} 平方厘米")

def q_c4():  # 圆环面积
    R = random.choice([6, 8, 10, 12])
    r = R - random.choice([2, 3, 4])
    a = round(3.14 * (R * R - r * r), 2)
    return calc(f"一个圆环,外圆半径 {R} 厘米,内圆半径 {r} 厘米,圆环的面积是多少平方厘米?(π取3.14)",
                a, f"S=π(R²-r²)=3.14×({R*R}-{r*r})={a} 平方厘米")

def q_pc3():  # 求一个数是另一个数的百分之几
    a1 = random.choice([20, 25, 30, 40, 45, 50, 60, 75])
    a2 = random.choice([50, 80, 100, 120, 150, 200])
    pct = F(a1 * 100, a2)
    ctx = random.choice([('班上有男生', '人,全班', '人,男生占全班的百分之几?'),
                         ('修路队修了', '米,全长', '米,修了全长的百分之几?')])
    return calc(f"{ctx[0]}{a1}{ctx[1]}{a2}{ctx[2]}", f"{pct}%",
                f"{a1}÷{a2}={pct}%")

def gen_point(pid, funcs, per):
    """对知识点批量生成(多模板轮换)"""
    qs = []
    for i in range(per):
        f = funcs[i % len(funcs)]
        q = f()
        if isinstance(q, list):
            qs.extend(q)
        else:
            qs.append(q)
    return qs

def main():
    data = json.load(open(RAW, encoding='utf-8'))
    plan = {
        'f1': ([q_f1, q_f1app], 40),
        'f2': ([q_f2, q_f2app], 40),
        'd2': ([q_d2], 35),
        'd3': ([q_d3], 35),
        'd5': ([q_d5app], 35),
        'b3': ([q_b3app], 35),
        'pc3': ([q_pc3], 35),
        'pc4': ([q_pc4app], 35),
        'pc5': ([q_pc5app], 35),
        'c2': ([q_c2, q_c2app], 40),
        'c3': ([q_c3], 35),
        'c4': ([q_c4], 35),
    }
    total = 0
    for pid, (funcs, per) in plan.items():
        entry = next((x for x in data if x['id'] == pid), None)
        if entry is None:
            print(f'{pid}: 不存在,跳过', flush=True)
            continue
        new = gen_point(pid, funcs, per)
        old = entry.get('questions', [])
        stems = {q.get('stem') for q in old}
        added = [q for q in new if q['stem'] not in stems]
        entry['questions'] = old + added
        total += len(added)
        print(f'{pid}({entry["name"]}): +{len(added)} (共{len(entry["questions"])})', flush=True)
    json.dump(data, open(RAW, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'共新增 {total} 题 → {RAW}', flush=True)

if __name__ == '__main__':
    main()
