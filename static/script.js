function startScan() {
    let ip = document.getElementById("ip").value;
    let port = document.getElementById("port").value;
    let slave_id = document.getElementById("slave_id").value;
    let start_address = document.getElementById("start_address").value;
    let end_address = document.getElementById("end_address").value;

    let scan_options = {
        ip: ip,
        port: port,
        slave_id: parseInt(slave_id),
        start_address: parseInt(start_address),
        end_address: parseInt(end_address),
        scan_registers: document.getElementById("scan_registers").checked,
        scan_coils: document.getElementById("scan_coils").checked,
        scan_discrete_inputs: document.getElementById("scan_discrete_inputs").checked,
        scan_input_registers: document.getElementById("scan_input_registers").checked
    };

    fetch("/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(scan_options)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("results").innerText = JSON.stringify(data, null, 2);
    });
}

function stopScan() {
    fetch("/stop_scan", { method: "POST" })
    .then(response => response.json())
    .then(data => {
        document.getElementById("results").innerText = JSON.stringify(data, null, 2);
    });
}

function startExploit() {
    let ip = document.getElementById("ip").value;
    let port = document.getElementById("port").value;

    let exploit_options = {
        ip: ip,
        port: port,
        write_register: document.getElementById("write_register").checked,
        register_address: document.getElementById("register_address").value,
        register_value: document.getElementById("register_value").value,
        write_coil: document.getElementById("write_coil").checked,
        coil_address: document.getElementById("coil_address").value,
        coil_value: document.getElementById("coil_value").checked
    };

    fetch("/exploit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(exploit_options)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("results").innerText = JSON.stringify(data, null, 2);
    });
}

