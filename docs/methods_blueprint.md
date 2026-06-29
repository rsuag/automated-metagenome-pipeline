# Metagenome Methods Blueprint

## General Backbone

1. 原始 reads 质控、接头去除、宿主/污染过滤。
2. 多工具分类谱：Kraken2/Bracken + MetaPhlAn/mOTUs，必要时加入 Kaiju 做蛋白层面补充。
3. 分组共组装：按生境、纬度、处理组或测序批次定义 `group`，避免把生态差异过大的样本强行共组装。
4. 多算法 binning + refinement：MetaBAT2、MaxBin2、CONCOCT 取交集/优化结果。
5. MAG 质控：completeness、contamination、N50、contig 数、GC、strain heterogeneity。
6. 去冗余与分类：dRep/ANI 聚类，GTDB-Tk 给统一 taxonomy。
7. 丰度回贴：每个样本 reads mapping 到 contigs/MAGs，生成 coverage、TPM/RPKM、presence/absence。
8. 功能注释：Prokka/eggNOG/DRAM/KEGG；氮循环额外用 NCycDB 或 curated HMM。
9. 生态统计：alpha/beta diversity、RDA/dbRDA、Mantel/MRM、VPA、distance-decay、NST/betaNTI/RCbray、niche breadth。
10. 论文级审计：每张图对应一个证据层，不把相关性、功能潜力和过程速率混为因果链。

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

- `amoA` read mapping：把 AOA/AOB/comammox marker 与全基因组 MAG abundance 分开汇总。
- NS/NP/TH1177/TH5896 lineage 层面丰度：用于连接地理梯度和 AOA 生态位差异。
- N/C/S/P marker gene heatmap：把 amoABC、ureABC、cynS、nirK、norBC、nosZ、coxAB、sqr、pst/phn、cob、sod/kef 等按模块展示。
- MAG completeness-aware heatmap：图例明确 medium-quality MAG 的缺失不能当作真实缺失。
- 环境变量共线性检查：纬度、温度、盐度、TC/TN/TS、NH4+、离子指标先做相关性/方差膨胀因子，再解释 RDA/MRM。

### Human/Host-Associated Pack

- Host read removal with explicit genome build and privacy-aware reporting.
- Strain-level tracking for dominant gut taxa when depth supports it.
- Functional modules for carbohydrate-active enzymes, bile acid metabolism and ARGs.
- Case-control statistics with covariates, batch effects and medication/diet metadata.

### Soil/Sediment/Biogeochemistry Pack

- Marker sets for nitrogen, sulfur, methane, carbon fixation and phosphorus acquisition.
- Redox, moisture, pH, organic matter and geochemical covariate checks.
- Guild-level aggregation and process-rate integration when measured.

## 不建议自动加入的内容

- 不在没有宏转录组/蛋白组/过程速率时声称“活性”或“机制已验证”。
- 不把所有样本强制 co-assembly；分组要能解释。
- 不只用单一分类工具下结论。
- 不用 MAG gene absence 支撑生态适应缺失，除非 MAG 高质量且 marker 检索充分。
