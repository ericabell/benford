from app import process_line


def test_process_line():
    r = process_line('Alabama	Bay Minette 	8342')
    assert r == [8342]
    r = process_line('1 2 3')
    assert r == [1, 2, 3]
