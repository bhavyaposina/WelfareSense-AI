
from flask import Flask, render_template, request, jsonify

from engine.eligibility import load_schemes, analyze_scheme
from engine.gap_analysis import generate_gap_analysis
from engine.recommendation import (
    generate_guidance,
    rank_recommendations
)
from engine.nlp_parser import parse_profile

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/results")
def results_page():
    return render_template("results.html")


def analyze_profile(user):
    schemes = load_schemes()
    results = []

    for scheme in schemes:
        criterion_results = analyze_scheme(user, scheme)
        gap_analysis = generate_gap_analysis(criterion_results)
        guidance = generate_guidance(scheme, gap_analysis)

        results.append({
            "scheme": scheme.get("name", "Unknown Opportunity"),
            "type": scheme.get("type", "welfare"),
            "description": scheme.get("description", ""),
            "criteria": criterion_results,
            "gap_analysis": gap_analysis,
            "guidance": guidance
        })

    return rank_recommendations(results)


def normalize_user(data):
    return {
        "name": str(data.get("name") or ""),
        "age": int(data.get("age") or 0),
        "income": int(data.get("income") or 0),
        "occupation": str(data.get("occupation") or "").strip(),
        "education": str(data.get("education") or "").strip(),
        "state": str(data.get("state") or "").strip(),
        "category": str(data.get("category") or "").strip(),
        "area": str(data.get("area") or "").strip(),
        "service_type": str(
            data.get("service_type") or ""
        ).strip()
    }


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "No valid profile data received."
        }), 400

    try:
        user = normalize_user(data)

        if user["age"] < 0 or user["income"] < 0:
            raise ValueError("Age and income cannot be negative.")

        results = analyze_profile(user)

        return jsonify({
            "success": True,
            "user": user,
            "results": results
        })

    except (ValueError, TypeError) as error:
        return jsonify({
            "success": False,
            "message": str(error) or "Invalid profile information."
        }), 400

    except Exception:
        app.logger.exception("Manual profile analysis failed")
        return jsonify({
            "success": False,
            "message": "The analysis failed. Check the Flask terminal."
        }), 500


@app.route("/analyze-text", methods=["POST"])
def analyze_text():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "No valid text was received."
        }), 400

    text = str(data.get("text") or "").strip()

    if not text:
        return jsonify({
            "success": False,
            "message": "Please describe your profile first."
        }), 400

    try:
        extracted_profile = parse_profile(text)

        user = normalize_user(extracted_profile)

        missing_fields = []

        required_fields = {
            "age": user["age"] > 0,
            "income": user["income"] > 0,
            "occupation": bool(user["occupation"]),
            "education": bool(user["education"]),
            "state": bool(user["state"]),
            "category": bool(user["category"]),
            "area": bool(user["area"]),
            "service_type": bool(user["service_type"])
        }

        for field, present in required_fields.items():
            if not present:
                missing_fields.append(field)

        # Return extracted details even if some fields are missing.
        # The frontend can show which details need confirmation.
        results = analyze_profile(user)

        return jsonify({
            "success": True,
            "user": user,
            "extracted_profile": user,
            "missing_fields": missing_fields,
            "results": results
        })

    except Exception:
        app.logger.exception("Natural-language profile analysis failed")
        return jsonify({
            "success": False,
            "message": (
                "Unable to analyze the text. "
                "Check the Flask terminal for the exact error."
            )
        }), 500


@app.route("/parse-profile", methods=["POST"])
def parse_profile_route():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "No valid request data received."
        }), 400

    text = str(data.get("text") or "").strip()

    if not text:
        return jsonify({
            "success": False,
            "message": "Please enter some text."
        }), 400

    try:
        profile = parse_profile(text)

        return jsonify({
            "success": True,
            "profile": profile
        })

    except Exception:
        app.logger.exception("NLP parser test failed")
        return jsonify({
            "success": False,
            "message": "Profile parsing failed. Check the Flask terminal."
        }), 500


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
