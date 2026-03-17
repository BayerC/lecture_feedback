import base64
import json
import struct

from pytest_bdd import scenario, then
from streamlit.testing.v1 import AppTest

from open_cups.types import UserStatus
from tests.bdd.fixture import MockTime
from tests.bdd.test_helper import refresh_all_apps


def _get_trace_y_values(trace: dict) -> list:
    """Extract y-values from a trace, handling both list and encoded formats."""
    y_data = trace.get("y", [])
    if isinstance(y_data, dict) and "bdata" in y_data:
        # Decode base64 encoded data
        decoded = base64.b64decode(y_data["bdata"])
        dtype = y_data.get("dtype", "f8")
        if dtype == "i1":
            return list(decoded)
        if dtype == "f8":
            return list(struct.unpack(f"{len(decoded) // 8}d", decoded))
        msg = f"Unsupported dtype: {dtype}"
        raise ValueError(msg)
    return list(y_data)


@scenario(
    "features/distribution_history.feature",
    "Host views distribution history",
)
def test_host_views_distribution_history(mock_time: MockTime) -> None:
    pass


@then("I should see the distribution history empty state")
def i_should_see_distribution_history_empty_state(
    context: dict[str, AppTest],
) -> None:
    plotly_charts = context["me"].get("plotly_chart")
    assert len(plotly_charts) == 1, "Expected exactly one plotly chart"

    chart_proto = plotly_charts[0].proto
    spec = json.loads(chart_proto.spec)

    trace_names = {trace["name"] for trace in spec["data"]}
    expected_names = {status.value for status in UserStatus} | {
        f"{status.value} (inactive)" for status in UserStatus
    }
    assert trace_names == expected_names

    for trace in spec["data"]:
        y_values = _get_trace_y_values(trace)
        assert len(y_values) == 2, (
            "Empty state should have exactly two data points "
            "per trace (original + extended)"
        )
        assert all(val == 0 for val in y_values), (
            f"Trace '{trace['name']}' should have all zero values in empty state"
        )


@then("I should see the user on the distribution history chart")
def i_should_see_distribution_history_chart(context: dict[str, AppTest]) -> None:
    refresh_all_apps(context)
    plotly_charts = context["me"].get("plotly_chart")
    assert len(plotly_charts) == 1, "Expected exactly one plotly chart"

    chart_proto = plotly_charts[0].proto
    spec = json.loads(chart_proto.spec)

    trace_names = {trace["name"] for trace in spec["data"]}
    expected_names = {status.value for status in UserStatus} | {
        f"{status.value} (inactive)" for status in UserStatus
    }
    assert trace_names == expected_names

    all_y_values = []
    for trace in spec["data"]:
        y_values = _get_trace_y_values(trace)
        all_y_values.extend(y_values)

    assert any(val > 0 for val in all_y_values), (
        "At least one user should be visible in the distribution history chart"
    )
