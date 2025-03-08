# M0D-Reconer

This tool is a Flask-based web application designed to scan and exploit Modbus devices over TCP. It allows users to enumerate Modbus registers and coils, as well as perform write operations for exploitation purposes.

## Features
✅ Scan Modbus devices for:
- Holding Registers
- Coils
- Discrete Inputs
- Input Registers  

✅ Exploit functionality to:
- Write to Holding Registers
- Write to Coils  

✅ Simple web-based interface for ease of use.


## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/modbus-scanner-exploiter.git
cd m0d_reconer
```

### 2️⃣ Create a Python Virtual Environment
```bash
python -m venv modbus
```

### 2️⃣ Activate the Virtual Environment
```bash
source modbus/bin/activate
```

### 3️⃣ Install Required Dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Running the Application
Start the Flask server by running:
```bash
python app.py
```
By default, the application runs on http://127.0.0.1:5000/.

## ⚠️ Disclaimer
This tool is for educational purposes only. Unauthorized scanning or exploitation of Modbus devices without permission is illegal. The authors are not responsible for any misuse of this tool.

## 📜 License
This project is open-source and can be modified or distributed under appropriate licensing terms.
