$(document).ready(function () {

    // 생년월일 Flatpickr 초기화
    flatpickr("#birth_date", {
        locale: "ko",
        dateFormat: "Y-m-d",
        maxDate: "today",
    });

    // 전화번호 숫자만 입력되도록 설정
    $("#phone").on("keyup", function () {
        this.value = this.value.replace(/[^0-9]/g, '');
    }); 

    $("#phone").on("input", function () {
    this.value = this.value.replace(/[^0-9]/g, '');
    });

    $("#email").on("blur", function () {
        const regemail =/^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i
        const email = $("#email").val();
        if (!regemail.test(email)) {
            $("#EmailError").show();
        } else {
            $("#EmailError").hide();
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