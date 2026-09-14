from pathlib import Path

import yaml


def test_validation_fetches_pinned_sources_before_running_tests():
    workflow = Path(__file__).parents[1] / ".github/workflows/validate.yml"
    steps = yaml.safe_load(workflow.read_text(encoding="utf-8"))["jobs"]["validate"]["steps"]
    test_steps = [index for index, step in enumerate(steps) if "pytest" in step.get("run", "")]
    assert test_steps
    for source in ("main", "release_62_0_0"):
        fetch_steps = [
            index for index, step in enumerate(steps)
            if f"swatref source fetch {source}" in step.get("run", "").splitlines()
        ]
        assert fetch_steps, f"missing fetch for {source}"
        assert max(fetch_steps) < min(test_steps), f"tests run before fetching {source}"
