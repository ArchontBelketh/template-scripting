from typing import List, Set
from graph.graph import Graph
from core.type_validation import TypeValidationEngine


class GraphValidator:
    @staticmethod
    def validate(graph: Graph) -> List[str]:
        errors: List[str] = []
        
        # 1. Проверка типов подключений данных
        for conn in graph.connections:
            src_type = conn.source_pin.effective_type
            tgt_type = conn.target_pin.effective_type
            
            if not TypeValidationEngine.validate_connection(src_type, tgt_type):
                errors.append(
                    f"Несовместимые типы: нельзя подключить пин '{conn.source_pin.node.title}.{conn.source_pin.name}' "
                    f"({src_type}) к пину '{conn.target_pin.node.title}.{conn.target_pin.name}' ({tgt_type})."
                )

        # 2. Поиск циклов в графе исполнения (DFS)
        visited: Set[str] = set()
        recursion_stack: Set[str] = set()

        def dfs_check_cycles(node_id: str) -> bool:
            visited.add(node_id)
            recursion_stack.add(node_id)

            node = graph.nodes.get(node_id)
            if node:
                for out_pin in node.outputs.values():
                    if out_pin.pin_type.name == "exec":
                        for conn in out_pin.connections:
                            neighbor_id = conn.target_pin.node.id
                            if neighbor_id not in visited:
                                if dfs_check_cycles(neighbor_id):
                                    return True
                            elif neighbor_id in recursion_stack:
                                return True

            recursion_stack.remove(node_id)
            return False

        for node_id in graph.nodes:
            if node_id not in visited:
                if dfs_check_cycles(node_id):
                    errors.append("В графе исполнения обнаружен цикл!")
                    break

        return errors