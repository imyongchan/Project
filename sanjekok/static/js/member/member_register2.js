$(document).ready(function () {

    // 생년월일 Flatpickr 초기화
    flatpickr("#birth_date", {
        locale: "ko",
        dateFormat: "Y-m-d",
        maxDate: "today",
    });

    // 전화번호 숫자만 입력되도록
    $("#phone").on("beforeinput", function (e) {
        if (e.originalEvent.data && !/^[0-9]$/.test(e.originalEvent.data)) {
            e.preventDefault();
        }
    });

});

// 다음 주소 API
function searchAddress(targetId) {
    new daum.Postcode({
        oncomplete: function (data) {
            $("#" + targetId).val(data.address);
        }
    }).open();
}