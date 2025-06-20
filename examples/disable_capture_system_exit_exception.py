from pyguiadapter.adapter import GUIAdapter


def test_fix(a: int, b: int):
    print("Test Fix 1")
    raise SystemExit(0)


adapter = GUIAdapter()
# adapter.add(test_fix, capture_system_exit_exception=True)
adapter.add(test_fix, capture_system_exit_exception=False)
adapter.run()
