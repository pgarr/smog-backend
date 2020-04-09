import datetime

import pytest

from notifier import get_hour_subs


@pytest.fixture
def make_subs_collection(make_subscription):
    sub1 = make_subscription("sample@test.pl", 51.1234, 21.0101, [12])
    sub2 = make_subscription("sample2@test.pl", 51.1234, 21.0101, [14, 20])
    sub3 = make_subscription("sample3@test.pl", 51.1234, 21.0101, [12, 14, 20])
    sub4 = make_subscription("sample4@test.pl", 51.1234, 21.0101, [14, 20, 24])
    sub5 = make_subscription("sample5@test.pl", 51.1234, 21.0101, [20, 24])
    return sub1, sub2, sub3, sub4, sub5


get_hours_test_data = [
    (12, (1, 3), (2, 4, 5)),
    (14, (2, 3, 4), (1, 5)),
    (20, (2, 3, 4, 5), (1,)),
    (24, (4, 5), (1, 2, 3)),
    (23, (), (1, 2, 3, 4, 5))
]


@pytest.mark.parametrize("hour,ins,notins", get_hours_test_data)
def test_get_hours_subs(test_client, database, make_subs_collection, hour, ins, notins):
    subs = get_hour_subs(hour)

    assert len(subs) == len(ins)

    for n in ins:
        assert make_subs_collection[n - 1] in subs

    for m in notins:
        assert make_subs_collection[m - 1] not in subs


actual_hours_test_data = [
    (datetime.datetime(year=2020, month=3, day=2, hour=10, minute=0, second=0), 10),
    (datetime.datetime(year=2020, month=3, day=2, hour=10, minute=0, second=1), 10),
    (datetime.datetime(year=2020, month=3, day=2, hour=10, minute=59, second=59), 10),
    (datetime.datetime(year=2020, month=3, day=2, hour=10, minute=1, second=0), 10)
]
