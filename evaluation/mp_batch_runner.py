"""Multiprocessing Agent Tester Script"""

import time
import pandas as pd
import numpy as np

from mp_agent_tester import benchmark_one_vs_five

if __name__ == "__main__":
    # np.random.seed(12345)
    runs_per_batch = 100
    n_batches = 4

    t0 = time.time()
    win_percentages = pd.Series(index=np.arange(1, n_batches +1))
    for k in win_percentages.index:
        win_percentages[k] = benchmark_one_vs_five(num_runs=runs_per_batch, num_workers=16, batch_seed=None)

    dt_total = time.time() - t0
    print("= " * 15)
    print("Summary of Win percentages of agent under test for each batch:")
    print(win_percentages)
    print()
    print(f"Mean: {win_percentages.mean():6.2f} %")
    print(f" Std: {win_percentages.std():6.2f} %")
    print()
    print(f"Total runtime: {dt_total:.3f} seconds")
