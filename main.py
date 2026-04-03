"""Main entry point for warehouse robot delivery system."""

import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.utils import set_seed, load_config
from src.state import RobotState
from src.search import UniformCostSearch
from src.problem import WarehouseProblem

def main():
    parser = argparse.ArgumentParser(description="Warehouse Robot Delivery")
    parser.add_argument("--grid", default="simple_5x5", 
                        help="Grid name (simple_5x5, medium_8x8, hard_10x10)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--no-mlflow", action="store_true", help="Disable MLflow")
    
    args = parser.parse_args()
    
    # Load config
    config = load_config()
    
    # Set seed
    set_seed(args.seed)
    
    # Import grid (simplified for demo)
    from experiments.run_experiment import get_grid_from_csv, parse_grid
    
    grid = get_grid_from_csv(args.grid)
    if not grid:
        print(f"Grid {args.grid} not found")
        return
    
    # Find positions
    package_positions = []
    delivery_pos = None
    start_pos = None
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'P':
                package_positions.append((i, j))
            elif grid[i][j] == 'D':
                delivery_pos = (i, j)
            elif grid[i][j] == 'S':
                start_pos = (i, j)
    
    # Create problem and solve
    problem = WarehouseProblem(grid, package_positions, delivery_pos)
    initial_state = RobotState(start_pos, frozenset())
    
    ucs = UniformCostSearch(problem)
    path, cost, nodes, time_taken = ucs.solve(initial_state)
    
    if path:
        print(f"\n✓ Solution found!")
        print(f"  Cost: {cost}")
        print(f"  Path: {path}")
        print(f"  Nodes expanded: {nodes}")
        print(f"  Time: {time_taken:.3f}s")
    else:
        print("\n✗ No solution found")

if __name__ == "__main__":
    main()
