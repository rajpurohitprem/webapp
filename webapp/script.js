async function loadChannels() {
  const res = await fetch("/channels");
  const channels = await res.json();

  const listDiv = document.getElementById("channelList");
  listDiv.innerHTML = "";

  channels.forEach(channel => {
    const btn = document.createElement("button");
    btn.textContent = channel.title;
    btn.onclick = () => sendSelection(channel.id);
    listDiv.appendChild(btn);
  });
}

async function sendSelection(channelId) {
  const res = await fetch("/save", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ channel_id: channelId })
  });

  const data = await res.json();
  alert("✅ Channel ID saved: " + data.channel_id);
}

loadChannels();
