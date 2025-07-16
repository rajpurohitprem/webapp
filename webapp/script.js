document.addEventListener("DOMContentLoaded", async () => {
  const list = document.getElementById("channelList");

  try {
    const res = await fetch("https://burner-gem-yr-classification.trycloudflare.com/channels");
    const channels = await res.json();

    list.innerHTML = "";

    channels.forEach(channel => {
      const btn = document.createElement("button");
      btn.textContent = `✅ ${channel.title}`;
      btn.onclick = async () => {
        await fetch("https://burner-gem-yr-classification.trycloudflare.com/save", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ channel_id: channel.id })
        });
        alert("Saved channel ID: " + channel.id);
      };
      list.appendChild(btn);
    });
  } catch (err) {
    console.error(err);
    list.innerHTML = "<b>❌ Failed to load channels</b>";
  }
});
