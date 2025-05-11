from pydantic import BaseModel, Field
from typing import List, Literal, Dict

def build_prompt_model_and_string(prompts: List[Dict]) -> tuple[type[BaseModel], str]:
    """
    Given prompt definitions from frontend, return:
    - A dynamic Pydantic model for instructor (model_class)
    - A string representation of the prompt class (prompt_class_str)
    """

    annotations = {}  # For __annotations__ in model_class
    fields = {}       # For Field(...) defaults
    lines = []

    # 🔹 Step 1: Define shared sub-model: EntityEvidence
    lines.append("from pydantic import BaseModel, Field")
    lines.append("from typing import List, Literal")
    lines.append("")
   

    # 🔹 Step 2: Start outer ExtractEntities class
    lines.append("class ExtractEntities(BaseModel):")
    lines.append('    """LLM should extract structured entities and their supporting evidence as defined below."""')
    lines.append("")

    for p in prompts:
        name = p["name"].strip().replace(" ", "_")
        description = p["description"].replace('"', '\\"')
        examples = p["examples"]

        literal_type = Literal[tuple(examples)]
        literal_values = ", ".join([f'\"{e}\"' for e in examples])

        # 🔹 Step 3: Create custom nested model for this field
        nested_model = type(
            f"{name}_EntityEvidence",
            (BaseModel,),
            {
                "__annotations__": {
                    "entities": List[literal_type],
                    "evidence": List[str]
                },
                "entities": Field(..., description=f"Extracted unique entities strictly according to the definition: {description}."),
                "evidence": Field(..., description=f"Each entity must be supported by one or more exact text spans copied directly from the input. Do not paraphrase or summarize.")
            }
        )

        annotations[name] = nested_model
        fields[name] = Field(..., description=description)
        
        lines.append(f"    class {name}_EntityEvidence(BaseModel):")
        lines.append(
                     f"        entities: List[Literal[{literal_values}]] = Field(..., "
                     f"description=\"Extracted unique entities strictly according to the definition: {description}. Must exactly match one of the allowed values.\")"
)
        lines.append("        evidence: List[str] = Field(..., description=\"Each entity must be supported by one or more exact text spans copied directly from the input. Do not paraphrase or summarize.\")")
        lines.append(f"    {name}: {name}_EntityEvidence = Field(..., description=\"Provide both extracted entities and their evidence.\")")

        lines.append("")
       

    # 🔹 Step 4: Build dynamic model class
    model_class = type(
        "ExtractEntities",
        (BaseModel,),
        {
            "__annotations__": annotations,
            **fields
        }
    )

    prompt_class_str = "\n".join(lines)
    return model_class, prompt_class_str
