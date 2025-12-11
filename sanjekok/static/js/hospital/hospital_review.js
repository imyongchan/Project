// hospital/static/JS/hospital/review.js

(function () {
  const listRoot = document.getElementById("review-list");
  if (!listRoot) return;

  const hospitalId = listRoot.dataset.hospitalId;
  const listUrl = listRoot.dataset.listUrl;
  const createUrl = listRoot.dataset.createUrl;
  const deleteUrl = listRoot.dataset.deleteUrl;

  if (!hospitalId || !listUrl || !createUrl || !deleteUrl) {
    console.error("리뷰 URL 또는 병원 ID가 설정되지 않았습니다.");
    return;
  }

  const starGroup = document.getElementById("review-star-group");
  const starEls = starGroup ? starGroup.querySelectorAll(".star") : [];
  const scoreEl = document.getElementById("review-score");
  const formEl = document.getElementById("review-form");
  const textEl = document.getElementById("review-text");
  const moreBtn = document.getElementById("btn-review-more");

  let currentRating = 0;       // 1 ~ 10
  let page = 1;
  const PAGE_SIZE = 4;
  let isLoading = false;
  let hasMore = true;

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
  }
  const csrftoken = getCookie("csrftoken");

  // 별 표시 (0~10점, 5개 별 / 반칸)
  function renderStars() {
    starEls.forEach((el, idx) => {
      const starIndex = idx + 1;      // 1~5
      const fullValue = starIndex * 2;     // 2,4,6,8,10
      const halfValue = fullValue - 1;     // 1,3,5,7,9

      el.classList.remove("on", "half");

      if (currentRating >= fullValue) {
        el.classList.add("on");
      } else if (currentRating === halfValue) {
        el.classList.add("half");
      }
    });

    if (scoreEl) scoreEl.textContent = currentRating;
  }

  // 별 클릭: 왼쪽 반칸 / 오른쪽 반칸
  starEls.forEach((el) => {
    el.addEventListener("click", function (e) {
      const starIndex = parseInt(this.dataset.star, 10) || 0; // 1~5
      if (!starIndex) return;

      const rect = this.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const isLeft = clickX < rect.width / 2;

      if (isLeft) {
        // 1,3,5,7,9
        currentRating = (starIndex - 1) * 2 + 1;
      } else {
        // 2,4,6,8,10
        currentRating = starIndex * 2;
      }
      renderStars();
    });
  });

  function createReviewItemDOM(item) {
    const wrapper = document.createElement("div");
    wrapper.className = "review-item";
    wrapper.dataset.reviewId = item.id;

    const header = document.createElement("div");
    header.className = "review-header";

    const writerSpan = document.createElement("span");
    writerSpan.className = "review-writer";
    writerSpan.textContent = `작성자ID: ${item.writer}`;

    const rightBox = document.createElement("div");

    const dateSpan = document.createElement("span");
    dateSpan.className = "review-date";
    dateSpan.textContent = item.created_at;
    rightBox.appendChild(dateSpan);

    if (item.is_owner) {
      const delBtn = document.createElement("button");
      delBtn.type = "button";
      delBtn.className = "btn-review-delete";
      delBtn.textContent = "삭제";
      delBtn.addEventListener("click", function () {
        deleteReview(item.id, wrapper);
      });
      rightBox.appendChild(delBtn);
    }

    header.appendChild(writerSpan);
    header.appendChild(rightBox);

    const bodyP = document.createElement("p");
    bodyP.className = "review-body";
    bodyP.textContent = item.contents;

    // 평점 표시 (★/☆) – 반칸은 지금은 숫자로만 사용 중이면 그대로 둬도 됨
    const ratingP = document.createElement("p");
    ratingP.className = "review-rating-line";

    const labelSpan = document.createElement("span");
    labelSpan.textContent = "평점: ";
    ratingP.appendChild(labelSpan);

    // item.rating : 1~10 → 별 5개 (반칸 포함)
    for (let i = 1; i <= 5; i++) {
      const starSpan = document.createElement("span");
      starSpan.classList.add("review-star");
      starSpan.textContent = "★";

      const fullValue = i * 2;       // 2,4,6,8,10
      const halfValue = fullValue - 1; // 1,3,5,7,9

      if (item.rating >= fullValue) {
        starSpan.classList.add("full");
      } else if (item.rating === halfValue) {
        starSpan.classList.add("half");
      } else {
        starSpan.classList.add("empty");
      }

      ratingP.appendChild(starSpan);
    }

    const scoreSpan = document.createElement("span");
    scoreSpan.className = "review-score-text";
    scoreSpan.textContent = ` (${item.rating})`;
    ratingP.appendChild(scoreSpan);
    
    wrapper.appendChild(header);
    wrapper.appendChild(ratingP);
    wrapper.appendChild(bodyP);

    return wrapper;
  }

  async function loadReviews(nextPage, append) {
    if (isLoading || !hasMore) return;
    isLoading = true;

    try {
      const url = `${listUrl}?page=${nextPage}&size=${PAGE_SIZE}`;
      const resp = await fetch(url, { method: "GET" });
      if (!resp.ok) throw new Error("HTTP " + resp.status);
      const data = await resp.json();

      const reviews = data.reviews || [];
      hasMore = !!data.has_more;

      if (!append) listRoot.innerHTML = "";

      reviews.forEach((item) => {
        const dom = createReviewItemDOM(item);
        listRoot.appendChild(dom);
      });

      page = nextPage;

      if (!hasMore && moreBtn) {
        moreBtn.style.display = "none";
      } else if (moreBtn && reviews.length > 0) {
        moreBtn.style.display = "inline-block";
      }
    } catch (e) {
      console.error("리뷰 조회 실패:", e);
    } finally {
      isLoading = false;
    }
  }

  async function deleteReview(reviewId, domNode) {
    try {
      const formData = new FormData();
      formData.append("review_id", reviewId);

      const resp = await fetch(deleteUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
        },
        body: formData,
      });

      if (!resp.ok) throw new Error("HTTP " + resp.status);
      const data = await resp.json();
      if (data.success && domNode && domNode.parentNode) {
        domNode.parentNode.removeChild(domNode);
      }
    } catch (e) {
      console.error("리뷰 삭제 실패:", e);
    }
  }

  /* ======================
   * 리뷰 등록: 성공 후 페이지 새로고침
   * ====================== */
  if (formEl) {
    formEl.addEventListener("submit", async function (e) {
      e.preventDefault();

      const contents = (textEl.value || "").trim();
      if (!contents) {
        alert("리뷰 내용을 입력해 주세요.");
        return;
      }
      if (currentRating <= 0) {
        alert("평점을 선택해 주세요.");
        return;
      }

      try {
        const formData = new FormData();
        formData.append("hospital_id", hospitalId);
        formData.append("contents", contents);
        formData.append("rating", currentRating);

        const resp = await fetch(createUrl, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrftoken,
          },
          body: formData,
        });

        if (!resp.ok) throw new Error("HTTP " + resp.status);
        await resp.json();  // 저장은 이미 끝났으므로 내용은 쓰지 않아도 됨

        // 새 리뷰가 반영된 평균 평점/리뷰 수를 보기 위해 전체 새로고침
        window.location.reload();
      } catch (error) {
        console.error("리뷰 등록 실패:", error);
      }
    });
  }

  if (moreBtn) {
    moreBtn.addEventListener("click", function () {
      if (hasMore && !isLoading) {
        loadReviews(page + 1, true);
      }
    });
  }

  renderStars();
  loadReviews(1, false);
})();
