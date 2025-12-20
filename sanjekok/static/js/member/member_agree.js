$(document).ready(function() {
    // 체크박스 요소 선택
    const $agreeAll = $('#agree_all');
    const $agreeCheckboxes = $('.required-agree');
    const $agreeForm = $('#agreeForm');
    const $errorMsg = $('#agree-error-msg');

    // '전체 동의' 체크박스 클릭 이벤트
    $agreeAll.on('click', function() {
        $agreeCheckboxes.prop('checked', $(this).is(':checked'));
    });

    // 개별 필수 동의 체크박스 클릭 이벤트
    $agreeCheckboxes.on('click', function() {
        if ($('.required-agree:checked').length === $agreeCheckboxes.length) {
            $agreeAll.prop('checked', true);
        } else {
            $agreeAll.prop('checked', false);
        }
    });

    // 폼 제출 이벤트
    $agreeForm.on('submit', function(e) {
        let allRequiredChecked = true;
        $agreeCheckboxes.each(function() {
            if (!$(this).is(':checked')) {
                allRequiredChecked = false;
                return false; // each 루프 중단
            }
        });

        if (!allRequiredChecked) {
            e.preventDefault(); // 폼 제출 중단
            $errorMsg.show(); // 에러 메시지 표시
        } else {
            $errorMsg.hide(); // 에러 메시지 숨김
        }
    });

    // 모달 로직
    $('#show-priv-modal-btn').on('click', function(e) {
        $('#modalPrivOverlay').addClass('is-active');
    });

    $('#show-term-modal-btn').on('click', function(e) {
        $('#modalTermOverlay').addClass('is-active');
    });

    $('#show-marketing-modal-btn').on('click', function(e) {
        $('#modalMarketingOverlay').addClass('is-active');
    });

    // 모달 닫기
    $('.custom-modal-close').on('click', function() {
        const overlayId = $(this).data('close');
        if (overlayId) {
            $('#' + overlayId).removeClass('is-active');
        }
    });

    // 오버레이 클릭 시 모달 닫기
    $('.custom-modal-overlay').on('click', function(e) {
        if (e.target === this) {
            $(this).removeClass('is-active');
        }
    });
});
