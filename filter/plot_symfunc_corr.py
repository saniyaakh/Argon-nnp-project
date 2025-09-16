import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import os
import matplotlib.ticker as ticker

def plot_correlation(csv_path, output_path="symfunc_corr_heatmap.png", tick_interval=100):
    # 读取 CSV 文件
    try:
        data = np.loadtxt(csv_path, delimiter=",")
    except Exception as e:
        print(f"Failed to read {csv_path}: {e}")
        return

    print(f"Loaded data with shape: {data.shape}")

    # 计算每个对称函数的标准差，过滤掉恒定项
    stds = np.std(data, axis=0)
    valid_indices = np.where(stds != 0)[0]
    num_removed = data.shape[1] - len(valid_indices)

    if num_removed > 0:
        print(f"Removed {num_removed} constant (zero-variance) symmetry functions.")
    else:
        print("All symmetry functions have non-zero variance.")

    filtered_data = data[:, valid_indices]

    # 计算相关性矩阵，并取绝对值
    corr = np.corrcoef(filtered_data.T)
    corr_abs = np.abs(corr)

    # 创建热力图（不显示自动 tick label）
    fig, ax = plt.subplots(figsize=(14, 12))
    sns.heatmap(
        corr_abs,
        cmap="coolwarm",
        center=0,
        square=True,
        cbar_kws={"label": "Abs Pearson Correlation Coefficient"},
        xticklabels=False,
        yticklabels=False
    )

    # 手动设置坐标轴刻度
    num_funcs = corr_abs.shape[0]
    ticks = np.arange(0, num_funcs, tick_interval)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(ticks)
    ax.set_yticklabels(ticks)
    ax.tick_params(axis='x', rotation=90)
    ax.tick_params(axis='y', rotation=0)

    plt.title("Symmetry Function Correlation Matrix (|Pearson|)")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.show()
    print(f"Saved heatmap to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot correlation matrix from symmetry function .csv file")
    parser.add_argument("csv_file", help="Path to cleaned_symfunc.csv")
    parser.add_argument("--output", default="symfunc_corr_heatmap.png", help="Output image filename")
    parser.add_argument("--tick", type=int, default=100, help="Tick interval for axis labels")

    args = parser.parse_args()

    if not os.path.exists(args.csv_file):
        print(f"ERROR: File {args.csv_file} does not exist.")
        exit(1)

    plot_correlation(args.csv_file, args.output, args.tick)

