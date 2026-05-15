# Instances used for the two-stage energy-oriented lot-sizing problem

This repository contains two-stage data instances ready for mathematical programming and optimization benchmarking in solvers like CPLEX or Gurobi. 


## Dataset Structure & Mirroring

The instances are structured into directories representing different problem dimensions (Days $d$, Items $p$, and the number of scenarios $scen$).

```text
.
├── README.md
└── result_output/
    ├── d3p3_100scen/        # 3 days, 3 items, 100 Scenarios
    │   ├── entree_1.csv     # Individual problem instances
    │   ├── entree_2.csv
    │   └── ...
    └── d4p5_500scen/         # 4 days, 5 items, 500 Scenarios
        ├── entree_1.csv
        └── entree_2.csv
