import os
import ast
import timeit
import cProfile
import pstats
import io
import math
import statistics
from tabulate import tabulate

# Composition Root imports
try:
    import baseline.main as baseline_app
    import optimised.main as optimised_app
except ImportError as e:
    print(f"Error: {e}. Ensure folders have __init__.py")

class ComplexityAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.cc = 1
        self.u_operators = set()
        self.u_operands = set()
        self.total_operands = 0

    def visit_FunctionDef(self, node):
        self.generic_visit(node)

    def visit_BinOp(self, node):
        self.u_operators.add(type(node.op))
        self.generic_visit(node)

    def visit_Name(self, node):
        self.u_operands.add(node.id)
        self.total_operands += 1
        self.generic_visit(node)

    def visit_DecisionPoint(self, node):
        self.cc += 1
        self.generic_visit(node)

    # Decision points for CC
    visit_If = visit_While = visit_For = visit_AsyncFor = visit_DecisionPoint
    visit_And = visit_Or = visit_ExceptHandler = visit_DecisionPoint

def calculate_metrics(file_path):
    with open(file_path, "r") as f:
        content = f.read()
        tree = ast.parse(content)
        
    analyzer = ComplexityAnalyzer()
    analyzer.visit(tree)
    
    lines = [l.strip() for l in content.splitlines() if l.strip() and not l.strip().startswith('#')]
    sloc = len(lines)
    
    # MI calculation
    mi = max(0, (171 - (5.2 * math.log(sloc if sloc > 0 else 1)) - (0.23 * analyzer.cc)) * 100 / 171)
    
    # Halstead Metrics
    n1, n2 = len(analyzer.u_operators), len(analyzer.u_operands)
    N2 = analyzer.total_operands
    
    volume = sloc * math.log2(n1 + n2) if (n1 + n2) > 0 else 0
    # Difficulty: (unique_ops / 2) * (total_operands / unique_operands)
    difficulty = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
    
    return {
        "sloc": sloc,
        "cc": analyzer.cc,
        "mi": round(mi, 2),
        "vol": round(volume, 2),
        "diff": round(difficulty, 2)
    }

def run_benchmarks():
    versions = [("Baseline ", baseline_app), ("Optimised ", optimised_app)]
    results = []

    for name, module in versions:
        # Resolve Controller Path
        controller_path = module.__file__.replace('main.py', 'controllers/submission_controller.py')
        if not os.path.exists(controller_path):
            controller_path = module.__file__.replace('main.py', 'submission_controller.py')
            
        static = calculate_metrics(controller_path)
        
        # Timing
        timer = timeit.Timer(lambda: module.main())
        raw_times = timer.repeat(repeat=3, number=5)
        avg_exec_time = (statistics.mean(raw_times) / 5) * 1000 
        
        # Interaction Count
        pr = cProfile.Profile()
        pr.enable()
        module.main()
        pr.disable()
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s)
        interactions = ps.total_calls

        # Coupling
        with open(controller_path, "r") as f:
            coupling = len([l for l in f.readlines() if "from optimised" in l or "from baseline" in l])

        results.append([
            name,
            f"{avg_exec_time:.3f}ms",
            interactions,
            static['sloc'],
            static['cc'],
            f"{static['mi']}%",
            static['vol'],
            static['diff'],
            f"{coupling} (CBO)"
        ])

    headers = ["Version", "Time", "Calls", "SLOC", "CC", "MI", "Hal. Vol", "Hal. Diff", "EOC (Coupling)"]
    print("\n" + "="*120)
    print("FINAL ARCHITECTURAL ANALYSIS REPORT")
    print("="*120)
    print(tabulate(results, headers=headers, tablefmt="fancy_grid"))

if __name__ == "__main__":
    run_benchmarks()