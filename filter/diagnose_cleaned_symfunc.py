import numpy as np
import argparse

def diagnose_symfunc_csv(path):
    try:
        data = np.loadtxt(path, delimiter=",")
    except Exception as e:
        print(f"[✗] Failed to load CSV: {e}")
        return

    print(f"[✓] Loaded data from {path}")
    print(f"    Shape: {data.shape} (rows = samples, cols = symfuncs)")

    # 检查是否存在 NaN
    if np.isnan(data).any():
        print("[!] Detected NaN values in the data.")
    else:
        print("[✓] No NaN values.")

    # 检查是否存在全 0 的列
    col_sums = np.sum(np.abs(data), axis=0)
    zero_cols = np.where(col_sums == 0)[0]
    if len(zero_cols) > 0:
        print(f"[!] Found {len(zero_cols)} all-zero columns.")
    else:
        print("[✓] No all-zero columns.")

    # 检查是否存在常数列
    stds = np.std(data, axis=0)
    constant_cols = np.where(stds == 0)[0]
    if len(constant_cols) > 0:
        print(f"[!] Found {len(constant_cols)} constant columns (zero variance).")
    else:
        print("[✓] No constant columns.")

    # 检查值范围
    dmin = np.min(data)
    dmax = np.max(data)
    print(f"[✓] Value range: min = {dmin:.4f}, max = {dmax:.4f}")

    if dmax - dmin < 1e-4:
        print("[!] Value range extremely narrow — may indicate bad normalization.")

    # 查看部分数值样本
    print("[i] Sample values from first 3 functions (columns):")
    for i in range(min(3, data.shape[1])):
        print(f"    Func {i}: {data[:10, i]}")

    # 最后提示
    if len(constant_cols) > 0 or len(zero_cols) > 0:
        print("\n[!] Suggest removing constant or zero columns before correlation analysis.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Diagnose cleaned_symfunc.csv for common issues.")
    parser.add_argument("csv_file", help="Path to cleaned_symfunc.csv")
    args = parser.parse_args()
    diagnose_symfunc_csv(args.csv_file)

