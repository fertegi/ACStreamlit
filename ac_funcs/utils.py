from dataclasses import dataclass
from typing import Any, Dict, List
from ac_funcs import aclib


def get_selected_elements() -> List[Dict[str, Any]]:
    try:
        selectedElements = aclib.RunTapirCommand(
            'GetSelectedElements', {})["elements"]
    except Exception as e:
        print(f"Error occurred while fetching selected elements: {e}")
        return []
    if not selectedElements:
        return []
    return selectedElements


def get_property_values(elements, property_ids):
    try:
        values = aclib.RunTapirCommand("GetPropertyValuesOfElements", {
            "elements": elements,
            "properties": property_ids
        })["propertyValuesForElements"]
    except:
        return []
    return values
