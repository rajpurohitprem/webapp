let tg = window.Telegram.WebApp;
tg.expand();

window.onload = async () => {
    const response = await fetch("/channels"); // termux API must serve this
    const channels = await response.json();
    const select = document.getElementById("channelSelect");

    channels.forEach(channel => {
        let option = document.createElement("option");
        option.value = channel.id;
        option.text = channel.title;
        select.appendChild(option);
    });
};

function sendSelection() {
    const selectedId = document.getElementById("channelSelect").value;
    tg.sendData(selectedId);  // Sends back to the bot
    tg.close();
}
