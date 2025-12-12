document.addEventListener("DOMContentLoaded", function() {
    //  요소 가져오기
    const hamburger = document.getElementById("hamburger-btn");
    const mobileMenu = document.getElementById("mobileMenu");
    const closeBtn = document.getElementById("closeMenu");
    const overlay = document.getElementById("menuOverlay");
    const body = document.body;

    // 햄버거 버튼 클릭 → 메뉴 열기
    if (hamburger) {
        hamburger.addEventListener("click", function() {
            mobileMenu.classList.add("open");
            overlay.classList.add("active");
            body.classList.add("menu-open"); // 스크롤 방지
        });
    }

    // 닫기 버튼 클릭 → 메뉴 닫기
    if (closeBtn) {
        closeBtn.addEventListener("click", function() {
            mobileMenu.classList.remove("open");
            overlay.classList.remove("active");
            body.classList.remove("menu-open");
        });
    }

    // 오버레이 클릭 → 메뉴 닫기
    if (overlay) {
        overlay.addEventListener("click", function() {
            mobileMenu.classList.remove("open");
            overlay.classList.remove("active");
            body.classList.remove("menu-open");
        });
    }

    // 로그아웃 클릭 시 확인창
    const logoutLink = document.getElementById("logout-link");
    if (logoutLink) {
        logoutLink.addEventListener("click", function(event) {
            if (!confirm("로그아웃하시겠습니까?")) {
                event.preventDefault(); // 취소 시 이동 막기
            }
        });
    }
});
