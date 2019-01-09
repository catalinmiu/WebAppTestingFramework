import pytest


class PyTestParser:

    def __init__(self):
        self.collected = []

    def pytest_collection_modifyitems(self, items):
        for item in items:
            self.collected.append(item)


my_plugin = PyTestParser()
directory = '..'
pytest.main(['--collect-only', directory], plugins=[my_plugin])

for node_id in my_plugin.collected:
    print(node_id)
