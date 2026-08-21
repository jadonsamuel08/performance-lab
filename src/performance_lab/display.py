from performance_lab.events import ExecutionEvent


def format_event(event: ExecutionEvent) -> str:
    event_name = event.event_type.value.upper()

    location = f"{event.file}:{event.line}"
    function = event.function

    output = f"{event_name:<16} {location:<70} {function}"

    if "locals" in event.data:
        locals_data = event.data["locals"]

        if locals_data:
            output += "\n"

            for name, value in locals_data.items():
                output += f"    {name} = {value!r}\n"

    if "return_value" in event.data:
        output += f"\n    return → {event.data['return_value']!r}"

    return output