from matcher import result
import pytest

@pytest.yield_fixture(autouse=True)
def setup_dummy_values():
    # nvm
    yield

def test_correct_insert():
    r = result.Result()
    r.insert(90, "High")
    assert len(r.high) == 1
    r.insert(50, "Medium")
    assert len(r.medium) == 1
    r.insert(30, "Low")
    assert len(r.low) == 1