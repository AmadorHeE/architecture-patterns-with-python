from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()

    def __repr__(self):
        return f'<Batch {self.reference}>'

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return self.reference == other.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    @property
    def allocated_quantity(self) -> int:
        return self._purchased_quantity - self.available_qty

    @property
    def available_qty(self) -> int:
        return sum(line.qty for line in self._allocations)

    def can_allocate(self, line: OrderLine):
        return self.sku == line.sku and self.allocated_quantity >= line.qty

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)
