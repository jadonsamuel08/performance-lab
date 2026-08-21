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
- Capture local variable state during execution
- Store observations as structured `ExecutionEvent` objects

Example execution:

```text
example.py

    FUNCTION_CALL → greet()

    LINE_EXECUTION → line 2
        name = "Jadon"

    LINE_EXECUTION → line 3
        name = "Jadon"
        message = "Hello, Jadon!"

    FUNCTION_RETURN → "Hello, Jadon!"
```

### Isolated Execution

Performance Lab can also execute a target Python program through a bootstrap layer:

```text
Target Program
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
```

This creates the foundation for eventually separating program execution from the systems that analyze and visualize it.

## Project Structure

```text
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
│       └── tracer.py
│
├── tests/
│   ├── test_example.py
│   └── test_tracer.py
│
├── .gitignore
├── .python-version
├── LICENSE
├── pyproject.toml
├── README.md
└── uv.lock
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) for Python environment and dependency management.

Install dependencies:

```bash
uv sync
```

Run the tests:

```bash
uv run pytest
```

Run the execution bootstrap:

```bash
uv run python -m performance_lab.bootstrap examples/example.py
```

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
- [ ] Connect `Runner` to the bootstrap
- [ ] Build a clean event stream API
- [ ] Improve event filtering and serialization

### Phase 3 — Execution Analysis

- [ ] Execution timeline
- [ ] Function call tree
- [ ] Variable/state changes
- [ ] Runtime statistics
- [ ] Execution summaries
- [ ] Program execution recording

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