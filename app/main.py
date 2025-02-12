from flask import Flask, request, jsonify
from database import db, init_db
from models import Reservation

app = Flask(__name__)

# Inicializar base de datos con configuración desde .env
init_db(app)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Reservation Service is running"})


@app.route("/create_reservation/", methods=["POST"])
def create_reservation():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    try:
        new_reservation = Reservation(
            user_id=data["user_id"],
            date=data["date"],
            time=data["time"],
            status="Confirmed"
        )
        db.session.add(new_reservation)
        db.session.commit()
        return jsonify({"id": new_reservation.id, "status": new_reservation.status}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/update_reservation/<int:reservation_id>", methods=["PUT"])
def update_reservation(reservation_id):
    data = request.json
    if not data or "status" not in data:
        return jsonify({"error": "Invalid JSON"}), 400

    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404

    try:
        reservation.status = data["status"]
        db.session.commit()
        return jsonify({"message": f"Reservation {reservation_id} updated to {data['status']}"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/reservation/<int:reservation_id>", methods=["GET"])
def get_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404

    return jsonify({
        "id": reservation.id,
        "user_id": reservation.user_id,
        "date": reservation.date,
        "time": reservation.time,
        "status": reservation.status
    })


@app.route("/delete_reservation/<int:reservation_id>", methods=["DELETE"])
def delete_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404

    try:
        db.session.delete(reservation)
        db.session.commit()
        return jsonify({"message": f"Reservation {reservation_id} deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
