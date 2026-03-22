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
    if (!laneDiv) return;

    let lights = laneDiv.querySelectorAll(".light");
    if (lights.length < 3) return;

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

    let data;
    try {
        const res = await fetch(url);
        if (!res.ok) throw new Error("API returned " + res.status);
        data = await res.json();
    } catch (err) {
        document.getElementById("decision").innerText =
            "Backend not reachable. Start Flask on http://127.0.0.1:5000";
        return;
    }

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
    document.getElementById("timer").innerText = timer;

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

/* 🚀 Initial fetch */
fetchTraffic();

/* 🔁 Auto refresh every second */
setInterval(fetchTraffic, 1000);