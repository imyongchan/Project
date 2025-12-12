$(document).ready(function () {
    // 생년월일 Flatpickr 초기화
    flatpickr("#i_accident_date", {
        locale: "ko",
        dateFormat: "Y-m-d",
        maxDate: "today",
    });

    const industryMap = {
        "광업": ["석탄광업 및 채석업", "석회석·금속·비금속광업 및 기타광업"],
        "제조업": ["식료품제조업", "섬유 및 섬유제품 제조업", "목재 및 종이제품 제조업", "출판·인쇄·제지업", "화학 및 고무제품 제조업", "의약품·화장품·연탄·석유제품제조업", "기계기구·금속·비금속광물제품제조업", "금속제련업", "전기기계기구·정밀기구·전자제품제조업", "자동차 및 수리업", "수제품 및 기타제품 제조업"],
        "전기·가스·증기 및 수도사업": ["전기·가스·증기 및 수도사업"],
        "건설업": ["건설업"],
        "운수·창고 및 통신업": ["철도·항공·창고·운수관련서비스업", "육상 및 수상운수업", "통신업"],
        "임업": ["임업"],
        "어업": ["어업"],
        "농업": ["농업"],
        "금융 및 보험업": ["금융 및 보험업"],
        "기타의 사업": ["시설관리및사업지원서비스업", "해외파견자", "전문·보건·교육·여가관련서비스업", "도소매·음식·숙박업", "부동산업 및 임대업", "국가 및 지방자치단체의 사업", "주한미군", "기타의 각종사업"]
    };

    // ⬆ 업종 대분류 채우기
    const $cat1 = $("#i_industry_type1");
    $.each(industryMap, function (key, value) {
        $cat1.append(`<option value="${key}">${key}</option>`);
    });

    // 업종 대분류 → 중분류 연동
    $("#i_industry_type1").on("change", function () {
        const selected = $(this).val();
        const $cat2 = $("#i_industry_type2");
        $cat2.empty().append(`<option value="">중분류 선택</option>`);
        if (!selected) return;
        $.each(industryMap[selected], function (idx, item) {
            $cat2.append(`<option value="${item}">${item}</option>`);
        });
    });

    /* 발생형태 리스트 */
    const occList = ["떨어짐", "넘어짐", "부딪힘", "물체에 맞음", "무너짐", "끼임", "절단·베임·찔림", "감전", "폭발·파열", "화재", "깔림·뒤집힘", "이상온도 물체접촉", "빠짐·익사", "광산사고", "불균형 및 무리한 동작", "화학물질 누출·접촉", "산소결핍", "사업장내 교통사고", "사업장외 교통사고", "업무상질병", "체육행사등의 사고", "폭력행위", "동물상해", "기타", "분류불능"];

    /* 질병 리스트 */
    const disList = ["직업병", "진폐증", "소음성난청", "이상기압", "진동장해", "물리적인자 기타", "이황화탄소", "트리클로로에틸렌(TCE)", "기타유기화합물", "벤젠", "타르", "염화비닐", "디이소시아네이트", "석면", "기타화학물질", "연", "수은", "크롬", "카드M", "망간", "감염성질환", "독성간염", "직업성피부질환", "직업성암", "직업병 기타", "작업관련성 질병", "뇌혈관질환", "심장질환", "뇌·심혈관질환", "신체부담작업", "비사고성요통", "사고성요통", "수근관증후군", "간질환", "정신질환", "작업관련성 기타"];

    const $occInput = $("#occInput");
    const $disInput = $("#disInput");

    function updateModeInputs() {
        const mode = $("input[name='mode']:checked").val();
        if (mode === "occ") {
            $occInput.prop("disabled", false);
            $disInput.prop("disabled", true).val("");
        } else if (mode === "dis") {
            $occInput.prop("disabled", true).val("");
            $disInput.prop("disabled", false);
        } else { // 'all'
            $occInput.prop("disabled", false);
            $disInput.prop("disabled", false);
        }
    }

    // 변경 시 즉시 적용
    $("input[name='mode']").on("change", updateModeInputs);

    // 페이지 로드 시 기본 설정 ('모두' 선택 상태 반영)
    updateModeInputs();
    
    /* input 클릭 → 모달 오픈  */
    $occInput.on("mousedown", function (e) {   
        e.preventDefault();                    
        e.stopPropagation();                   
        if (!$occInput.prop("disabled")) {
            openModal("occ");
        }
    });

    $disInput.on("mousedown", function (e) {   
        e.preventDefault();
        e.stopPropagation();
        if (!$disInput.prop("disabled")) {
            openModal("dis");
        }
    });

    /* 모달 닫기 */
    $("#modal").on("click", ".close-btn", function () {
        closeModal();
    });
    
    // 모달 외부 클릭 시 닫기
    $(window).on("click", function(event) {
        if ($(event.target).is("#modal")) {
            closeModal();
        }
    });

    /* 모달 열기 함수 */
    function openModal(type) {
        const $modal = $("#modal");
        const $modalGrid = $("#modalGrid");
        const $modalTitle = $("#modalTitle");
        $modalGrid.empty();
        if (type === "occ") {
            $modalTitle.text("발생형태 선택");
            createGrid(occList, $occInput);
        } else {
            $modalTitle.text("질병 선택");
            createGrid(disList, $disInput);
        }
        $modal.css("display", "flex");
    }

    /* 모달 닫기 함수 */
    function closeModal() {
        $("#modal").hide();
    }

    /* 그리드 생성 (jQuery) */
    function createGrid(list, $targetInput) {
        const $modalGrid = $("#modalGrid");
        $.each(list, function (index, item) {
            const $div = $("<div>").text(item);
            $div.on("click", function () {
                $targetInput.val(item);
                closeModal();
            });
            $modalGrid.append($div);
        });
    }

    // Form submission validation
    $("#add-info-form").on("submit", function (e) {
        e.preventDefault(); // Stop submission immediately

        // Reset all error messages
        $("#accidentDateError").hide();
        $("#addressError").hide();
        $("#mode-error").hide();

        // Check date
        if ($("#i_accident_date").val().trim() === "") {
            $("#accidentDateError").show();
            const dateInput = $("#i_accident_date");
            dateInput.focus();
            if (dateInput[0] && dateInput[0]._flatpickr) {
                dateInput[0]._flatpickr.close();
            }
            return; // Stop validation
        }

        // Check address
        if ($("#i_address").val().trim() === "") {
            $("#addressError").show();
            $("#i_address").focus();
            return; // Stop validation
        }

        // Check mode and corresponding inputs
        const mode = $("input[name='mode']:checked").val();
        const occValue = $("#occInput").val().trim();
        const disValue = $("#disInput").val().trim();
        let modeIsValid = true;

        if (!mode) {
            modeIsValid = false;
        } else if (mode === "occ" && occValue === "") {
            modeIsValid = false;
        } else if (mode === "dis" && disValue === "") {
            modeIsValid = false;
        } else if (mode === "all" && (occValue === "" || disValue === "")) {
            modeIsValid = false;
        }

        if (!modeIsValid) {
            $("#mode-error").show();
            // Focus on the relevant input
            if (!mode) {
                 $("input[name='mode']").first().focus();
            } else if (mode === 'occ') {
                 $("#occInput").focus();
            } else if (mode === 'dis') {
                 $("#disInput").focus();
            } else if (mode === 'all') {
                occValue === "" ? $("#occInput").focus() : $("#disInput").focus();
            }
            return; // Stop validation
        }
        
        // If all validation passes, submit the form
        this.submit();
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
