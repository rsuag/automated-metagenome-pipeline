# Automated Metagenome Pipeline

A reusable metagenomics analysis scaffold that brings established workflows, commonly used analyses, method tracking, quality audits, and interpretable reports together. It builds on `nf-core/mag` and `nf-core/taxprofiler` with checks and decisions from raw data through publication-ready results.

## Why This Exists

Even with a working metagenomics workflow, users still need to decide:

- Whether samplesheets, databases, host filtering, and co-assembly groups are appropriate.
- Which taxonomy, binning, MAG QC, functional annotation, and abundance tools to use.
- Whether a new method or tool merits adoption.
- Which results support a mechanistic interpretation and which show only potential or association.
- Whether the final report is transparent enough to reproduce.

This project turns those decisions into inspectable workflow modules, with a traceable analysis path for both new and experienced users.

## Main Workflow

```mermaid
flowchart TD
    A["Samplesheet + metadata"] --> B["Input validator"]
    B --> C["Read QC and host filtering"]
    C --> D["Taxonomic profiling<br/>Kraken2, Bracken, MetaPhlAn, mOTUs, Kaiju"]
    C --> E["Assembly<br/>single-sample or group co-assembly"]
    E --> F["Binning and refinement<br/>MetaBAT2, MaxBin2, CONCOCT"]
    F --> G["MAG quality control<br/>CheckM/CheckM2, QUAST, BUSCO"]
    G --> H["Dereplication and taxonomy<br/>dRep, ANI, GTDB-Tk"]
    H --> I["Read-to-MAG abundance<br/>CoverM or mapper-based coverage"]
    H --> J["Functional annotation<br/>eggNOG, DRAM, KEGG, custom HMMs"]
    D --> K["Ecological statistics<br/>diversity, ordination, VPA, NST, betaNTI"]
    I --> K
    J --> K
    K --> L["Evidence-aware report<br/>figures, tables, methods audit"]
    M["Method radar<br/>papers, releases, nf-core, tool registries"] --> N["Adoption checklist"]
    N --> O["Curated module registry"]
    O --> B
```

## What Makes It More Automatic

- One command validates samplesheets, database paths, output structure and expected modules.
- Project parameters live in `config/project.yaml`; pipeline-specific parameters live in focused files.
- `method_radar` scans curated sources and writes an update report instead of relying on memory.
- `methods_audit` checks whether expected result layers exist before interpretation.
- Evidence guardrails are built into the report: abundance, taxonomy, MAG gene content and environmental correlations are kept as separate evidence layers.
- The design is domain-neutral: human gut, soil, sediment, marine, plant-associated, engineered systems and host-associated metagenomes can use the same backbone.

## Quick Start

```bash
git clone https://github.com/rsuag/automated-metagenome-pipeline.git
cd automated-metagenome-pipeline

make validate
make radar
make run-taxonomy
make run-mag
make summarize
```

For a full run:

```bash
make all
```

Before real analysis, edit:

- `config/project.yaml`
- `config/samplesheet_mag.csv`
- `config/samplesheet_taxprofiler.csv`
- `config/databases_taxprofiler.csv`
- `config/params_mag.yml`
- `config/params_taxprofiler.yml`

## Modules

| Layer | Default strategy | Reliability check |
| --- | --- | --- |
| Read QC | FastQC/MultiQC plus short-read QC | fail early on missing reads or wrong file shape |
| Decontamination | host/PhiX/custom reference filtering | require explicit reference paths |
| Taxonomy | multi-tool profiling | compare marker-based and k-mer-based profiles |
| Assembly | single-sample or group co-assembly | group must be declared in samplesheet |
| Binning | multiple binners plus refinement | report bin origin and refinement status |
| MAG QC | completeness, contamination, N50, contig count | separate high-quality and medium-quality MAGs |
| Taxonomy | GTDB-Tk/CAT-style classification | preserve database version in report |
| Dereplication | dRep/ANI | keep representative genome and cluster map |
| Abundance | reads-to-contigs/MAG mapping | report coverage, breadth and normalized abundance |
| Function | general and custom databases | distinguish gene presence, pathway completeness and measured activity |
| Ecology | ordination, variance partitioning, null models | require metadata and multiple-testing notes |
| Reporting | audit-first summary | flag missing layers before biological interpretation |

## Method Radar

The radar is a lightweight way to keep the project current without blindly chasing every new tool.

```bash
make radar
```

It reads `config/method_sources.json`, checks curated sources when network is available, and writes:

```text
results/report/method_radar.md
```

New methods are not automatically promoted to defaults. They pass through this checklist:

1. Does it solve a real bottleneck compared with the current module?
2. Is it maintained, documented and reproducible in containers or conda?
3. Does it expose outputs that can be audited automatically?
4. Can it coexist with current defaults without breaking old projects?
5. Does it improve accuracy, speed, interpretability or scope enough to justify adoption?

## Top-Journal Analysis Extensions

The default backbone can be extended with modules often seen in strong microbiome and metagenome papers:

- Strain-resolved profiling and population genetics.
- Viral, plasmid, ARG and mobile genetic element analysis.
- Genome-resolved metabolic reconstruction.
- Long-read or hybrid assembly.
- MAG abundance, prevalence and niche breadth.
- Environmental association, variance partitioning and distance-decay.
- Null-model community assembly analysis.
- Custom marker HMMs for nitrogen, carbon, sulfur, phosphorus, methane, antibiotic resistance or host-specific pathways.

## Interpretation Rules

- MAG gene presence supports metabolic potential, not direct activity.
- Gene absence in incomplete MAGs should be reported as not detected, not true pathway loss.
- Taxonomic profiles, read mapping, MAG content and environmental correlations should not be collapsed into one causal claim.
- Process claims need process measurements, transcriptomics, proteomics, stable isotope data or controlled validation.

## Repository Layout

```text
.
├── bin/                         # pipeline launchers
├── config/                      # project, samplesheet, database and radar configs
├── docs/                        # method blueprint and reliability model
├── scripts/                     # validators, radar and reporting utilities
├── Makefile                     # common entry points
└── README.md                    # GitHub landing page
```

## Current Status

This is an automation scaffold plus reliability layer. It is ready for real project paths and database paths, but the first public release intentionally keeps compute-heavy outputs out of the repository.

