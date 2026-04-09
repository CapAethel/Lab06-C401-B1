"""Utility functions for VFCare Agent"""
import json
from typing import Any, Dict, List
from datetime import datetime


def load_json(filepath: str) -> Dict[str, Any]:
    """Load JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON file: {filepath}")


def save_json(filepath: str, data: Dict[str, Any]) -> None:
    """Save data to JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_distance_km(distance: float) -> float:
    """Get distance in kilometers"""
    return distance


def format_datetime(dt_str: str) -> str:
    """Format datetime string"""
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime('%d/%m/%Y %H:%M')
    except:
        return dt_str


def evaluate_condition(condition_str: str, data: Dict[str, Any]) -> bool:
    """Evaluate a condition string against vehicle data"""
    # Simple condition evaluation
    try:
        # Extract component name and field from nested access
        # Example: "brake_system.front_pad_thickness_mm < 4.0"
        
        # This is a simplified evaluator - in production, use ast.literal_eval safely
        return eval(condition_str, {"__builtins__": {}}, flatten_dict(data))
    except Exception as e:
        print(f"Error evaluating condition: {e}")
        return False


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """Flatten nested dictionary"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def get_nested_value(data: Dict[str, Any], path: str) -> Any:
    """Get nested value from dictionary using dot notation"""
    keys = path.split('.')
    value = data
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
            if value is None:
                return None
        else:
            return None
    return value


def set_nested_value(data: Dict[str, Any], path: str, value: Any) -> None:
    """Set nested value in dictionary using dot notation"""
    keys = path.split('.')
    obj = data
    for key in keys[:-1]:
        if key not in obj:
            obj[key] = {}
        obj = obj[key]
    obj[keys[-1]] = value
