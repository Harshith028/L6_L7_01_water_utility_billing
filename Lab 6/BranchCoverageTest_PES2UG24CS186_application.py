
import pytest

from water_utility_billing import (
    calculate_water_bill,
    check_meter_tampering,
)


def test_account_validation_branches():
    assert calculate_water_bill([], 10)["status"] == "NO_ACTIVITY"


def test_invalid_accounts_branch():
    with pytest.raises(ValueError):
        calculate_water_bill("invalid", 10)


def test_negative_base_fee_branch():
    with pytest.raises(ValueError):
        calculate_water_bill([], -1)


def test_active_and_inactive_branches():
    result = calculate_water_bill(
        [{"is_active": False}, {"is_active": True, "usage_blocks": [10]}],
        5,
    )
    assert result["total_billed"] == 20.0


def test_usage_branches():
    result = calculate_water_bill(
        [{"is_active": True, "usage_blocks": [-1, 50, 51, 100]}],
        10,
    )
    assert result["total_billed"] == 462.5


def test_residential_break_branch():
    result = calculate_water_bill(
        [{"is_active": True, "usage_blocks": [101, 10]}], 10
    )
    assert result["total_billed"] == 464.5


def test_commercial_branch():
    result = calculate_water_bill(
        [{"is_active": True, "is_commercial": True,
          "usage_blocks": [101]}], 10
    )
    assert result["total_billed"] == 363.5


def test_waiver_condition_branches():
    result = calculate_water_bill(
        [
            {"is_active": True, "usage_blocks": [120],
             "has_leak_waiver": True},
            {"is_active": True, "usage_blocks": [10],
             "has_leak_waiver": True},
        ],
        10,
    )
    assert result["total_billed"] == 525.0


def test_excessive_flags_branch():
    result = calculate_water_bill(
        [{"is_active": True, "usage_blocks": [0, 0, 0, 0, 0, 0]}],
        10,
    )
    assert result["status"] == "EXCESSIVE_FLAGS"


def test_meter_branches():
    assert check_meter_tampering([]) == "NO_DATA"
    assert check_meter_tampering([[1, -1, 2]]) == "CLEAR"
    assert check_meter_tampering([[1, -1, -2]]) == "TAMPER_SUSPECTED"
