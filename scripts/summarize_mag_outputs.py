#!/usr/bin/env python3
import argparse
import os
from datetime import date

from read_project_value import load_simple_yaml


CHECKS = [
    ("Raw read QC", ["multiqc", "fastqc"]),
    ("Taxonomic profiling", ["kraken2", "bracken", "metaphlan", "taxprofiler"]),
    ("Assembly", ["megahit", "spades", "assembly"]),
    ("Binning", ["metabat", "maxbin", "concoct", "binning"]),
    ("MAG QC", ["checkm", "quast", "busco"]),
    ("MAG taxonomy", ["gtdb", "cat"]),
    ("MAG annotation", ["prokka", "eggnog", "dram", "annotation"]),
    ("Abundance mapping", ["coverm", "quant", "coverage", "abundance"]),
]


def find_hits(root, needles):
    hits = []
    if not os.path.exists(root):
        return hits
    for current, dirs, files in os.walk(root):
        hay = current.lower()
        if any(needle in hay for needle in needles):
            hits.append(current)
        for name in files:
            lowered = name.lower()
            if any(needle in lowered for needle in needles):
                hits.append(os.path.join(current, name))
        if len(hits) >= 5:
            break
    return hits


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    args = parser.parse_args()

    project = load_simple_yaml(args.project)
    outputs = project["outputs"]
    report_dir = outputs["report_dir"]
    os.makedirs(report_dir, exist_ok=True)

    roots = [outputs["taxonomy_dir"], outputs["mag_dir"]]
    lines = [
        "# Metagenome Methods Audit",
        "",
        f"- Date: {date.today().isoformat()}",
        f"- Project: {project['project_name']}",
        f"- nf-core/mag: {project['nfcore']['mag_version']}",
        f"- nf-core/taxprofiler: {project['nfcore']['taxprofiler_version']}",
        "",
        "## Module Status",
        "",
        "| Module | Status | Evidence |",
        "| --- | --- | --- |",
    ]

    missing = []
    for label, needles in CHECKS:
        hits = []
        for root in roots:
            hits.extend(find_hits(root, needles))
        if hits:
            evidence = "<br>".join(hits[:3])
            status = "present"
        else:
            evidence = "not found"
            status = "missing"
            missing.append(label)
        lines.append(f"| {label} | {status} | {evidence} |")

    lines.extend(
        [
            "",
            "## Interpretation Guardrails",
            "",
            "- MAG gene presence supports metabolic potential, not measured activity.",
            "- Gene absence in medium-quality MAGs should be reported as not detected, not pathway loss.",
            "- Read-based abundance, amplicon ASVs, and MAG gene content should remain separate evidence layers.",
            "- Environmental correlations need effect size and multiple-testing control before biological interpretation.",
            "",
            "## Next Actions",
            "",
        ]
    )

    if missing:
        lines.extend([f"- Add or verify output for: {item}" for item in missing])
    else:
        lines.append("- All expected module outputs were detected.")

    report_path = os.path.join(report_dir, "methods_audit.md")
    with open(report_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    print(report_path)


if __name__ == "__main__":
    main()

