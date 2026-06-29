# Reliability Model

This project treats automation as a controlled system, not as a pile of shell commands.

## Reliability Gates

| Gate | Question | Failure behavior |
| --- | --- | --- |
| Input gate | Are samplesheets, paths and metadata shaped correctly? | stop before compute |
| Database gate | Are database paths explicit and versioned? | warn or stop depending on module |
| Module gate | Did each expected output layer appear? | report missing layer |
| Evidence gate | Does the interpretation match the evidence type? | downgrade claim |
| Method gate | Is a new method maintained, benchmarked and auditable? | keep in watch list |

## Evidence Types

| Evidence | Supports | Does not support alone |
| --- | --- | --- |
| Taxonomic profile | community composition | strain activity or mechanism |
| MAG abundance | distribution of recovered genomes | absolute organismal abundance without caveats |
| MAG gene content | metabolic potential | gene expression or process rate |
| Environmental correlation | association | causality |
| Null model | assembly pattern hypothesis | direct ecological mechanism |

## Adoption Stages

- `watch`: interesting source or release, no workflow change.
- `benchmark`: candidate has a clear module fit and can be tested.
- `optional`: available as an opt-in module.
- `default`: promoted only after benchmark, documentation and audit support.

