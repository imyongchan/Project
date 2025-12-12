$(document).ready(function () {

    // 생년월일 Flatpickr 초기화
    flatpickr("#m_birth_date", {
        locale: "ko",
        dateFormat: "Y-m-d",
        maxDate: "today",
    });

    // 전화번호 필드에 숫자만 입력되도록 설정
    $("#cel1, #cel2_1, #cel2_2").on("input", function () {
        this.value = this.value.replace(/[^0-9]/g, '');
    });

    // 이메일 도메인 선택 로직
    $('#emailaddr').on('change', function() {
        const selectedValue = $(this).val();
        if (selectedValue) {
            // 도메인을 선택한 경우
            $('#email_dns').val(selectedValue).prop('readonly', true);
        } else {
            // '직접입력'을 선택한 경우
            $('#email_dns').val('').prop('readonly', false).focus();
        }
    });

    // 폼 제출 시 유효성 검사 (선택 사항)
    $('form').on('submit', function(e) {
        // 이메일 필드 조합 후 유효성 검사
        const emailId = $('#email_id').val();
        const emailDns = $('#email_dns').val();
        if (emailId && emailDns) {
            const fullEmail = `${emailId}@${emailDns}`;
            const regemail = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i;
            if (!regemail.test(fullEmail)) {
                $('#EmailError').show();
                e.preventDefault(); // 폼 제출 중단
                return;
            }
        }
        $('#EmailError').hide();
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