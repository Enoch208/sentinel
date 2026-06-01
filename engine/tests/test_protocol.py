from __future__ import annotations

import pytest
from pydantic import ValidationError

from sentinel_engine.protocol import (
    COMMAND_ADAPTER,
    SensitivityCommand,
    TeachCommand,
    VerdictEvent,
)
from sentinel_engine.types import Neighbor, Verdict


def test_parses_sensitivity_command() -> None:
    command = COMMAND_ADAPTER.validate_python({"type": "sensitivity", "value": 0.7})
    assert isinstance(command, SensitivityCommand)
    assert command.value == 0.7


def test_parses_teach_command() -> None:
    command = COMMAND_ADAPTER.validate_python(
        {"type": "teach", "frame_id": 3, "label": "expected"}
    )
    assert isinstance(command, TeachCommand)
    assert command.frame_id == 3


def test_verdict_event_maps_from_domain() -> None:
    verdict = Verdict(
        frame_id=1,
        ts=1.0,
        score=0.9,
        threshold=0.8,
        flagged=True,
        warming=False,
        neighbors=[Neighbor(id=2, score=0.9)],
    )
    event = VerdictEvent.of(verdict)
    assert event.type == "verdict"
    assert event.flagged is True
    assert event.neighbors[0].id == 2


def test_parses_zone_and_facet_commands() -> None:
    from sentinel_engine.protocol import FacetCommand, ZoneCommand

    zone = COMMAND_ADAPTER.validate_python({"type": "zone", "zone": "bench"})
    assert isinstance(zone, ZoneCommand)
    assert zone.zone == "bench"

    facet = COMMAND_ADAPTER.validate_python({"type": "facet"})
    assert isinstance(facet, FacetCommand)


def test_unknown_command_type_is_rejected() -> None:
    with pytest.raises(ValidationError):
        COMMAND_ADAPTER.validate_python({"type": "nope"})
