import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import os

def plot_corr_matrix(data, title, output_path, tick_interval=100):
    if data.shape[1] == 0:
        print(f"[!] No functions left to plot for: {title}")
        return

    # 使用绝对值相关性
    corr = np.abs(np.corrcoef(data.T))
    np.fill_diagonal(corr, 0.0)

    fig, ax = plt.subplots(figsize=(14, 12))
    sns.heatmap(
        corr,
        cmap="coolwarm",
        center=0,
        square=True,
        cbar_kws={"label": "Abs Pearson Correlation Coefficient"},
        xticklabels=False,
        yticklabels=False
    )

    num_funcs = corr.shape[0]
    ticks = np.arange(0, num_funcs, tick_interval)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(ticks)
    ax.set_yticklabels(ticks)
    ax.tick_params(axis='x', rotation=90)
    ax.tick_params(axis='y', rotation=0)

    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[+] Saved: {output_path}")

def filter_symfuncs(data, threshold):
    corr = np.corrcoef(data.T)
    np.fill_diagonal(corr, 0.0)
    n = corr.shape[0]

    to_remove = set()
    removed_pairs = []

    for i in range(n):
        if i in to_remove:
            continue
        for j in range(i + 1, n):
            if j in to_remove:
                continue
            if abs(corr[i, j]) >= threshold:
                to_remove.add(j)
                removed_pairs.append((i, j, corr[i, j]))

    selected_indices = [i for i in range(n) if i not in to_remove]
    return np.array(selected_indices), removed_pairs

def batch_process(csv_path, thresholds=[0.99, 0.95, 0.90, 0.85, 0.80, 0.70, 0.60]):
    data = np.loadtxt(csv_path, delimiter=",")
    print(f"[✓] Loaded data from {csv_path}, shape: {data.shape}")

    # 过滤常数列
    variances = np.var(data, axis=0)
    constant_cols = np.where(variances == 0)[0]
    valid_mask = variances > 0
    data = data[:, valid_mask]
    print(f"[✓] Removed {len(constant_cols)} constant columns.")
    np.savetxt("valid_indices.txt", np.where(valid_mask)[0], fmt="%d")

    # 标准化
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    std[std == 0] = 1.0
    data = (data - mean) / std
    print("[✓] Data standardized (zero mean, unit variance).")

    all_retained_counts = []

    for threshold in thresholds:
        selected_indices, removed_pairs = filter_symfuncs(data, threshold)
        filtered_data = data[:, selected_indices]
        retained_count = len(selected_indices)
        all_retained_counts.append(retained_count)

        np.savetxt(f"filtered_symfunc_{int(threshold*100)}.csv", filtered_data, delimiter=",")
        np.savetxt(f"selected_indices_{int(threshold*100)}.txt", selected_indices, fmt="%d")
        with open(f"removed_pairs_{int(threshold*100)}.txt", "w") as f:
            for i, j, c in removed_pairs:
                f.write(f"{i},{j},{c:.4f}\n")

        print(f"[✓] Threshold {threshold}: {retained_count} functions retained, {len(removed_pairs)} pairs removed")

        if retained_count > 0:
            plot_corr_matrix(filtered_data, f"Filtered Symfuncs | Threshold < {threshold}", f"filtered_heatmap_{int(threshold*100)}.png")
        else:
            print(f"[!] Skipping heatmap for threshold {threshold} (no functions retained)")

    # 绘图：保留函数数量 vs 阈值
    if all_retained_counts:
        plt.figure(figsize=(7, 5))
        plt.plot(thresholds, all_retained_counts, marker='o')
        plt.xlabel("Correlation Threshold")
        plt.ylabel("Number of Retained Functions")
        plt.title("Retained Symfuncs vs Threshold")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("retained_vs_threshold.png", dpi=300)
        print("[+] Saved: retained_vs_threshold.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Symfunc correlation filtering and heatmap batch plotting")
    parser.add_argument("csv_file", help="Path to cleaned_symfunc.csv")
    args = parser.parse_args()

    if not os.path.exists(args.csv_file):
        print(f"ERROR: File {args.csv_file} does not exist.")
        exit(1)

    batch_process(args.csv_file)

