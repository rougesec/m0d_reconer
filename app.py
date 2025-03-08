from flask import Flask, render_template, request, jsonify
from pymodbus.client import ModbusTcpClient
import threading

app = Flask(__name__, static_folder='static', template_folder='templates')

# Store the current scan status
scan_in_progress = False

def scan_modbus(target_ip, target_port, slave_id, start_address, end_address, scan_options, results):
    global scan_in_progress
    scan_in_progress = True
    client = ModbusTcpClient(target_ip, port=target_port)
    
    if not client.connect():
        results["error"] = "Connection failed! Check IP and Port."
        scan_in_progress = False
        return

    try:
        count = end_address - start_address + 1  # Calculate range

        if scan_options.get("scan_registers"):
            rr = client.read_holding_registers(start_address)
            results["Holding Registers"] = rr.registers if not rr.isError() else f"Error {rr}"

        if scan_options.get("scan_coils"):
            rr = client.read_coils(start_address)
            results["Coils"] = rr.bits if not rr.isError() else f"Error {rr}"

        if scan_options.get("scan_discrete_inputs"):
            rr = client.read_discrete_inputs(start_address)
            results["Discrete Inputs"] = rr.bits if not rr.isError() else f"Error {rr}"

        if scan_options.get("scan_input_registers"):
            rr = client.read_input_registers(start_address)
            results["Input Registers"] = rr.registers if not rr.isError() else f"Error {rr}"

    except Exception as e:
        results["error"] = str(e)

    client.close()
    scan_in_progress = False




def exploit_modbus(target_ip, target_port, exploit_options, results):
    client = ModbusTcpClient(target_ip, port=target_port)

    try:
        client.connect()
        if not client.connected:
            results["error"] = "Failed to connect to Modbus server."
            return

        if exploit_options.get("write_register"):
            address = int(exploit_options["register_address"])
            value = int(exploit_options["register_value"])
            rr = client.write_register(address, value, slave=1)
            results["Write Register"] = "Success" if rr else "Failed"

        if exploit_options.get("write_coil"):
            address = int(exploit_options["coil_address"])
            value = bool(exploit_options["coil_value"])
            rr = client.write_coil(address, value, slave=1)
            results["Write Coil"] = "Success" if rr else "Failed"

    except Exception as e:
        results["error"] = str(e)

    finally:
        client.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    global scan_in_progress
    if scan_in_progress:
        return jsonify({"status": "error", "message": "A scan is already in progress!"}), 400

    data = request.json
    ip = data.get("ip")
    port = int(data.get("port", 502))
    slave_id = int(data.get("slave_id", 1))  # Get from user (default: 1)
    start_address = int(data.get("start_address", 0))  # Get from user (default: 0)
    end_address = int(data.get("end_address", 10))  # Get from user (default: 10)
    
    scan_options = {
        "scan_registers": data.get("scan_registers", False),
        "scan_coils": data.get("scan_coils", False),
        "scan_discrete_inputs": data.get("scan_discrete_inputs", False),
        "scan_input_registers": data.get("scan_input_registers", False)
    }
    
    results = {}
    scan_thread = threading.Thread(target=scan_modbus, args=(ip, port, slave_id, start_address, end_address, scan_options, results))
    scan_thread.start()
    scan_thread.join()
    
    return jsonify(results)



@app.route('/exploit', methods=['POST'])
def exploit():
    data = request.json
    ip = data.get("ip")
    port = int(data.get("port", 502))
    
    exploit_options = {
        "write_register": data.get("write_register", False),
        "register_address": data.get("register_address", 0),
        "register_value": data.get("register_value", 0),
        "write_coil": data.get("write_coil", False),
        "coil_address": data.get("coil_address", 0),
        "coil_value": data.get("coil_value", False)
    }
    
    results = {}
    exploit_thread = threading.Thread(target=exploit_modbus, args=(ip, port, exploit_options, results))
    exploit_thread.start()
    exploit_thread.join()
    
    return jsonify(results)

@app.route("/stop_scan", methods=["POST"])
def stop_scan():
    global scan_in_progress
    scan_in_progress = False
    return jsonify({"status": "stopped", "message": "Scan stopped successfully!"})

if __name__ == '__main__':
    app.run(debug=True)

