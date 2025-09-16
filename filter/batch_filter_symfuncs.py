import os
import re
import numpy as np

def load_selected_indices(path):
    return np.loadtxt(path, dtype=int)

def extract_index_threshold(filename):
    match = re.search(r"selected_indices_(\d+)\.txt", filename)
    if match:
        return float(match.group(1)) / 100
    return None

def filter_with_indices(original_file, indices_file, output_prefix):
    selected_indices = load_selected_indices(indices_file)

    with open(original_file, "r") as f:
        lines = f.readlines()

    # Separate comment lines and symfunction lines
    header_lines = [line for line in lines if line.strip().startswith("#")]
    symfunc_lines = [line for line in lines if not line.strip().startswith("#") and line.strip().startswith("symfunction")]

    if max(selected_indices) >= len(symfunc_lines):
        raise ValueError(f"[×] Index out of range in {indices_file} (max index {max(selected_indices)} >= {len(symfunc_lines)})")

    retained_lines = [symfunc_lines[i] for i in selected_indices]

    # Save the filtered file (with header)
    with open(f"{output_prefix}.txt", "w") as f:
        f.writelines(header_lines)
        f.writelines(retained_lines)

    # Save retained lines as a separate record
    with open(f"retained_symfunc_lines_{output_prefix.split('_')[-1]}.txt", "w") as f:
        for idx in selected_indices:
            f.write(f"# index {idx}:\n{symfunc_lines[idx]}")

    print(f"[✓] Processed: {indices_file} → {output_prefix}.txt + retained_symfunc_lines_*.txt ({len(retained_lines)} functions retained)")

def batch_filter(original_file, indices_dir="."):
    for fname in sorted(os.listdir(indices_dir)):
        if fname.startswith("selected_indices_") and fname.endswith(".txt"):
            threshold = extract_index_threshold(fname)
            if threshold is None:
                continue

            input_path = os.path.join(indices_dir, fname)
            output_prefix = os.path.join(indices_dir, f"filtered_generated_symfuncs_{int(threshold * 100)}")

            try:
                filter_with_indices(original_file, input_path, output_prefix)
            except Exception as e:
                print(f"[!] Error processing {fname}: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Batch filter symmetry functions using selected index files")
    parser.add_argument("original_file", help="Path to original generated_symfuncs.txt file")
    parser.add_argument("--dir", default=".", help="Directory containing selected_indices_XX.txt files (default: current directory)")
    args = parser.parse_args()

    batch_filter(args.original_file, args.dir)

