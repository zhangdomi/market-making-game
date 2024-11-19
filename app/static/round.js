document.addEventListener("DOMContentLoaded", () => {
    const ownQuantityInput = document.getElementById("own-quantity");
    const actionPhase = document.getElementById("action-phase");
    const evalPhase = document.getElementById("eval-phase");
    const evalPrompt = document.getElementById("evaluationPrompt");
    let selectedQuantity = 0; // Predefined quantity

    function setPredefinedQuantity(qty) {
        selectedQuantity = qty; // Update the selected quantity
        ownQuantityInput.value = ""; // Clear the custom input field
    }

    ownQuantityInput.addEventListener("input", () => {
        selectedQuantity = 0; // Reset predefined quantity
    });

    // Player actions (buy, sell, skip)
    function playerAction(actionType) {
        const quantity = selectedQuantity > 0 ? selectedQuantity : parseInt(ownQuantityInput.value, 10);


        if ((!quantity || quantity <= 0) && actionType != "skip") {
            alert("Please select or enter a valid quantity.");
            return; // Prevent further execution
        }

        fetch("/round", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action_type: actionType, quantity }),
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.redirect) {
                    window.location.href = data.redirect;
                }
                else if (actionType == "skip" || data["next_round"] == true){
                    updateRound(data)
                }
                else {
                    actionPhase.style.display = "none"; // Hide action buttons
                    evalPhase.style.display = "block"; // Show evaluation phase
                    evalPrompt.textContent = `${data.message} What was your profit or loss this round?`;
                }
            })
            .catch((error) => {
                console.error("Error executing action:", error);
                alert("Action failed.");
            });
    }

    function submitPnl() {
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
                } else if (data["next_round"] == true){
                    // alert(data.message); // Feedback on PnL evaluation
                    updateRound(data);
                }
            })
            .catch((error) => {
                console.error("Error submitting PnL:", error);
                alert("Failed to submit profit/loss.");
            });
    }
    
    function updateRound(data) {
        actionPhase.style.display = "block"; // Show action buttons
        evalPhase.style.display = "none"; // Hide evaluation phase

        // Update round information dynamically without reloading the page
        document.getElementById("roundNumber").textContent = `Round ${data.round}`;
        document.getElementById("marketInfo").textContent = `The market maker quotes ${data.market_info[0]} at ${data.market_info[1]}.`;
        document.getElementById("curr-budget").textContent = `Budget: ${data.budget}`;
        ownQuantityInput.value = ""; // Reset the custom input field
        selectedQuantity = 0; // Reset predefined quantity
    }

    document.getElementById("skip").addEventListener("click", () => playerAction("skip"));
    document.getElementById("qty1").addEventListener("click", () => setPredefinedQuantity(1));
    document.getElementById("qty5").addEventListener("click", () => setPredefinedQuantity(5));
    document.getElementById("qty10").addEventListener("click", () => setPredefinedQuantity(10));

    document.getElementById("buy").addEventListener("click", () => playerAction("buy"));
    document.getElementById("sell").addEventListener("click", () => playerAction("sell"));
    document.getElementById("submitPnl").addEventListener("click", submitPnl);

});
