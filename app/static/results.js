document.addEventListener("DOMContentLoaded", () => {
    const resultsContainer = document.getElementById("resultsContainer");
    

    // Fetch results data
    fetch("/results-data")
        .then((res) => res.json())
        .then((data) => {
            if (data.error) {
                resultsContainer.textContent = "Error: " + data.error;
            } else {
                resultsContainer.innerHTML = `
                    <h2>Game Summary</h2>
                    <pre>${JSON.stringify(data, null, 2)}</pre>
                `;
            }
        })
        .catch((error) => {
            console.error("Error fetching results:", error);
            resultsContainer.textContent = "Failed to fetch results.";
        });
});
