$(document).ready(function () {

    /* =========================
       공통 에러 표시 함수
    ========================= */
    function showError(fieldId, message) {
        const $input = $('#' + fieldId);
        const $error = $('#' + fieldId + '-error');

        $input.addClass('is-invalid');
        $error.text(message).show();
    }

    function clearError(fieldId) {
        const $input = $('#' + fieldId);
        const $error = $('#' + fieldId + '-error');

        $input.removeClass('is-invalid');
        $error.hide().text('');
    }

    /* =========================
       생년월일 Flatpickr
    ========================= */
    flatpickr("#m_birth_date", {
        locale: "ko",
        dateFormat: "Y-m-d",
        minDate: "1900-01-01",
        maxDate: "today",
        onChange: function () {
            clearError('m_birth_date');
        }
    });

    /* =========================
       숫자만 입력
    ========================= */
    $("#cel1, #cel2_1, #cel2_2").on("input", function () {
        this.value = this.value.replace(/[^0-9]/g, '');
    });

    /* =========================
       이메일 도메인 선택
    ========================= */
    $('#emailaddr').on('change', function () {
        const val = $(this).val();
        if (val) {
            $('#email_dns').val(val).prop('readonly', true).trigger('blur');
        } else {
            $('#email_dns').val('').prop('readonly', false).focus();
        }
    });

    /* =========================
       실시간 검증
    ========================= */

    // 이름
    $('#m_name').on('input blur', function () {
        const value = $(this).val().trim();
        const regex=/^(?=.*[가-힣a-zA-Z0-9])[가-힣a-zA-Z0-9_](?:[가-힣a-zA-Z0-9_ ]{0,18}[가-힣a-zA-Z0-9_])?$/;
                
        if (!value) {
            showError('m_name', '이름을 입력해주세요.');
        } else if (!regex.test(value)) {
            showError('m_name', '이름은 한글, 영어, 숫자, _, 공백만 입력 가능하며 1~20글자까지 가능합니다.');
        } else {
            clearError('m_name');
        }
    });

    // 생년월일
    $('#m_birth_date').on('blur', function () {
        if (!$(this).val()) {
            showError('m_birth_date', '생년월일을 선택해주세요.');
        }
    });

    // 집 주소
    $('#m_address').on('blur', function () {
        if (!$(this).val().trim()) {
            showError('m_address', '집 주소를 입력해주세요.');
        } else {
            clearError('m_address');
        }
    });

    // 직장 주소
    $('#m_jaddress').on('blur', function () {
        if (!$(this).val().trim()) {
            showError('m_jaddress', '직장 주소를 입력해주세요.');
        } else {
            clearError('m_jaddress');
        }
    });

    // 전화번호 (선택)
    $('#cel1, #cel2_1, #cel2_2').on('input blur', function () {
        const c1 = $('#cel1').val();
        const c2 = $('#cel2_1').val();
        const c3 = $('#cel2_2').val();

        if (c1 || c2 || c3) {
            if (c1.length !== 3 || c2.length !== 4 || c3.length !== 4) {
                showError('m_phone', '전화번호를 올바르게 입력해주세요.');
            } else {
                clearError('m_phone');
            }
        } else {
            clearError('m_phone');
        }
    });

    // 이메일 (선택)
    $('#email_id, #email_dns').on('input blur', function () {
        const id = $('#email_id').val().trim();
        const dns = $('#email_dns').val().trim();

        if (!id && !dns) {
            clearError('m_email');
            return;
        }

        const email = `${id}@${dns}`;
        const regex = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,}$/;

        if (!regex.test(email)) {
            showError('m_email', '이메일 형식이 올바르지 않습니다.');
        } else {
            clearError('m_email');
        }
    });

    /* =========================
       submit 최종 검증
    ========================= */
    $('form').on('submit', function (e) {
        const $submitButton = $('.btn-next');

        if ($submitButton.is(':disabled')) {
            e.preventDefault();
            return;
        }

        // 모든 필드 강제 검증
        $('#m_name, #m_birth_date, #m_address, #m_jaddress, #cel1, #email_id')
            .trigger('blur');

        if ($('.is-invalid').length > 0) {
            e.preventDefault();
            $('.is-invalid').first().focus();
            return;
        }

        $submitButton.prop('disabled', true).text('가입 처리 중...');
    });

    /* =========================
       서버 사이드 에러 포커스
    ========================= */
    if (window.firstErrorField) {
        const target = window.firstErrorField === 'm_sex'
            ? $('#sex_male')
            : $('#' + window.firstErrorField);

        if (target.length) {
            target.focus();
        }
    }
});

/* =========================
   다음 주소 API
========================= */
function searchAddress(targetId) {
    new daum.Postcode({
        oncomplete: function (data) {
            $("#" + targetId).val(data.address).trigger('blur');
        }
    }).open();
}
