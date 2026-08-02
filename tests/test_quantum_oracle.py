import pytest

from quantum_oracle import build_circuit, run_oracle


def test_circuit_has_hadamard_and_measurement():
    operations = build_circuit().count_ops()
    assert operations["h"] == 1
    assert operations["measure"] == 1


def test_seeded_oracle_returns_complete_distribution():
    result = run_oracle("Is this quantum?", shots=128, seed=42)
    assert sum(result.counts.values()) == 128
    assert sum(result.probabilities.values()) == pytest.approx(1.0)
    assert result.answer in {"Yes", "No"}
    assert "H" in result.circuit


@pytest.mark.parametrize("question", ["", "   "])
def test_question_is_required(question):
    with pytest.raises(ValueError, match="Please ask"):
        run_oracle(question)


def test_shots_are_bounded_to_supported_values():
    with pytest.raises(ValueError, match="Unsupported"):
        run_oracle("Question?", shots=1_000_000)

