SHELL := /bin/bash

.PHONY: validate radar run-taxonomy run-mag summarize all

validate:
	python3 scripts/validate_inputs.py --project config/project.yaml

radar:
	python3 scripts/method_radar.py --sources config/method_sources.json --project config/project.yaml

run-taxonomy: validate
	bash bin/run_pipeline.sh taxprofiler

run-mag: validate
	bash bin/run_pipeline.sh mag

summarize:
	python3 scripts/summarize_mag_outputs.py --project config/project.yaml

all: validate radar run-taxonomy run-mag summarize
