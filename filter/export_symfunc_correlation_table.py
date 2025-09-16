import numpy as np
import pandas as pd
import argparse
import os

def compute_sorted_correlations(csv_path, output_csv="correlation_table.csv", threshold=0.0):
    # 加载数据
    data = np.loadtxt(csv_path, delimiter=",")
    n_funcs = data.shape[1]

    # 计算相关性矩阵
    corr = np.corrcoef(data.T)

    # 提取非对角线元素并排序
    records = []
    for i in range(n_funcs):
        for j in range(i+1, n_funcs):
            r = corr[i, j]
            if abs(r) >= threshold:
                records.append((i, j, r))

    records_sorted = sorted(records, key=lambda x: -abs(x[2]))

    # 写入 CSV 表格
    df = pd.DataFrame(records_sorted, columns=["Function A", "Function B", "Pearson Correlation"])
    df.to_csv(output_csv, index=False)
    print(f"✅ Exported correlation table with {len(df)} entries to {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute and export sorted symmetry function correlation table.")
    parser.add_argument("csv_path", help="Path to cleaned_symfunc.csv")
    parser.add_argument("--output", default="correlation_table.csv", help="Output CSV file name")
    parser.add_argument("--threshold", type=float, default=0.0, help="Minimum absolute correlation to include")

    args = parser.parse_args()

    if not os.path.exists(args.csv_path):
        print(f"❌ File {args.csv_path} not found.")
        exit(1)

    compute_sorted_correlations(args.csv_path, args.output, args.threshold)

