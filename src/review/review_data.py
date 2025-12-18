from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from src.processing.RuleProcessor import RuleProcessor
from src.processing.FileManager import FileManager


@dataclass
class RuleComparison:
    """Container linking a guideline clause to its ASP translations."""

    guideline_id: str
    guideline_text: str
    asp_rules: List[Dict[str, str]]


def _guideline_sort_key(rule_id: str) -> List[int]:
    """Convert dotted guideline IDs (e.g., 1.2.3) into sortable integer tuples."""
    parts = []
    for part in rule_id.split("."):
        try:
            parts.append(int(part))
        except ValueError:
            # Fallback for unexpected tokens (e.g., letters)
            cleaned = "".join(ch for ch in part if ch.isdigit())
            parts.append(int(cleaned) if cleaned else 0)
    return parts


def build_rule_review_dataset(guideline_path: str, lp_file_path: str) -> List[RuleComparison]:
    """
    Build a dataset that pairs each guideline clause with its ASP rule(s), if any.

    Args:
        guideline_path: Path to the guideline text file.
        lp_file_path: Path to the fired-rule .lp file (e.g., rulegen_response_fired.lp).

    Returns:
        Ordered list of RuleComparison instances, covering every guideline clause found.
    """

    processor = RuleProcessor(guideline_path)
    file_manager = FileManager()
    lp_content = file_manager.load_file(lp_file_path)

    # Choose parser based on file type / content
    if lp_file_path.endswith(".lp"):
        rule_map = processor._build_rule_map_from_lp(lp_content)
    else:
        # LLM text outputs like in_context_response.txt / zero_shot_response.txt
        rule_map = processor._build_rule_map_from_llm_txt(lp_content)

    # Group ASP rules by their base guideline ID (strip suffixes like _B).
    asp_groups: Dict[str, List[Dict[str, str]]] = {}
    for rule_id, rule_text in rule_map.items():
        base_id = rule_id.split("_")[0]
        asp_groups.setdefault(base_id, []).append(
            {"rule_id": rule_id, "rule_text": rule_text}
        )

    dataset: List[RuleComparison] = []
    for guideline_id in sorted(processor.guideline_text.keys(), key=_guideline_sort_key):
        # Skip rules with only one decimal (e.g., 1.1, 1.2, 1.3)
        # Count the number of dots to determine depth
        if guideline_id.count('.') <= 1:
            continue
            
        dataset.append(
            RuleComparison(
                guideline_id=guideline_id,
                guideline_text=processor.guideline_text[guideline_id],
                asp_rules=asp_groups.get(guideline_id, []),
            )
        )

    return dataset


