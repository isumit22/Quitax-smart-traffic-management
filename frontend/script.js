let currentLane = null;
let timer = 0;

/* 🔁 Reset all lights */
function resetLights() {
    document.querySelectorAll(".light").forEach(light => {
        light.classList.remove("active");
    });
}

/* 🚦 Set signal properly */
function setSignal(lane) {
    resetLights();

    let laneDiv = document.getElementById(lane);
    let lights = laneDiv.querySelectorAll(".light");

    // Step 1: Yellow
    lights[1].classList.add("active");

    setTimeout(() => {
        lights[1].classList.remove("active");

        // Step 2: Green
        lights[2].classList.add("active");
    }, 1000);
}

/* 🌐 Fetch traffic data */
async function fetchTraffic(emergency=false) {
    let url = "http://127.0.0.1:5000/traffic";
    if (emergency) url += "?ambulance=true";

    const res = await fetch(url);
    const data = await res.json();

    // 🚗 Update vehicle count
    for (let lane in data.lanes) {
        document.getElementById("count" + lane).innerText =
            data.lanes[lane] + " vehicles";
    }

    // 🚦 Change signal if needed
    if (data.green !== currentLane) {
        currentLane = data.green;
        setSignal(currentLane);

        // dynamic timer (based on traffic)
        timer = Math.max(5, data.lanes[currentLane] * 1);
    }

    // ⏱ Update timer
    document.getElementById("timer").innerText =
        "⏱ Timer: " + timer + "s";

    if (timer > 0) timer--;

    // 🧠 Decision explanation
    document.getElementById("decision").innerText =
        "Green → Lane " + data.green + " (highest traffic)";

    // 🚑 Emergency mode UI
    if (data.emergency) {
        document.body.style.background = "#550000";
        document.getElementById("decision").innerText =
            "🚑 Emergency Override Activated!";
    } else {
        document.body.style.background = "#111";
    }
}

/* 🚑 Emergency trigger */
function simulateEmergency() {
    fetchTraffic(true);
}

/* 🔁 Auto refresh every second */
setInterval(fetchTraffic, 1000);