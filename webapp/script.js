document.addEventListener("DOMContentLoaded", async () => {
  const list = document.getElementById("channelList");

  try {
    const res = await fetch("https://nor-gives-officially-canada.trycloudflare.com/channels");
    const channels = await res.json();

    console.log("Received channels:", channels); // Log the raw response

    list.innerHTML = "";

    // Ensure it's an array
    if (!Array.isArray(channels)) {
      throw new Error("Server did not return a channel list. Response: " + JSON.stringify(channels));
    }

    // Create a button for each channel
    channels.forEach(channel => {
      const btn = document.createElement("button");
      btn.textContent = `✅ ${channel.title}`;
      btn.onclick = async () => {
        try {
          await fetch("https://nor-gives-officially-canada.trycloudflare.com/save", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ channel_id: channel.id })
          });
          alert("✅ Saved channel ID: " + channel.id);
        } catch (saveErr) {
          alert("❌ Failed to save channel: " + saveErr.message);
        }
      };
      list.appendChild(btn);
    });

    if (channels.length === 0) {
      list.innerHTML = "<b>ℹ️ You haven't joined any channels.</b>";
    }

  } catch (err) {
    console.error(err);
    alert("❌ Failed to load channels: " + err.message);
    list.innerHTML = "<b>❌ Failed to load channels</b>";
  }
});
