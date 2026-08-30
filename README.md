# Performance Lab

A Python execution visualization and analysis tool that captures what happens inside a running program.

> 🚧 **Early development** — the project is currently focused on building the execution-analysis and digital microscope backend before moving into the interactive frontend.

## What is this?

Performance Lab is being built as a **digital microscope for Python programs**.

The goal is to make program execution easier to understand by capturing and analyzing events such as:

- Function calls
- Line execution
- Function returns
- Exceptions
- Variable and program state
- Execution timing
- Function relationships
- Runtime statistics

These observations can be replayed and analyzed as a structured execution history.

Eventually, they will power an interactive interface that lets you explore a program's execution step by step.

## Current Status

### Execution Tracing

The current system can:

- Trace Python program execution
- Identify function calls and returns
- Record executed lines
- Capture exceptions
- Associate events with their source file and line number
- Capture local variable state during execution
- Store observations as structured `ExecutionEvent` objects
- Record execution timestamps

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

Performance Lab can execute a target Python program through a bootstrap layer and collect its execution events:

```text
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
```

This separates the target program from the systems that collect, analyze, and eventually visualize its execution.

### Execution Recording

The `Recorder` can replay a captured execution event stream and reconstruct program state as execution progresses.

It currently supports:

- Stepping forward through execution
- Stepping backward through execution
- Resetting execution
- Jumping directly to an execution event
- Tracking replay progress
- Rebuilding program state when navigating backward or jumping
- Tracking variables across function scopes
- Removing local state when a function returns

Example:

```text
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
```

This provides the foundation for the interactive execution timeline and digital microscope.

### Execution Analysis

Performance Lab provides higher-level analysis of a captured execution.

The system can build:

- An execution timeline
- A function call tree
- Runtime statistics
- Execution summaries
- Navigable execution history
- Reconstructable program state

These analysis tools are exposed through a unified `Execution` object.

The public API can be used as:

```python
from performance_lab import run

execution = run("examples/example.py")

execution.events
execution.recorder
execution.timeline
execution.call_tree
execution.statistics
execution.summary
```

This creates a clean boundary between the execution engine and the future visualization layer.

### Digital Microscope Backend

The project has begun building the backend model for the digital microscope.

The `ExecutionView` represents what should currently be displayed at a specific point in program execution. It can provide:

- The current execution event
- Source file and line number
- Current function
- Program state
- Current call stack
- Source-code context
- Current execution position
- Total number of events
- Execution progress

The `SourceViewer` provides source-code access around the current execution line and identifies the currently executing line.

The `Microscope` provides a high-level interface for navigating an execution:

```python
microscope.step_forward()
microscope.step_back()
microscope.reset()
microscope.jump_to(5)

view = microscope.view
```

This creates the backend interface that the future interactive visualization can consume without needing to understand the underlying tracing and replay systems.

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
│       ├── api.py
│       ├── bootstrap.py
│       ├── call_tree.py
│       ├── display.py
│       ├── events.py
│       ├── execution.py
│       ├── microscope.py
│       ├── recorder.py
│       ├── runner.py
│       ├── source.py
│       ├── state.py
│       ├── statistics.py
│       ├── summary.py
│       ├── timeline.py
│       ├── tracer.py
│       └── view.py
│
├── tests/
│   ├── test_api.py
│   ├── test_call_tree.py
│   ├── test_example.py
│   ├── test_execution.py
│   ├── test_microscope.py
│   ├── test_source.py
│   ├── test_state.py
│   ├── test_statistics.py
│   ├── test_summary.py
│   ├── test_timeline.py
│   ├── test_tracer.py
│   └── test_view.py
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

Use the public execution API:

```python
from performance_lab import run

execution = run("examples/example.py")
```

The current test suite contains **74 tests** covering execution, tracing, program state, recording, timeline navigation, call trees, statistics, summaries, the unified execution model, the public API, source-code inspection, execution views, and the digital microscope interface.

## Roadmap

### Phase 1 — Core Tracing

- [x] Basic execution event model
- [x] Python execution tracer
- [x] Function call/return tracking
- [x] Line execution tracking
- [x] Exception tracking
- [x] Local variable state capture
- [x] Execution timestamps

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
- [x] Direct event navigation
- [x] Execution progress tracking
- [x] Unified `Execution` object
- [x] Public `run()` API

### Phase 3 — Execution Analysis

- [x] Unified execution timeline
- [x] Event indexing and navigation
- [x] Function call tree
- [x] Variable/state change tracking
- [x] Runtime statistics
- [x] Execution summaries
- [x] Replay API
- [x] Unified analysis interface
- [x] Comprehensive automated test coverage

### Phase 4 — Digital Microscope

- [x] Design execution view model
- [x] Represent a single point in program execution
- [x] Source-code viewer
- [x] Source-code context around the current execution line
- [x] Current-line identification
- [x] Digital microscope navigation interface
- [x] Step through execution
- [x] Step backward through execution
- [x] Reset execution
- [x] Jump to an execution event
- [ ] Visualize program execution
- [ ] Interactive execution timeline
- [ ] Function/call visualization
- [ ] Interactive program-state inspection
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
- [ ] Support for larger and more complex Python applications

## License

This project is licensed under the MIT License.