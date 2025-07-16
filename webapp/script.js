document.addEventListener("DOMContentLoaded", async () => {
  const list = document.getElementById("channelList");

  try {
    const res = await fetch("https://nor-gives-officially-canada.trycloudflare.com/channels");
    
    // Log the raw response for debug
    const text = await res.text();
    console.log("🔍 Raw response:", text);

    // Try to parse it as JSON
    const channels = JSON.parse(text);
    console.log("✅ Parsed channels:", channels);

    list.innerHTML = "";

    channels.forEach(channel => {
      const btn = document.createElement("button");
      btn.textContent = `✅ ${channel.title}`;
      btn.onclick = async () => {
        const saveRes = await fetch("https://nor-gives-officially-canada.trycloudflare.com/save", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ channel_id: channel.id })
        });
        console.log("📥 Save response:", await saveRes.text());
        alert("✅ Saved channel ID: " + channel.id);
      };
      list.appendChild(btn);
    });

  } catch (err) {
    console.error("❌ Error loading channels:", err);
    alert("Failed to load channels: " + err.message);
    list.innerHTML = "<b>❌ Failed to load channels</b>";
  }
});
