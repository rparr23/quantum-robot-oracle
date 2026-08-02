"""Quantum simulation domain logic for the educational oracle."""

from dataclasses import asdict, dataclass

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


ALLOWED_SHOTS = {128, 256, 512, 1024, 2048, 4096}


@dataclass(frozen=True)
class OracleResult:
    question: str
    answer: str
    winning_state: str
    shots: int
    counts: dict[str, int]
    probabilities: dict[str, float]
    circuit: str

    def to_dict(self) -> dict:
        return asdict(self)


def build_circuit() -> QuantumCircuit:
    circuit = QuantumCircuit(1, 1, name="oracle")
    circuit.h(0)
    circuit.measure(0, 0)
    return circuit


def run_oracle(question: str, shots: int = 1024, seed: int | None = None) -> OracleResult:
    cleaned = question.strip()
    if not cleaned:
        raise ValueError("Please ask a yes/no question.")
    if len(cleaned) > 240:
        raise ValueError("Question must be 240 characters or fewer.")
    if shots not in ALLOWED_SHOTS:
        raise ValueError("Unsupported shot count.")

    circuit = build_circuit()
    simulator = AerSimulator(seed_simulator=seed)
    compiled = transpile(circuit, simulator)
    raw_counts = simulator.run(compiled, shots=shots).result().get_counts()
    counts = {state: int(raw_counts.get(state, 0)) for state in ("0", "1")}
    probabilities = {state: round(counts[state] / shots, 6) for state in counts}
    winning_state = "1" if counts["1"] > counts["0"] else "0"

    return OracleResult(
        question=cleaned,
        answer="Yes" if winning_state == "1" else "No",
        winning_state=winning_state,
        shots=shots,
        counts=counts,
        probabilities=probabilities,
        circuit=str(circuit.draw(output="text")),
    )

