function getSuggestions() {
    let query = document.getElementById("search").value;
    let suggestionsDiv = document.getElementById("suggestions");

    if (query.length === 0) {
        suggestionsDiv.innerHTML = "";
        return;
    }

    fetch(`/autocomplete?query=${query}`)
        .then(response => response.json())
        .then(data => {
            suggestionsDiv.innerHTML = "";
            if (data.length === 0) {
                return;
            }

            data.forEach(word => {
                let div = document.createElement("div");
                div.textContent = word;
                div.classList.add("suggestion-item");
                div.onclick = () => {
                    document.getElementById("search").value = word;
                    suggestionsDiv.innerHTML = "";
                };
                suggestionsDiv.appendChild(div);
            });
        })
        .catch(error => console.error("Error fetching suggestions:", error));
}
