document.addEventListener("DOMContentLoaded", () => {
    const resultsContainer = document.getElementById("evalRounds-cards");
    

    // Fetch results data
    fetch("/results", {
        method: "GET",
        headers: { "X-Requested-With": "XMLHttpRequest" }
    })
        .then((res) => {
            if(!res.ok) {
                throw new error (`HTTP error! status: ${res.status}`)
            }
            return res.json();
        })
        .then((data) => {
            if (!data.round_history) {
                resultsContainer.textContent = "No results available";
            } else {
                resultsContainer.innerHTML = `
                    <h2>Game Summary</h2>
                    ${data.round_history
                        .map(
                            (round, index) => `
                        <div>
                            <h3>Round ${index + 1}</h3>
                            <p>Market: ${round.market[0]} at ${round.market[1]}</p>
                            <p>Action: ${round.action}</p>
                            <p>Quantity: ${round.quantity}</p>
                            <p>PnL: ${round.pnl}</p>
                            <p>Player Guess: ${round.player_guess}</p>
                            <p>Correct Guess: ${round.correct_guess}</p>
                            <p>Cards1: ${round.cards.join(" ")}<p>
                        </div>`
                        )
                        .join("")}
                `;
            }
        })
        .catch((error) => {
            console.error("Error fetching results:", error);
            resultsContainer.textContent = "Failed to fetch results.";
        });

    function startNewGame(action){
        fetch("/results", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        })
            .then((res) => {
                if (!res.ok) {
                    throw new Error(`HTTP error! status: ${res.status}`);
                }
                return res.json();
            })
            .then(() => {
                window.location.href = "/round";  
            })
            .catch((error) => {
                console.error("Error starting a new game:", error);
            });    
    }

    function backToLobby(){
        window.location.href = "/";
        
    }

    document.getElementById("settings-but").addEventListener("click", backToLobby)
    document.getElementById("new-game-but").addEventListener("click", startNewGame)
});
