document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("searchInput");
  const resultsContainer = document.getElementById("autocompleteResults");
  const form = document.getElementById("searchForm");

  if (!input || !resultsContainer || !form) return;

  function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        func.apply(this, args);
      }, delay);
    };
  }

  const fetchSuggestions = debounce(function (query) {
    fetch(`/api/location-autocomplete/?q=${encodeURIComponent(query)}`)
      .then((response) => response.json())
      .then((data) => {
        resultsContainer.innerHTML = "";

        if (data.length === 0) {
          const noResultRow = document.createElement("div");
          noResultRow.className = "autocomplete-no-results";
          noResultRow.textContent = "No locations found";
          resultsContainer.appendChild(noResultRow);
          resultsContainer.style.display = "block";
          return;
        }

        data.forEach((item) => {
          const row = document.createElement("div");
          row.className = "autocomplete-row";
          row.textContent = `${item.name}`;

          row.addEventListener("click", function () {
            input.value = item.name;
            resultsContainer.style.display = "none";
            form.submit();
          });
          resultsContainer.appendChild(row);
        });

        resultsContainer.style.display = "block";
      })
      .catch((err) => console.error("Autocomplete fetch error:", err));
  }, 300);

  input.addEventListener("input", function () {
    const query = input.value.trim();

    if (query.length < 1) {
      resultsContainer.style.display = "none";
      return;
    }

    fetchSuggestions(query);
  });

  document.addEventListener("click", function (e) {
    if (!input.contains(e.target) && !resultsContainer.contains(e.target)) {
      resultsContainer.style.display = "none";
    }
  });
});
