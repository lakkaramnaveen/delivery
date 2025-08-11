from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError
from decimal import Decimal
import logging
import sys

from config import Config
from db import SessionLocal, engine, Base
from models import Delivery
from utils.datetime_utils import calculate_duration_and_validate

# ------------------- App Initialization ------------------- #

app = Flask(__name__)
app.config.from_object(Config)

# CORS: strict origins
CORS(app, resources={r"/*": {"origins": Config.CORS_ORIGINS}})

# Logging
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO))
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
handler.setFormatter(formatter)
app.logger.handlers.clear()
app.logger.addHandler(handler)
app.logger.setLevel(getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO))

# DB schema (idempotent)
Base.metadata.create_all(bind=engine)

# ------------------- Helpers ------------------- #

def _json_required(data: dict, fields: list[str]) -> tuple[bool, str | None]:
    """Ensure required keys exist and are not None/empty."""
    for f in fields:
        if f not in data:
            return False, f"Missing required field: {f}"
        v = data[f]
        if v is None or (isinstance(v, str) and v.strip() == ""):
            return False, f"Field '{f}' must not be empty"
    return True, None

def _to_decimal(value) -> Decimal:
    """Safe monetary/decimal conversion."""
    try:
        return Decimal(str(value))
    except Exception as exc:
        raise ValueError("hourly_rate must be a valid number") from exc

# Ensure sessions are always removed (scoped_session)
@app.teardown_appcontext
def remove_session(exc=None):
    SessionLocal.remove()

# Consistent error JSON
@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(422)
def handle_client_errors(err):
    msg = getattr(err, "description", str(err))
    return jsonify({"error": msg}), err.code if hasattr(err, "code") else 400

@app.errorhandler(Exception)
def handle_unexpected(err):
    app.logger.exception("Unhandled exception")
    # Hide internals in production
    return jsonify({"error": "Internal server error"}), 500

# ------------------- Routes ------------------- #

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/deliveries", methods=["POST"])
def add_delivery():
    """
    Add a new delivery.
    JSON body: driver_id (int), start_time (ISO), end_time (ISO), hourly_rate (number)
    """
    data = request.get_json(silent=True) or {}
    ok, msg = _json_required(data, ["driver_id", "start_time", "end_time", "hourly_rate"])
    if not ok:
        return jsonify({"error": msg}), 400

    # Validate and normalize
    try:
        driver_id = int(data["driver_id"])
    except (TypeError, ValueError):
        return jsonify({"error": "driver_id must be an integer"}), 400

    try:
        start_dt, end_dt, _duration_hours = calculate_duration_and_validate(
            data["start_time"], data["end_time"],
            allow_cross_day=True, min_minutes=1, max_hours=24.0
        )
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    try:
        rate = _to_decimal(data["hourly_rate"])
        if rate < 0:
            return jsonify({"error": "hourly_rate must be non-negative"}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    session = SessionLocal()
    try:
        delivery = Delivery(
            driver_id=driver_id,
            start_time=start_dt,
            end_time=end_dt,
            hourly_rate=rate
        )
        session.add(delivery)
        session.commit()

        return jsonify({
            "id": delivery.id,
            "driver_id": delivery.driver_id,
            "start_time": delivery.start_time.isoformat(),
            "end_time": delivery.end_time.isoformat(),
            "hourly_rate": float(delivery.hourly_rate),
        }), 201
    except (ValueError, SQLAlchemyError) as e:
        app.logger.exception("Failed to add delivery")
        session.rollback()
        # If it's a validation error we raised, surface 400; otherwise 500
        status = 400 if isinstance(e, ValueError) else 500
        msg = str(e) if status == 400 else "Database error"
        return jsonify({"error": msg}), status
    finally:
        session.close()

@app.route("/deliveries", methods=["GET"])
def list_deliveries():
    session = SessionLocal()
    try:
        deliveries = session.query(Delivery).all()
        result = [
            {
                "id": d.id,
                "driver_id": d.driver_id,
                "start_time": d.start_time.isoformat(),
                "end_time": d.end_time.isoformat(),
                "hourly_rate": float(d.hourly_rate),
            }
            for d in deliveries
        ]
        return jsonify(result), 200
    except SQLAlchemyError:
        app.logger.exception("Failed to fetch deliveries")
        return jsonify({"error": "Database error"}), 500
    finally:
        session.close()

@app.route("/total-cost", methods=["GET"])
def total_cost():
    """
    Return total cost across all deliveries.
    """
    session = SessionLocal()
    try:
        deliveries = session.query(Delivery).all()
        total = Decimal("0.00")
        for d in deliveries:
            hours = (d.end_time - d.start_time).total_seconds() / 3600.0
            total += Decimal(str(hours)) * Decimal(str(d.hourly_rate))
        return jsonify({"total_cost": float(round(total, 2))}), 200
    except SQLAlchemyError:
        app.logger.exception("Failed to calculate total cost")
        return jsonify({"error": "Database error"}), 500
    finally:
        session.close()

# ------------------- Entrypoint ------------------- #

if __name__ == "__main__":
    # Use gunicorn in production: gunicorn -w 4 -b 0.0.0.0:5000 app:app
    app.run(host="0.0.0.0", port=5000, debug=Config.DEBUG)
