// app.js

// Selectors
const textInput = document.getElementById("textInput");
const convertButton = document.getElementById("convertButton");
const historyList = document.getElementById("historyList");
const settingsForm = document.getElementById("settingsForm");
const historyPrompt = document.getElementById("historyPrompt");
const sampleRate = document.getElementById("sampleRate");

// Functions
async function fetchHistory() {
    const response = await fetch("http://127.0.0.1:8000/api/get-history/");
    const history = await response.json();
    updateHistory(history);
}

function updateHistory(history) {
    historyList.innerHTML = "";
    history.forEach(item => {
        const listItem = document.createElement("li");
        listItem.textContent = item.text;
        if (item.file_name) {
            const listenButton = document.createElement("button");
            listenButton.textContent = "Play";
            listenButton.onclick = () => playAudio(item.file_name);
            
            const downloadButton = document.createElement("button");
            downloadButton.textContent = "Download";
            downloadButton.onclick = () => downloadAudio(item.file_name);

            listItem.appendChild(listenButton);
            listItem.appendChild(downloadButton);
        } else {
            const loadingIcon = document.createElement("span");
            loadingIcon.textContent = " ⏳ Generating...";
            listItem.appendChild(loadingIcon);
        }
        historyList.appendChild(listItem);
    });
}

async function playAudio(fileName) {
    const audio = new Audio(`http://127.0.0.1:8000/api/get-file/?file_name=${fileName}`);
    audio.play();
}

async function downloadAudio(fileName) {
    const response = await fetch(`http://127.0.0.1:8000/api/get-file/?file_name=${fileName}`);
    if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = fileName;
        a.click();
    } else {
        alert("File is not ready yet. Please try again later.");
    }
}

async function convertTextToSpeech() {
    const text = textInput.value;
    if (!text.trim()) return;

    await fetch("http://127.0.0.1:8000/api/get-audio/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
    });

    textInput.value = "";
    fetchHistory();
}

function stopAudio() {
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
        currentAudio = null;
    }
}

async function updateSettings(event) {
    event.preventDefault();

    const params = {
        history_prompt: historyPrompt.value,
        sample_rate: parseInt(sampleRate.value, 10),
    };

    const response = await fetch("http://127.0.0.1:8000/api/send-params/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(params),
    });

    const result = await response.json();
    alert(result.message);
}

// Event Listeners
convertButton.addEventListener("click", convertTextToSpeech);
settingsForm.addEventListener("submit", updateSettings);

// Poll for history updates
timerId = setInterval(fetchHistory, 5000);
