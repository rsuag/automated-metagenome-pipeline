#!/usr/bin/env python3
import argparse
import csv
import os
import sys

try:
    import yaml
except ImportError:
    yaml = None

from read_project_value import load_simple_yaml


REQUIRED_MAG_COLUMNS = [
    "sample",
    "group",
    "short_reads_1",
    "short_reads_2",
    "long_reads",
    "short_reads_platform",
    "long_reads_platform",
]

REQUIRED_TAX_COLUMNS = [
    "sample",
    "run_accession",
    "instrument_platform",
    "fastq_1",
    "fastq_2",
    "fasta",
]

REQUIRED_DB_COLUMNS = ["tool", "db_name", "db_params", "db_type", "db_path"]


def read_csv(path):
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def require_columns(rows, required, label):
    if not rows:
        raise ValueError(f"{label} is empty")
    missing = [col for col in required if col not in rows[0]]
    if missing:
        raise ValueError(f"{label} missing columns: {', '.join(missing)}")


def check_fastq_paths(rows, columns, label):
    missing = []
    bad_ext = []
    for row in rows:
        for col in columns:
            value = (row.get(col) or "").strip()
            if not value:
                continue
            if not value.endswith((".fastq.gz", ".fq.gz", ".fa.gz", ".fasta.gz")):
                bad_ext.append(f"{label}:{row.get('sample')}:{col}={value}")
            if value.startswith("/path/to/"):
                missing.append(value)
            elif not os.path.exists(value):
                missing.append(value)
    return missing, bad_ext


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    args = parser.parse_args()

    project = load_simple_yaml(args.project)
    inputs = project["inputs"]

    errors = []
    warnings = []

    for path_key, required, label in [
        ("mag_samplesheet", REQUIRED_MAG_COLUMNS, "MAG samplesheet"),
        ("taxprofiler_samplesheet", REQUIRED_TAX_COLUMNS, "taxprofiler samplesheet"),
        ("taxprofiler_databases", REQUIRED_DB_COLUMNS, "taxprofiler database sheet"),
    ]:
        path = inputs[path_key]
        if not os.path.exists(path):
            example = path.replace(".csv", ".example.csv")
            errors.append(f"{path} does not exist; start from {example}")
            continue
        try:
            rows = read_csv(path)
            require_columns(rows, required, label)
        except Exception as exc:
            errors.append(str(exc))
            continue

        if path_key.endswith("samplesheet"):
            missing, bad_ext = check_fastq_paths(
                rows,
                ["short_reads_1", "short_reads_2", "long_reads", "fastq_1", "fastq_2", "fasta"],
                label,
            )
            warnings.extend([f"Input path not found yet: {item}" for item in missing])
            errors.extend([f"Unexpected sequence file extension: {item}" for item in bad_ext])
        else:
            for row in rows:
                db_path = (row.get("db_path") or "").strip()
                if db_path.startswith("/path/to/") or not os.path.exists(db_path):
                    warnings.append(f"Database path not found yet: {db_path}")

    for warning in warnings:
        print(f"WARN: {warning}", file=sys.stderr)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        sys.exit(1)
    print("Input structure is valid. Missing data/database paths are warnings until real paths are filled.")


if __name__ == "__main__":
    main()

