import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from swatplus_reference.parser.fortran import parse_tree  # noqa: E402
from swatplus_reference.source.config import Config  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def store():
    return parse_tree(FIXTURES, source_ref="test")


@pytest.fixture
def cfg(tmp_path):
    return Config(
        root=tmp_path,
        source_dir=FIXTURES,
        source_link_base="https://example.test/src",
        version_label="TEST 1.0",
    )
