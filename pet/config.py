from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path


CONFIG_PATH = Path.home() / ".desktop_pet_config.json"


@dataclass
class AppConfig:
    pet_name: str = "Mochi"
    speed: int = 6
    color: str = "#ffb6c1"
    speech_frequency_ms: int = 6500


DEFAULT_CONFIG = AppConfig()


def load_config(path: Path = CONFIG_PATH) -> AppConfig:
    if not path.exists():
        return DEFAULT_CONFIG
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return AppConfig(**{**asdict(DEFAULT_CONFIG), **data})


def save_config(config: AppConfig, path: Path = CONFIG_PATH) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(asdict(config), f, indent=2)
