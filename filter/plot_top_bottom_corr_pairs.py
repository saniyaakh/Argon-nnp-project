import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_extreme_corr_pairs(data_path, corr_table_path, output_dir="extreme_corr_plots", top_n=10):
    # 加载数据和相关性表
    data = np.loadtxt(data_path, delimiter=",")
    df_corr = pd.read_csv(corr_table_path)

    # 排序
    df_corr_sorted = df_corr.reindex(df_corr["Pearson Correlation"].abs().sort_values(ascending=False).index)

    # 提取前/后 N 对
    top_pairs = df_corr_sorted.head(top_n)
    bottom_pairs = df_corr_sorted.tail(top_n)

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 画图函数
    def plot_pair(i, j, r, label, rank):
        plt.figure(figsize=(6, 6))
        plt.scatter(data[:, i], data[:, j], alpha=0.5, s=10)
        plt.xlabel(f"Function {i}")
        plt.ylabel(f"Function {j}")
        plt.title(f"{label} {rank}: f{i} vs f{j}\nPearson r = {r:.4f}")
        fname = f"{label.lower()}_{rank:02d}_f{i}_vs_f{j}.png"
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, fname), dpi=300)
        plt.close()

    # 绘制 Top N
    for rank, row in enumerate(top_pairs.itertuples(), 1):
        plot_pair(row._1, row._2, row._3, "Top", rank)

    # 绘制 Bottom N
    for rank, row in enumerate(bottom_pairs.itertuples(), 1):
        plot_pair(row._1, row._2, row._3, "Bottom", rank)

    print(f"✅ Saved plots to {output_dir}/")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Plot top and bottom correlated symmetry function pairs.")
    parser.add_argument("data_csv", help="CSV file of symmetry function values (e.g. cleaned_symfunc.csv)")
    parser.add_argument("corr_table_csv", help="CSV file of correlation table (e.g. correlation_table.csv)")
    parser.add_argument("--output_dir", default="extreme_corr_plots", help="Folder to save plots")
    parser.add_argument("--top_n", type=int, default=10, help="Number of top/bottom pairs to plot")
    args = parser.parse_args()

    plot_extreme_corr_pairs(args.data_csv, args.corr_table_csv, args.output_dir, args.top_n)

