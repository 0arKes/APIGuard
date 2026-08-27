const historySquares = document.querySelectorAll(".square-history");

const historyDate = document.querySelector("#history-date");
const historyTime = document.querySelector("#history-time");
const historyStatusCode = document.querySelector("#history-status-code");
const historyApiResponse = document.querySelector("#history-api-response");
const historyResponseTime = document.querySelector("#history-response-time");

const divHistory = document.querySelector(".history-information");

historySquares.forEach((square) => {

    square.addEventListener("click", () => {

        divHistory.style.display = "flex";

        historyDate.textContent = square.dataset.date;
        historyTime.textContent = square.dataset.time;
        historyStatusCode.textContent = square.dataset.statusCode;
        historyApiResponse.textContent = square.dataset.apiResponse;
        historyResponseTime.textContent =
            square.dataset.responseTime === "N/A"
            ? "N/A"
            : `${square.dataset.responseTime} ms`;

    });

});