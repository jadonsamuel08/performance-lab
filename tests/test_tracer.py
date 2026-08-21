from performance_lab.events import EventType
from performance_lab.tracer import Tracer


def test_tracer_records_execution():
    tracer = Tracer(__file__)

    tracer.start()

    def add(a: int, b: int) -> int:
        result = a + b
        return result

    result = add(2, 3)

    tracer.stop()

    assert result == 5
    assert len(tracer.events) > 0

    event_types = {event.event_type for event in tracer.events}

    assert EventType.FUNCTION_CALL in event_types
    assert EventType.LINE_EXECUTION in event_types
    assert EventType.FUNCTION_RETURN in event_types