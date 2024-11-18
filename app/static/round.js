document.addEventListener("DOMContentLoaded", () => {
    const ownQuantityInput = document.getElementById("own-quantity");
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

        if (!quantity || quantity <= 0) {
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
                } else {
                    showEvaluationPhase(data.message); // Display action result
                }
            })
            .catch((error) => {
                console.error("Error executing action:", error);
                alert("Action failed.");
            });
    }

    function showEvaluationPhase(actionMessage) {
        const roundContent = document.querySelector(".market-and-action"); // Locate the container
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
                } else if (data.next_round){
                    alert(data.message); // Feedback on PnL evaluation
                    // loadMarket(); // Proceed to the next rond    
                    // updateRound(data);
                }
            })
            .catch((error) => {
                console.error("Error submitting PnL:", error);
                alert("Failed to submit profit/loss.");
            });
    }

    // function updateRound(data) {
    //     // Update DOM elements with new round data
    //     roundNumberElement.textContent = `Round ${data.round}`;
    //     marketInfoElement.textContent = `The market maker quotes ${data.market_info[0]} at ${data.market_info[1]}.`;
    //     currBudgetElement.textContent = `Budget: ${data.budget}`;
    //     // Reset input fields for the next round
    //     ownQuantityInput.value = "";
    //     selectedQuantity = 0;
    // }
    

    document.getElementById("qty1").addEventListener("click", () => setPredefinedQuantity(1));
    document.getElementById("qty5").addEventListener("click", () => setPredefinedQuantity(5));
    document.getElementById("qty10").addEventListener("click", () => setPredefinedQuantity(10));

    document.getElementById("buy").addEventListener("click", () => playerAction("buy"));
    document.getElementById("sell").addEventListener("click", () => playerAction("sell"));
    document.getElementById("skip").addEventListener("click", () => playerAction("skip"));

});
