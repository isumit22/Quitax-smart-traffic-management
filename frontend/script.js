async function fetchTraffic(emergency=false) {
    let url = "http://127.0.0.1:5000/traffic";
    if (emergency) url += "?ambulance=true";

    const res = await fetch(url);
    const data = await res.json();

    document.querySelectorAll(".lane").forEach(l => {
        l.style.background = "red";
    });

    if (data.green !== "EMERGENCY") {
        document.getElementById(data.green).style.background = "green";
    }
}

function simulateEmergency() {
    fetchTraffic(true);
}

setInterval(() => fetchTraffic(), 3000);