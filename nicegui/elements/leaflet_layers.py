from dataclasses import dataclass, field
from typing import Any, Dict, Tuple

from typing_extensions import Self

from ..dataclasses import KWONLY_SLOTS
from .leaflet_layer import Layer


@dataclass(**KWONLY_SLOTS)
class GenericLayer(Layer):
    name: str
    args: list[Any] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            'type': self.name,
            'args': self.args,
        }


@dataclass(**KWONLY_SLOTS)
class TileLayer(Layer):
    url_template: str
    options: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            'type': 'tileLayer',
            'args': [self.url_template, self.options],
        }


@dataclass(**KWONLY_SLOTS)
class Marker(Layer):
    location: Tuple[float, float]
    options: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            'type': 'marker',
            'args': [{'lat': self.location[0], 'lng': self.location[1]}, self.options],
        }

    def draggable(self, value: bool = True) -> Self:
        """Make the marker draggable."""
        self.options['draggable'] = value
        return self
