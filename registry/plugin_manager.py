import importlib.util
from pathlib import Path


class PluginManager:
    def __init__(self):
        self.plugins = []

    def load_plugins(
        self,
        plugins_directory="plugins",
    ):
        path = Path(plugins_directory)

        if not path.exists():
            return

        for file in path.glob("*.py"):
            self.load_plugin(file)

    def load_plugin(self, file_path):
        module_name = file_path.stem

        spec = importlib.util.spec_from_file_location(
            module_name,
            file_path,
        )

        if not spec:
            return

        module = importlib.util.module_from_spec(
            spec
        )

        spec.loader.exec_module(module)

        self.plugins.append(module)