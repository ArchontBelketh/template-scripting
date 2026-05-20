import ast


class ASTGenerator:
    def generate(
        self,
        root_node,
    ):
        module = root_node.build_ast()

        ast.fix_missing_locations(
            module
        )

        return ast.unparse(module)