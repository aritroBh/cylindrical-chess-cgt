def pytest_configure(config):
    config.addinivalue_line("markers", "slow: long perft runs (deselect with -m 'not slow')")
