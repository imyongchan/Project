$(document).ready(function() {
    // 체크박스 및 버튼 요소 선택
    const $agreeAll = $('#agree_all');
    const $agreeCheckboxes = $('.required-agree');
    const $nextButton = $('#submitBtn');

    function updateNextButtonState() {
        let allRequiredChecked = true;
        $agreeCheckboxes.each(function() {
            if (!$(this).is(':checked')) {
                allRequiredChecked = false;
                return false;
            }
        });
        $nextButton.prop('disabled', !allRequiredChecked);
    }

    $agreeAll.on('click', function() {
        $agreeCheckboxes.prop('checked', $(this).is(':checked'));
        updateNextButtonState();
    });

    $agreeCheckboxes.on('click', function() {
        if ($('.required-agree:checked').length === $agreeCheckboxes.length) {
            $agreeAll.prop('checked', true);
        } else {
            $agreeAll.prop('checked', false);
        }
        updateNextButtonState();
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

    // 초기 상태 설정
    updateNextButtonState();
});
