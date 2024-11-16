document.addEventListener("DOMContentLoaded", () => {
    const startButton = document.getElementById("startGame");

    // Start Game and Redirect to Round Page
    startButton.addEventListener("click", () => {
        fetch("/round", { method: "GET" })
            .then((res) => res.json())
            .then((data) => {
                if (data.redirect) {
                    window.location.href = data.redirect;
                } else {
                    window.location.href = "/round"; // Proceed to the round page
                }
            })
            .catch((error) => {
                console.error("Error starting game:", error);
                alert("Failed to start the game.");
            });
    });
});