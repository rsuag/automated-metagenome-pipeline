#!/usr/bin/env bash
set -euo pipefail

mode="${1:-}"

if [[ "$mode" != "mag" && "$mode" != "taxprofiler" ]]; then
  echo "Usage: bash bin/run_pipeline.sh {mag|taxprofiler}" >&2
  exit 2
fi

if ! command -v nextflow >/dev/null 2>&1; then
  echo "Nextflow is not available. Install Nextflow before running $mode." >&2
  exit 127
fi

profile="$(python3 scripts/read_project_value.py config/project.yaml container_profile)"
work_dir="$(python3 scripts/read_project_value.py config/project.yaml work_dir)"

mkdir -p results logs "$work_dir"

if [[ "$mode" == "taxprofiler" ]]; then
  version="$(python3 scripts/read_project_value.py config/project.yaml nfcore.taxprofiler_version)"
  nextflow run nf-core/taxprofiler \
    -r "$version" \
    -profile "$profile" \
    -params-file config/params_taxprofiler.yml \
    -work-dir "$work_dir/taxprofiler" \
    -resume \
    | tee logs/taxprofiler.nextflow.log
else
  version="$(python3 scripts/read_project_value.py config/project.yaml nfcore.mag_version)"
  nextflow run nf-core/mag \
    -r "$version" \
    -profile "$profile" \
    -params-file config/params_mag.yml \
    -work-dir "$work_dir/mag" \
    -resume \
    | tee logs/mag.nextflow.log
fi

