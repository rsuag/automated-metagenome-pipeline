#!/usr/bin/env python3
import argparse
import json
import os
import textwrap
import urllib.error
import urllib.request
from datetime import date

from read_project_value import load_simple_yaml


def fetch_json(url, timeout=15):
    request = urllib.request.Request(url, headers={"User-Agent": "automated-metagenome-pipeline"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def summarize_github_releases(source):
    try:
        releases = fetch_json(source["url"])
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {"status": "unavailable", "items": [], "note": str(exc)}

    items = []
    for release in releases[:5]:
        items.append(
            {
                "title": release.get("name") or release.get("tag_name") or "unnamed release",
                "version": release.get("tag_name") or "",
                "published_at": release.get("published_at") or "",
                "url": release.get("html_url") or source["url"],
            }
        )
    return {"status": "ok", "items": items, "note": ""}


def summarize_static_source(source):
    return {
        "status": "watch",
        "items": [
            {
                "title": source["name"],
                "version": "",
                "published_at": "",
                "url": source["url"],
            }
        ],
        "note": "Static watch source. Review manually or replace with a machine-readable feed.",
    }


def adoption_checklist(stage):
    checklist = [
        "maintenance status checked",
        "container or conda availability checked",
        "benchmark dataset identified",
        "outputs are parseable by audit scripts",
        "interpretation limits documented",
    ]
    if stage in {"optional", "default"}:
        checklist.append("backward compatibility plan written")
    if stage == "default":
        checklist.append("default promotion approved after benchmark")
    return checklist


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", required=True)
    parser.add_argument("--project", required=True)
    args = parser.parse_args()

    with open(args.sources, "r", encoding="utf-8") as handle:
        config = json.load(handle)
    project = load_simple_yaml(args.project)
    report_path = project["automation"]["method_radar_report"]
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    lines = [
        "# Method Radar",
        "",
        f"- Date: {date.today().isoformat()}",
        f"- Project: {project['project_name']}",
        "",
        "This report tracks candidate methods and tool updates. It does not promote tools automatically; it creates a review queue.",
        "",
        "## Sources",
        "",
    ]

    for source in config["sources"]:
        if source["type"] == "github_releases":
            summary = summarize_github_releases(source)
        else:
            summary = summarize_static_source(source)

        lines.extend(
            [
                f"### {source['name']}",
                "",
                f"- Module: `{source['module']}`",
                f"- Adoption stage: `{source['adoption_stage']}`",
                f"- Status: `{summary['status']}`",
            ]
        )
        if summary["note"]:
            wrapped_note = textwrap.fill(summary["note"], width=100)
            lines.append(f"- Note: {wrapped_note}")
        lines.extend(["", "| Item | Version | Published | Link |", "| --- | --- | --- | --- |"])
        if summary["items"]:
            for item in summary["items"]:
                lines.append(
                    f"| {item['title']} | {item['version']} | {item['published_at']} | {item['url']} |"
                )
        else:
            lines.append("| No items collected |  |  |  |")
        lines.extend(["", "Adoption checklist:", ""])
        lines.extend([f"- {item}" for item in adoption_checklist(source["adoption_stage"])])
        lines.append("")

    lines.extend(
        [
            "## Promotion Rule",
            "",
            "A candidate can move from `watch` to `benchmark` only when it has a clear module fit and documented outputs. It can move to `optional` after a benchmark on a small public or internal dataset. It can become `default` only when it improves accuracy, speed, interpretability or scope without breaking existing projects.",
            "",
        ]
    )

    with open(report_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    print(report_path)


if __name__ == "__main__":
    main()
