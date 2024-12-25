from dataclasses import dataclass
import graphviz

class BaseExpr:
    pass

@dataclass
class Literal(BaseExpr):
    n: bool

@dataclass
class Expr(BaseExpr):
    left: BaseExpr
    right: BaseExpr
    op: str

def parse_input(filename: str) -> dict[str, BaseExpr]:
    with open(filename, 'r') as file:
        data = file.read()
    res = {}
    [assignments, expressions] = data.split("\n\n")
    for a in assignments.split("\n"):
        [var, value] = a.replace(" ", "").split(":")
        res[var] = Literal(bool(int(value)))
    for e in expressions.split("\n"):
        [expr, var] = e.split(" -> ")
        [l, op, r] = expr.split(" ")
        res[var] = Expr(l, r, op)
    return res

def apply_op(op: str, left: bool, right: bool) -> bool:
    match op:
        case "OR":
            return left or right
        case "AND":
            return left and right
        case "XOR":
            return left ^ right

def evaluate(exprs: dict[str, BaseExpr], var: str, path: list[str] = []) -> bool:
    expr = exprs[var]
    if isinstance(expr, Literal):
        return expr.n
    
    if var in path:
        return False
    
    return apply_op(expr.op, 
                    evaluate(exprs, expr.left, path + [var]), 
                    evaluate(exprs, expr.right, path + [var]))

def eval_for_prefix(exprs: dict[str, BaseExpr], prefix: str) -> int:
    ps = {}
    for k in exprs:
        if k.startswith(prefix):
            ps[k] = evaluate(exprs, k)
    res = 0
    for i, (k, v) in enumerate(sorted(ps.items())):
        res += int(v) * pow(2, i)
    return res

def do_part_1(exprs: dict[str, BaseExpr]) -> int:
    return eval_for_prefix(exprs, "z")

def make_graph(filename: str) -> str:
    dot = graphviz.Digraph(comment='Day 24')
    with open(filename, 'r') as file:
        data = file.read()
    [_, expressions] = data.split("\n\n")
    for e in expressions.split("\n"):
        [expr, var] = e.split(" -> ")
        [l, op, r] = expr.split(" ")
        dot.node(var, var + " [" + op + "]")
        dot.edge(var, l)
        dot.edge(var, r)
    return dot.source

filename = "day24/input.txt"
exprs = parse_input(filename)
part1 = do_part_1(exprs)
print(part1)
dot_src = make_graph(filename)
print(dot_src)
# manually looked for anomalies...
part2 = ",".join(sorted(['z08', 'ffj', 'dwp', 'kfm', 'gjh', 'z22', 'z31', 'jdr']))
print(part2)