from typing import List, Dict
def build_llm_input(row: dict, selected_columns: List[str]) -> str:
    return "\n".join(f"{col}: {row.get(col, '')}" for col in selected_columns)
