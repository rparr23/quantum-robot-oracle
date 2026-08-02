# Quantum Robot Oracle

An approachable, production-shaped teaching app that turns a yes/no question into a one-qubit experiment. It prepares a Hadamard circuit, runs it with Qiskit Aer, visualizes the circuit, explains measurement, and can optionally hand the answer to an Anki Vector robot.

![CI](https://github.com/rparr23/quantum-robot-oracle/actions/workflows/ci.yml/badge.svg)

## Why this project

This modern educational adaptation is inspired by James Weaver's article, [“A Robot and a Quantum Computer”](https://medium.com/qiskit/a-robot-and-a-quantum-computer-41d6c778a5bf), and Devanshi Arora's original [`ibmq-anki-vector`](https://github.com/DevanshiArora40/ibmq-anki-vector) project. Their playful bridge between embodied robotics and quantum computing made this learning experience possible. See [NOTICE.md](NOTICE.md) for complete attribution.

For recruiters and engineering reviewers, the project demonstrates:

- a tested Python service with clear domain boundaries
- real Qiskit Aer simulation and circuit serialization
- a dependency-isolated optional hardware adapter
- a responsive, accessible web interface with live probability results
- deterministic unit tests, API tests, containerization, and CI

## Try it locally

Requires Python 3.11+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open <http://localhost:8000>. Ask any yes/no question, choose the number of shots, and run the oracle. The answer is sampled from the measured qubit; it is educational randomness, not prediction.

## How it works

1. Start in `|0⟩`.
2. Apply a Hadamard gate to create equal superposition.
3. Measure the qubit with Qiskit Aer.
4. Show counts, probabilities, and the circuit diagram.
5. Choose the majority outcome as the robot's spoken answer (ties use the first sampled result).

The browser calls `POST /api/oracle` with a question and shot count. The response contains counts, normalized probabilities, a text circuit, and the sampled answer.

## Optional Anki Vector

The simulator works without a robot. To enable hardware support, install the optional SDK and configure the robot according to the [`anki_vector` documentation](https://developer.anki.com/vector/docs/initial.html):

```bash
pip install -r requirements-vector.txt
set VECTOR_ENABLED=1        # PowerShell: $env:VECTOR_ENABLED="1"
```

The API endpoint `POST /api/vector/speak` stays disabled unless `VECTOR_ENABLED=1`. The adapter imports the SDK lazily, so normal development and CI never require robot hardware.

## Test and quality checks

```bash
pytest
ruff check .
```

## Docker

```bash
docker build -t quantum-robot-oracle .
docker run --rm -p 8000:8000 quantum-robot-oracle
```

Then visit <http://localhost:8000>. The container intentionally excludes the robot SDK and hardware access.

## Project map

```text
app.py                 Flask routes and validation
quantum_oracle.py      Qiskit circuit and simulation domain logic
vector_adapter.py      Optional, lazy-loaded Anki Vector integration
templates/index.html   Accessible application shell
static/                Interface styling and interaction
tests/                 Domain and API tests
.github/workflows/     Continuous integration
```

## Responsible use

The oracle is a demonstration of quantum measurement. It cannot forecast events or make informed decisions. Do not use its output for medical, legal, financial, safety, or other consequential choices.

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE). Copyright 2026 Richard Parr and contributors.

