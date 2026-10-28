
import pytest

from water_utility_billing import (
    calculate_water_bill,
    check_meter_tampering,
)


def test_normal_residential():
    assert calculate_water_bill(
        [{"is_active": True, "usage_blocks": [30]}], 10
    ) == {"total_billed": 55.0, "status": "NORMAL"}


def test_invalid_accounts():
    with pytest.raises(ValueError):
        calculate_water_bill("invalid", 10)


def test_negative_fee():
    with pytest.raises(ValueError):
        calculate_water_bill([], -1)


def test_inactive_account():
    assert calculate_water_bill(
        [{"is_active": False}], 10
    )["status"] == "NO_ACTIVITY"


def test_nonpositive_usage():
    result = calculate_water_bill(
        [{"is_active": True, "usage_blocks": [0, -1]}], 10
    )
    assert result["total_billed"] == 10.0


def test_usage_over_50():
    result = calculate_water_bill(
        [{"is_active": True, "usage_blocks": [75]}], 10
    )
    assert result["total_billed"] == 197.5


def test_residential_over_100():
    result = calculate_water_bill(
        [{"is_active": True, "usage_blocks": [120, 10]}], 10
    )
    assert result["total_billed"] == 550.0


def test_commercial_over_100():
    result = calculate_water_bill(
        [{"is_active": True, "is_commercial": True,
          "usage_blocks": [120]}], 10
    )
    assert result["total_billed"] == 430.0


def test_leak_waiver():
    result = calculate_water_bill(
        [{"is_active": True, "usage_blocks": [120],
          "has_leak_waiver": True}], 10
    )
    assert result["total_billed"] == 500.0


def test_excessive_flags():
    result = calculate_water_bill(
        [{"is_active": True, "usage_blocks": [0, 0, 0, 0, 0, 0]}],
        10,
    )
    assert result["status"] == "EXCESSIVE_FLAGS"


def test_no_activity():
    assert calculate_water_bill([], 10)["status"] == "NO_ACTIVITY"


def test_meter_no_data():
    assert check_meter_tampering([]) == "NO_DATA"


def test_meter_clear():
    assert check_meter_tampering([[1, 2, -1, 3]]) == "CLEAR"


def test_meter_tampering():
    assert check_meter_tampering([[1, -1, -2]]) == "TAMPER_SUSPECTED"
