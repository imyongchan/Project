btnSubmit.addEventListener("click", function () {
  const text = textarea.value.trim();
  if (!text) {
    alert("리뷰 내용을 입력하세요.");
    return;
  }
  if (currentScore === 0) {
    alert("별점을 선택하세요.");
    return;
  }

  const hospitalId = document.body.dataset.hospitalId;
  const csrftoken = getCookie("csrftoken"); // 기존에 사용 중인 CSRF 함수

  fetch("/reviews/create/", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
      "X-CSRFToken": csrftoken,
    },
    body:
      "hospital_id=" +
      encodeURIComponent(hospitalId) +
      "&rating=" +
      encodeURIComponent(currentScore) +
      "&contents=" +
      encodeURIComponent(text),
  })
    .then((res) => {
      if (!res.ok) throw new Error("error");
      return res.json();
    })
    .then((data) => {
      // 화면에 신규 리뷰 추가
      // (기존 prepend 코드 여기에서 data로 교체)
    })
    .catch(() => {
      alert("리뷰 저장 중 오류가 발생했습니다.");
    });
});
