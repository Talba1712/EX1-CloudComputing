from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

parking_lot_status = {}
ticket_id_counter = 0

@app.route('/entry', methods=['POST'])
def entry():
    global ticket_id_counter
    plate = request.args.get('plate')
    parking_lot = request.args.get('parkingLot')
    ticket_id = ticket_id_counter
    ticket_id_counter += 1
    parking_lot_status[ticket_id] = {'plate': plate, 'parking_lot': parking_lot, 'entry_time': datetime.datetime.now()}
    return jsonify({'ticket_id': ticket_id})

@app.route('/exit', methods=['POST'])
def exit():
    ticket_id = int(request.args.get('ticketId'))
    if ticket_id not in parking_lot_status:
        return jsonify({'error': 'Invalid ticket ID'})
    entry_time = parking_lot_status[ticket_id]['entry_time']
    exit_time = datetime.datetime.now()
    parked_time = (exit_time - entry_time).total_seconds() / 60.0
    parked_time_hours = parked_time / 60.0
    charge = round(parked_time_hours * 10, 2)
    plate = parking_lot_status[ticket_id]['plate']
    parking_lot = parking_lot_status[ticket_id]['parking_lot']
    del parking_lot_status[ticket_id]
    return jsonify({'plate': plate, 'parking_lot': parking_lot, 'parked_time': parked_time, 'charge': charge})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
