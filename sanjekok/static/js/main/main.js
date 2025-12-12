function toggleMenu() {
    const nav = document.getElementById("menu");
    nav.classList.toggle("open");
}

document.addEventListener('DOMContentLoaded', function() {
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(event) {
            if (!confirm("로그아웃하시겠습니까?")) {
                event.preventDefault(); // 사용자가 '취소'를 누르면 링크 이동을 막음
            }
        });
    }
});