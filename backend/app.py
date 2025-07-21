from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from db import SessionLocal, engine, Base
from models import Delivery

import logging

# ------------------- App Initialization ------------------- #

app = Flask(__name__)

# Enable CORS only for known frontend domain
CORS(app, origins=["http://localhost:3000"])

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create all tables (idempotent)
Base.metadata.create_all(bind=engine)


# ------------------- Routes ------------------- #

@app.route("/deliveries", methods=["POST"])
def add_delivery():
    """
    Add a new delivery to the database.
    Expects JSON payload with driver_id, start_time, end_time, hourly_rate.
    """
    session = SessionLocal()
    try:
        data = request.get_json()

        # Basic validation
        required_fields = ["driver_id", "start_time", "end_time", "hourly_rate"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        delivery = Delivery(
            driver_id=int(data["driver_id"]),
            start_time=datetime.fromisoformat(data["start_time"]),
            end_time=datetime.fromisoformat(data["end_time"]),
            hourly_rate=float(data["hourly_rate"]),
        )

        session.add(delivery)
        session.commit()

        return jsonify({"message": "Delivery added successfully"}), 201

    except (ValueError, SQLAlchemyError) as e:
        logger.exception("Failed to add delivery")
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()


@app.route("/deliveries", methods=["GET"])
def list_deliveries():
    """
    Return a list of all deliveries.
    """
    session = SessionLocal()
    try:
        deliveries = session.query(Delivery).all()
        result = [
            {
                "id": d.id,
                "driver_id": d.driver_id,
                "start_time": d.start_time.isoformat(),
                "end_time": d.end_time.isoformat(),
                "hourly_rate": d.hourly_rate,
            }
            for d in deliveries
        ]
        return jsonify(result), 200

    except SQLAlchemyError as e:
        logger.exception("Failed to fetch deliveries")
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()


@app.route("/total-cost", methods=["GET"])
def total_cost():
    """
    Calculate and return the total cost of all deliveries.
    """
    session = SessionLocal()
    try:
        deliveries = session.query(Delivery).all()
        total = 0.0

        for d in deliveries:
            duration_hours = (d.end_time - d.start_time).total_seconds() / 3600
            total += duration_hours * d.hourly_rate

        return jsonify({"total_cost": round(total, 2)}), 200

    except SQLAlchemyError as e:
        logger.exception("Failed to calculate total cost")
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()


# ------------------- Entry Point ------------------- #

if __name__ == "__main__":
    # Never use debug=True in production
    app.run(host="0.0.0.0", port=5000, debug=False)
