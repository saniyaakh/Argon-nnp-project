import numpy as np
import argparse
import os

def clean_function_data(input_file, output_prefix="cleaned_symfunc", expected_cols=None):
    clean_data = []

    with open(input_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            # 忽略空行
            if len(parts) == 0:
                continue
            # 如果未指定 expected 列数，取第一个正常值
            if expected_cols is None and len(parts) > 1:
                expected_cols = len(parts)
            # 跳过列数不匹配的行
            if len(parts) == expected_cols:
                try:
                    row = [float(x) for x in parts]
                    clean_data.append(row)
                except ValueError:
                    continue

    clean_array = np.array(clean_data)
    print(f"Loaded {clean_array.shape[0]} valid rows with {clean_array.shape[1]} features each.")

    # 保存为 .npy 和 .csv
    np.save(f"{output_prefix}.npy", clean_array)
    np.savetxt(f"{output_prefix}.csv", clean_array, delimiter=",")
    print(f"Saved to: {output_prefix}.npy and {output_prefix}.csv")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean n2p2 symmetry function data.")
    parser.add_argument("input_file", help="Path to function.data or similar file")
    parser.add_argument("--output_prefix", default="cleaned_symfunc", help="Output file prefix")
    parser.add_argument("--expected_cols", type=int, default=None, help="Expected number of columns (optional)")
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"ERROR: File {args.input_file} does not exist.")
        exit(1)

    clean_function_data(args.input_file, args.output_prefix, args.expected_cols)

