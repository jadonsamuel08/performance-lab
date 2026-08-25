# Performance Lab

A Python execution visualization and analysis tool that captures what happens inside a running program.

> 🚧 **Early development** — the project is currently focused on building the execution-tracing and replay backend.

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
- Capture local variable state during execution
- Store observations as structured `ExecutionEvent` objects

Example execution:

    example.py

        FUNCTION_CALL → greet()

        LINE_EXECUTION → line 2
            name = "Jadon"

        LINE_EXECUTION → line 3
            name = "Jadon"
            message = "Hello, Jadon!"

        FUNCTION_RETURN → "Hello, Jadon!"

### Isolated Execution

Performance Lab can execute a target Python program through a bootstrap layer and collect its execution events:

    Target Program
          │
          ▼
       Runner
          │
          ▼
      Bootstrap
          │
          ▼
        Tracer
          │
          ▼
    Execution Events
          │
          ▼
         JSON

This separates the target program from the systems that collect, analyze, and eventually visualize its execution.

### Execution Recording

The `Recorder` can replay a captured execution event stream and reconstruct program state as execution progresses.

It currently supports:

- Stepping forward through execution
- Stepping backward through execution
- Resetting execution
- Rebuilding program state when stepping backward
- Tracking variables across function scopes
- Removing local state when a function returns

Example:

    Step forward

        name = "Jadon"

            ↓

    Enter greet()

        name = "Jadon"
        message = "Hello, Jadon!"

            ↓

    Return from greet()

        name = "Jadon"

            ↓

    Execute result = greet(name)

        name = "Jadon"
        result = "Hello, Jadon!"

This is the foundation for the eventual interactive execution timeline and digital microscope.

## Project Structure

    performance-lab/

    │
    ├── examples/
    │   └── example.py
    │
    ├── src/
    │   └── performance_lab/
    │       ├── __init__.py
    │       ├── bootstrap.py
    │       ├── events.py
    │       ├── recorder.py
    │       ├── runner.py
    │       ├── state.py
    │       └── tracer.py
    │
    ├── tests/
    │   ├── test_example.py
    │   ├── test_state.py
    │   └── test_tracer.py
    │
    ├── .gitignore
    ├── .python-version
    ├── LICENSE
    ├── pyproject.toml
    ├── README.md
    └── uv.lock

## Development

This project uses [uv](https://docs.astral.sh/uv/) for Python environment and dependency management.

Install dependencies:

    uv sync

Run the tests:

    uv run pytest

Run the execution bootstrap:

    uv run python -m performance_lab.bootstrap examples/example.py

The current test suite contains 12 tests covering execution, tracing, state tracking, and replay behavior.

## Roadmap

### Phase 1 — Core Tracing

- [x] Basic execution event model
- [x] Python execution tracer
- [x] Function call/return tracking
- [x] Line execution tracking
- [x] Exception tracking
- [x] Local variable state capture

### Phase 2 — Execution Engine

- [x] Target program isolation
- [x] Bootstrap execution layer
- [x] Structured event serialization
- [x] Connect `Runner` to the bootstrap
- [x] Build a clean event stream API
- [x] Program state reconstruction
- [x] Execution recording
- [x] Forward execution stepping
- [x] Backward execution stepping
- [x] State reconstruction during rewind
- [ ] Improve event filtering and serialization

### Phase 3 — Execution Analysis

- [ ] Unified execution timeline
- [ ] Event indexing and navigation
- [ ] Function call tree
- [ ] Variable/state change tracking
- [ ] Runtime statistics
- [ ] Execution summaries
- [ ] Replay API

### Phase 4 — Digital Microscope

- [ ] Visualize program execution
- [ ] Interactive execution timeline
- [ ] Function/call visualization
- [ ] Step through execution
- [ ] Inspect program state at each step
- [ ] Navigate between source code and execution events

### Phase 5 — Interactive Frontend

- [ ] Build web-based interface
- [ ] Interactive source viewer
- [ ] Execution visualization
- [ ] State inspection
- [ ] Call graph visualization
- [ ] Full execution dashboard

### Future Exploration

- [ ] Performance analysis
- [ ] Memory analysis
- [ ] Execution comparisons
- [ ] Advanced debugging capabilities
- [ ] Support for larger Python projects

## License

This project is licensed under the MIT License.