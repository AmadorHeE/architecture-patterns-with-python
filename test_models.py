from models import Batch, OrderLine
from datetime import date


def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch('Ref-001', sku, batch_qty, eta=date.today()),
        OrderLine('Line-001', sku, line_qty)
    )


def test_can_allocate_if_available_grater_than_required():
    large_batch, small_line = make_batch_and_line('Table-001', 20, 2)
    return large_batch.can_allocate(small_line)


def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_line = make_batch_and_line('Table-001', 2, 20)
    return small_batch.can_allocate(large_line) is False


def test_call_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line('table-001', 20, 20)
    return batch.can_allocate(line)


def test_cannot_allocate_if_skues_do_not_match():
    batch = Batch('Ref-002', 'Table-001', 20, eta=date.today())
    line = OrderLine('Order-001', 'Table-002', 2)
    return batch.can_allocate(line) is False


def test_allocate_is_idempotent():
    batch, line = make_batch_and_line('Table-001', 20, 2)
    batch.allocate(line)
    batch.allocate(line)
    return batch.available_qty == 18
