$(document).ready(function () {

    // 생년월일 Flatpickr 초기화
    flatpickr("#m_birth_date", {
        locale: "ko",
        dateFormat: "Y-m-d",
        maxDate: "today",
    });

    // 전화번호 숫자만 입력되도록 설정
    $("#m_phone").on("keyup", function () {
        this.value = this.value.replace(/[^0-9]/g, '');
    }); 

    $("#m_phone").on("input", function () {
    this.value = this.value.replace(/[^0-9]/g, '');
    });

    $("#m_email").on("blur", function () {
        const regemail =/^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i
        const email = $("#m_email").val();
        if (!regemail.test(email)) {
            $("#EmailError").show();
        } else {
            $("#EmailError").hide();
        }
    });

    
    if (window.firstErrorField) {
        let elementToFocus;
        if (window.firstErrorField === 'm_sex') {
            
            elementToFocus = $('#sex_male'); 
        } else {
            elementToFocus = $('#' + window.firstErrorField); 
        }
        
        if (elementToFocus && elementToFocus.length) { 
            elementToFocus.focus();
        }
    }
});

// 다음 주소 API
function searchAddress(targetId) {
    new daum.Postcode({
        oncomplete: function (data) {
            $("#" + targetId).val(data.address);
        }
    }).open();
}