document.addEventListener("DOMContentLoaded", () => {
    const marketInfo = document.getElementById("marketInfo");
    // const feedback = document.getElementById("feedback");
    const ownQuantityInput = document.getElementById("own-quantity");            //inputted quantity
    let selectedQuantity = 0;       //predefined quantity

    // Load market data when the page loads
    function loadMarket() {
        fetch("/round", { method: "GET" })
            .then((res) => res.json())
            .then((data) => {
                if (data.redirect) {
                    window.location.href = data.redirect; // Redirect to results if game is over
                } else {
                    marketInfo.textContent = `The market maker quotes ${data.market_info[0]} at ${data.market_info[1]}.`;
                    document.getElementById("roundNumber").textContent = 'Round ${data.round}';
                    document.getElementById("curr-budget").textContent = `Budget: ${data.budget}`;

                }
            })
            .catch((error) => {
                console.error("Error loading market:", error);
                feedback.textContent = "Failed to fetch market data.";
            });
    }

    function setPredefinedQuantity(qty) {
        selectedQuantity = qty; // Update the selected quantity
        ownQuantityInput.value = ""; // Clear the custom input field
    }

    ownQuantityInput.addEventListener("input", () => {
        selectedQuantity = 0; // Reset predefined quantity
    });

    // Player actions (buy, sell, skip)
    function playerAction(actionType) {        
        const customQuantity = parseInt(ownQuantityInput.value, 10);
        
        const quantity = 0;
        if (selectedQuantity == 0){
            quantity = customQuantity > 0 ? customQuantity : alert("Please select or enter a valid quantity.")
        }
        else{
            quantity = selectedQuantity
        }

        fetch("/round", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action_type: actionType, quantity: parseInt(quantity, 10) }),
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.redirect){
                    window.location.href = data.redirect
                }
                else{
                    showEvaulationPhase(data.message)               //display action result
                }
            })
            .catch((error) => {
                console.error("Error executing action:", error);
                feedback.textContent = "Action failed.";
            });
    }

    function showEvaulationPhase(actionMessage){
        roundContent.innerHTML = `
            <div class="round-evaluation">
                <p id="evaluationPrompt">${actionMessage} What was your profit or loss this round?</p>
                <label for="pnlInput" class="text-muted">Use a minus sign (-) for losses.</label>
                <input type="number" id="pnlInput" placeholder="Enter profit/loss">
                <button id="submitPnl">Submit</button>
            </div>
        `;
        document.getElementById("submitPnl").addEventListener("click", submitPnl);
    }

    function submitPnl(){
        const pnlGuess = parseInt(document.getElementById("pnlInput").value, 10);

        if (isNaN(pnlGuess)) {
            alert("Please enter a valid number for profit or loss.");
            return;
        }

        fetch("/round", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ guess: pnlGuess }),
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.redirect) {
                    window.location.href = data.redirect;
                } else {
                    alert(data.message); // Feedback on PnL evaluation
                    loadMarket(); // Proceed to the next round
                }
            })
            .catch((error) => {
                console.error("Error submitting PnL:", error);
                alert("Failed to submit profit/loss.");
            });
    }

    document.getElementById("qty1").addEventListener("click", () => setPredefinedQuantity(1));
    document.getElementById("qty5").addEventListener("click", () => setPredefinedQuantity(5));
    document.getElementById("qty10").addEventListener("click", () => setPredefinedQuantity(10));

    document.getElementById("buy").addEventListener("click", () => playerAction("buy"));
    document.getElementById("sell").addEventListener("click", () => playerAction("sell"));
    document.getElementById("skip").addEventListener("click", () => playerAction("skip"));

    loadMarket()
});
