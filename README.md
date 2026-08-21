# Performance Lab

A Python execution visualization and analysis tool that captures what happens inside a running program.

> 🚧 **Early development** — the project is currently focused on building the execution-tracing backend.

## What is this?

Performance Lab is being built as a **digital microscope for Python programs**.

The goal is to make program execution easier to understand by capturing events such as:

- Function calls
- Line execution
- Function returns
- Exceptions
- Variable and program state

Eventually, these events will power an interactive interface that lets you explore a program's execution step by step.

## Current Status

### Execution Tracing

The current prototype can:

- Trace Python program execution
- Identify function calls and returns
- Record executed lines
- Capture exceptions
- Associate events with their source file and line number
- Store observations as structured `ExecutionEvent` objects

Example execution:

    example.py
        │
        ├── FUNCTION_CALL → greet()
        ├── LINE_EXECUTION → line 2
        ├── LINE_EXECUTION → line 3
        └── FUNCTION_RETURN → "Hello, Jadon!"

## Project Structure

    performance-lab/
    ├── examples/
    │   └── example.py
    │
    ├── src/
    │   └── performance_lab/
    │       ├── __init__.py
    │       ├── events.py
    │       └── tracer.py
    │
    └── tests/
        ├── test_example.py
        └── test_tracer.py

## Development

This project uses [uv](https://docs.astral.sh/uv/) for Python environment and dependency management.

Install dependencies:

    uv sync

Run the tests:

    uv run pytest

## Roadmap

- [x] Basic execution event model
- [x] Python execution tracer
- [x] Function call/return tracking
- [x] Line execution tracking
- [x] Exception tracking
- [ ] Variable state tracking
- [ ] Execution recording
- [ ] Replay engine
- [ ] Call graph visualization
- [ ] Interactive execution timeline
- [ ] Web-based frontend
- [ ] Performance and memory analysis

## License

This project is licensed under the MIT License.