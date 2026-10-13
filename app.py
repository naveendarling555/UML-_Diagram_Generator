from flask import Flask, render_template, request, jsonify
from uml_engine import generate_uml

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    description = (data.get("description") or "").strip()
    if len(description) < 20:
        return jsonify({"error": "Please enter a system description of at least 20 characters."}), 400
    try:
        return jsonify(generate_uml(description))
    except Exception as exc:
        app.logger.exception("UML generation failed")
        return jsonify({"error": "Could not generate diagrams. Please try a clearer description."}), 500

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
