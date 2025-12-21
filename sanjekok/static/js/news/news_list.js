// static/js/news/news_list.js
document.addEventListener("DOMContentLoaded", function () {
  if (typeof flatpickr === "undefined") return;

  const startEl = document.querySelector("#startDate");
  const endEl = document.querySelector("#endDate");

   const commonOptions = {
    locale: "ko",
    dateFormat: "Y-m-d",
    maxDate: "today",

    monthSelectorType: "dropdown",   // 월 dropdown
    yearSelectorType: "dropdown",    // 연도 dropdown
    yearRange: [1990, new Date().getFullYear()],
    allowInput: false
  };

  if (startEl) {
    flatpickr(startEl, commonOptions);
  }

  if (endEl) {
    flatpickr(endEl, commonOptions);
  }
});
