
import importlib
from verva import VervaManager
import ast
from astpretty import pprint

from typing import Any


class VervaVisitor(ast.NodeVisitor):

    def __init__(self) -> None:
        super().__init__()
        self.__known_checks: dict[str, str] = {}

    def visit_Import(self, node: ast.Import) -> Any:
        for name in node.names:
            # For now, just try to import the module ourselves, and then check
            # if it's registered
            # This is potentially a security issue, but I can't think of a
            # better way to do it tbh
            try:
                importlib.import_module(name.name)
            except (ImportError):
                pass
            if VervaManager.isRegistered(name.name):
                if name.asname is None:
                    asname = name.name
                else:
                    asname = name.asname
                self.__known_checks[asname] = name.name
        self.generic_visit(node)


    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        if node.module is not None:
            try:
                importlib.import_module(node.module)
            except (ImportError):
                pass
            if VervaManager.isRegistered(node.module):
                for name in node.names:
                    if name.asname is None:
                        asname = name.name
                    else:
                        asname = name.asname
                    self.__known_checks[asname] = f"{node.module}.{name.name}"
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        f = node.func
        if isinstance(f, ast.Attribute):
            if isinstance(f.value, ast.Name):
                print(f"Attribute: {f.attr}.{f.value}")
            else:
                pprint(f.value)
        elif isinstance(f, ast.Name):
            print(f"Name: {f.id}")
        else:
            pprint(node)
        self.generic_visit(node)


if __name__ == "__main__":
    v = VervaVisitor()
    ast_t = ast.parse(open("t2.py").read())
    v.visit(ast_t)
