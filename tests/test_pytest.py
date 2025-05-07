class A:
    x: int = 1


def test_func():
    assert A.x == 2
