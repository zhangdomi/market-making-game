document.addEventListener("DOMContentLoaded", () => {
    const startButton = document.getElementById("startGame");

    // Start Game and Redirect to Round Page
    startButton.addEventListener("click", () => {
        window.location.href = "/round";
    })
});