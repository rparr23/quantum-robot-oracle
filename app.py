"""Web entry point for Quantum Robot Oracle."""

import os

from flask import Flask, jsonify, render_template, request

from quantum_oracle import run_oracle
from vector_adapter import is_enabled, speak


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index():
        return render_template("index.html", vector_enabled=is_enabled())

    @app.get("/api/health")
    def health():
        return jsonify(status="ok", simulator="qiskit-aer")

    @app.post("/api/oracle")
    def oracle():
        payload = request.get_json(silent=True) or {}
        try:
            result = run_oracle(str(payload.get("question", "")), int(payload.get("shots", 1024)))
        except (ValueError, TypeError) as exc:
            return jsonify(error=str(exc)), 400
        return jsonify(result.to_dict())

    @app.post("/api/vector/speak")
    def vector_speak():
        payload = request.get_json(silent=True) or {}
        text = str(payload.get("text", "")).strip()
        if not text or len(text) > 120:
            return jsonify(error="Speech must be between 1 and 120 characters."), 400
        try:
            speak(text)
        except RuntimeError as exc:
            return jsonify(error=str(exc)), 503
        return jsonify(status="spoken")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")), debug=False)

