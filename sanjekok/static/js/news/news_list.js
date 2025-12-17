// static/js/news/news_list.js
document.addEventListener("DOMContentLoaded", function () {
  if (typeof flatpickr === "undefined") return;

  const startEl = document.querySelector("#startDate");
  const endEl = document.querySelector("#endDate");

  if (startEl) {
    flatpickr(startEl, {
      dateFormat: "Y-m-d",
      maxDate: "today"
    });
  }

  if (endEl) {
    flatpickr(endEl, {
      dateFormat: "Y-m-d",
      maxDate: "today"
    });
  }
});
