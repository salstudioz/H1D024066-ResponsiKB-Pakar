"""
Flask Application – SalstudioZ.Pakar
"""
import os, logging, logging.handlers
from flask import Flask, render_template, request, jsonify
from knowledge_base import ALL_SYMPTOMS, SYMPTOM_GROUPS
from inference import forward_chaining

app = Flask(__name__)
os.makedirs("logs", exist_ok=True)
handler = logging.handlers.RotatingFileHandler("logs/expert.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
logging.basicConfig(level=logging.INFO, handlers=[handler, logging.StreamHandler()])
logger = logging.getLogger(__name__)

@app.route("/")
def index():
    return render_template("index.html", symptom_groups=SYMPTOM_GROUPS)

@app.route("/diagnose", methods=["POST"])
def diagnose():
    try:
        data = request.get_json(force=True)
        if data is None:
            return jsonify({"error": "Body harus berupa JSON."}), 400
        symptoms = data.get("symptoms", [])
        if not isinstance(symptoms, list):
            return jsonify({"error": "Field 'symptoms' harus berupa list."}), 400
        if not symptoms:
            return jsonify({"error": "Pilih minimal satu gejala untuk memulai diagnosis."}), 400
        invalid = [s for s in symptoms if s not in ALL_SYMPTOMS]
        if invalid:
            return jsonify({"error": f"Gejala tidak dikenal: {invalid}"}), 400
        logger.info(f"POST /diagnose – symptoms={symptoms} | IP={request.remote_addr}")
        diagnoses = forward_chaining(symptoms)
        return jsonify({"diagnoses": diagnoses}), 200
    except Exception as exc:
        logger.exception(f"Error di /diagnose: {exc}")
        return jsonify({"error": "Terjadi kesalahan internal."}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5002)
