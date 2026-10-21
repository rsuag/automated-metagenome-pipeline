# Metagenome Methods Blueprint

## General Backbone

1. Run read quality control, trim adapters, and filter host or contaminant reads.
2. Profile taxonomy with Kraken2/Bracken and MetaPhlAn/mOTUs; add Kaiju when protein-level classification is useful.
3. Define co-assembly `group` by habitat, latitude, treatment, or sequencing batch. Avoid forcing ecologically dissimilar samples into one assembly.
4. Use multiple binning algorithms and refinement, such as MetaBAT2, MaxBin2, and CONCOCT.
5. Assess MAG completeness, contamination, N50, contig count, GC content, and strain heterogeneity.
6. Dereplicate with dRep/ANI and assign consistent taxonomy with GTDB-Tk.
7. Map each sample's reads back to contigs or MAGs; report coverage, TPM/RPKM, and presence/absence.
8. Annotate functions with Prokka, eggNOG, DRAM, or KEGG; add NCycDB or curated HMMs for nitrogen cycling.
9. Run ecological analyses as appropriate: alpha/beta diversity, RDA/dbRDA, Mantel/MRM, VPA, distance-decay, NST/betaNTI/RCbray, and niche breadth.
10. Audit figures against their evidence layers. Do not combine associations, functional potential, and process rates into an unsupported causal chain.

## Optional Top-Journal Modules

- Strain-resolved profiling: strain tracking, SNPs, pangenomes and within-species population structure.
- Viral and plasmid layer: viral contigs, host prediction, AMG annotation, plasmid/MGE detection.
- ARG and pathogen layer: AMR gene profiles, virulence factors, mobile element linkage and risk caveats.
- Eukaryotic or fungal layer: marker-specific profiling when the ecosystem needs it.
- Long-read or hybrid assembly: long-read correction, hybrid assembly and circular element recovery.
- Genome-resolved metabolism: pathway completeness, guild annotation and substrate-use potential.
- Spatial or temporal layer: mixed models, time-series, distance-decay and turnover partitioning.
- Multi-omics link: metatranscriptome, metaproteome or metabolome integration when available.

## Domain Packs

Domain packs should add markers, databases and interpretation rules without changing the general backbone.

### Mangrove/AOA/Nitrifier Pack

- `amoA` read mapping: summarize AOA/AOB/comammox markers separately from whole-genome MAG abundance.
- NS/NP/TH1177/TH5896 lineage abundance: connect geographic gradients to AOA niche differences.
- N/C/S/P marker-gene heatmaps: display amoABC, ureABC, cynS, nirK, norBC, nosZ, coxAB, sqr, pst/phn, cob, sod/kef, and related markers by module.
- MAG completeness-aware heatmaps: state clearly that non-detection in medium-quality MAGs is not proof of absence.
- Environmental collinearity checks: assess correlations or variance inflation among latitude, temperature, salinity, TC/TN/TS, NH4+, and ion measurements before interpreting RDA/MRM.

### Human/Host-Associated Pack

- Host read removal with explicit genome build and privacy-aware reporting.
- Strain-level tracking for dominant gut taxa when depth supports it.
- Functional modules for carbohydrate-active enzymes, bile acid metabolism and ARGs.
- Case-control statistics with covariates, batch effects and medication/diet metadata.

### Soil/Sediment/Biogeochemistry Pack

- Marker sets for nitrogen, sulfur, methane, carbon fixation and phosphorus acquisition.
- Redox, moisture, pH, organic matter and geochemical covariate checks.
- Guild-level aggregation and process-rate integration when measured.

## Claims Not to Make Automatically

- Do not claim activity or a validated mechanism without metatranscriptomic, proteomic, process-rate, or other direct supporting evidence.
- Do not co-assemble every sample by default; justify the grouping.
- Do not base a conclusion on one taxonomic classifier alone.
- Do not infer loss of ecological adaptation from missing MAG genes unless MAG quality and marker searches support that inference.
