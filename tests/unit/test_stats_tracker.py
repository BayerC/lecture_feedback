import pytest

from conftest import MockTime
from open_cups.stats_tracker import Config, StatsTracker
from open_cups.types import UserSession, UserStatus


def test_config_errors() -> None:
    with pytest.raises(ValueError, match="dense_snapshot_interval must be > 0"):
        Config(dense_snapshot_interval_seconds=0)

    with pytest.raises(ValueError, match="sparse_snapshot_interval must be > 0"):
        Config(sparse_snapshot_interval_seconds=0)

    with pytest.raises(ValueError, match="dense_sampling_window must be >= 0"):
        Config(dense_sampling_window_seconds=-1)

    with pytest.raises(ValueError, match="max_sparse_snapshot_count must be > 0"):
        Config(max_sparse_snapshot_count=0)

    with pytest.raises(
        ValueError,
        match="dense_sampling_window must be >= dense_snapshot_interval",
    ):
        Config(dense_snapshot_interval_seconds=10, dense_sampling_window_seconds=5)

    with pytest.raises(
        ValueError,
        match="dense_snapshot_interval must be <= sparse_snapshot_interval",
    ):
        Config(dense_snapshot_interval_seconds=10, sparse_snapshot_interval_seconds=5)

    with pytest.raises(
        ValueError,
        match="dense_snapshot_interval must be > 0, sparse_snapshot_interval must be > 0",  # noqa: E501
    ):
        Config(
            dense_snapshot_interval_seconds=0,
            sparse_snapshot_interval_seconds=0,
        )


def test_status_history_snapshot_interval(mock_time: MockTime) -> None:
    mock_time.current_time = 10.0

    unit = StatsTracker(
        config=Config(
            dense_snapshot_interval_seconds=1,
            dense_sampling_window_seconds=100,
            sparse_snapshot_interval_seconds=10,
            max_sparse_snapshot_count=10,
        ),
    )

    unit.record_status_snapshot(
        [UserSession(UserStatus.GREEN, 0.0), UserSession(UserStatus.YELLOW, 0.0)],
    )
    history = unit.status_history
    assert len(history) == 1
    assert history[0].counts[UserStatus.GREEN] == 1
    assert history[0].counts[UserStatus.YELLOW] == 1
    assert history[0].counts[UserStatus.RED] == 0
    assert history[0].counts[UserStatus.UNKNOWN] == 0

    mock_time.current_time = 11.0
    unit.record_status_snapshot(
        [UserSession(UserStatus.GREEN, 0.0), UserSession(UserStatus.YELLOW, 0.0)],
    )
    history = unit.status_history
    assert len(history) == 2
    assert history[-1].counts[UserStatus.GREEN] == 1
    assert history[-1].counts[UserStatus.YELLOW] == 1


def test_status_history_trims_old_snapshots(mock_time: MockTime) -> None:
    unit = StatsTracker(
        config=Config(
            dense_snapshot_interval_seconds=1,
            dense_sampling_window_seconds=10,
            sparse_snapshot_interval_seconds=5,
            max_sparse_snapshot_count=2,
        ),
    )

    mock_time.current_time = 1.0
    unit.record_status_snapshot([UserSession(UserStatus.GREEN, 0.0)])
    mock_time.current_time = 6.0
    unit.record_status_snapshot([UserSession(UserStatus.YELLOW, 0.0)])
    mock_time.current_time = 11.0
    unit.record_status_snapshot([UserSession(UserStatus.RED, 0.0)])
    mock_time.current_time = 27.0
    unit.record_status_snapshot([UserSession(UserStatus.GREEN, 0.0)])

    history = unit.status_history
    assert len(history) == 3
    assert history[0].timestamp == 6.0
    assert history[1].timestamp == 11.0
    assert history[2].timestamp == 27.0


def test_sparse_sampling_outside_dense_window(mock_time: MockTime) -> None:
    unit = StatsTracker(
        Config(
            dense_snapshot_interval_seconds=1,
            dense_sampling_window_seconds=10,
            sparse_snapshot_interval_seconds=5,
            max_sparse_snapshot_count=1000,
        ),
    )

    for i in range(30):
        mock_time.current_time = float(i)
        unit.record_status_snapshot([UserSession(UserStatus.GREEN, 0.0)])

    history = unit.status_history
    last_time = 29.0
    dense_cutoff = last_time - 10.0

    dense_snapshots = [s for s in history if s.timestamp >= dense_cutoff]
    assert len(dense_snapshots) == 11
    assert dense_snapshots[0].timestamp == 19.0
    assert dense_snapshots[1].timestamp == 20.0
    assert dense_snapshots[-1].timestamp == 29.0

    sparse_snapshots = [s for s in history if s.timestamp < dense_cutoff]
    assert len(sparse_snapshots) == 4
    assert sparse_snapshots[0].timestamp == 0.0
    assert sparse_snapshots[1].timestamp == 5.0
    assert sparse_snapshots[2].timestamp == 10.0
    assert sparse_snapshots[3].timestamp == 15.0


def test_disregard_samples_provided_quicker_than_dense_interval(
    mock_time: MockTime,
) -> None:
    unit = StatsTracker(
        Config(
            dense_snapshot_interval_seconds=5,
            dense_sampling_window_seconds=30,
            sparse_snapshot_interval_seconds=30,
            max_sparse_snapshot_count=1000,
        ),
    )

    for i in range(10):
        mock_time.current_time = float(i)
        unit.record_status_snapshot([UserSession(UserStatus.GREEN, 0.0)])

    history = unit.status_history
    assert len(history) == 2
    assert history[0].timestamp == 0.0
    assert history[1].timestamp == 5.0
