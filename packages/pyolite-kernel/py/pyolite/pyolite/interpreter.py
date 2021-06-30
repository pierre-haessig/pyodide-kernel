from IPython.core.history import HistoryManager
from IPython.core.interactiveshell import InteractiveShell
from pyodide_js import loadPackagesFromImports as _load_packages_from_imports

__all__ = ["Interpreter"]


class CustomHistoryManager(HistoryManager):
    def __init__(self, shell=None, config=None, **traits):
        self.enabled = False
        super(CustomHistoryManager, self).__init__(shell=shell, config=config, **traits)


class Interpreter(InteractiveShell):
    def __init__(self, kernel, *args, **kwargs):
        self.kernel = kernel
        super(Interpreter, self).__init__(*args, **kwargs)

    def init_history(self):
        self.history_manager = CustomHistoryManager(shell=self, parent=self)
        self.configurables.append(self.history_manager)

    async def run(self, code):
        exec_code = self.transform_cell(code)
        await _load_packages_from_imports(exec_code)
        self.result = self.run_cell(code)
