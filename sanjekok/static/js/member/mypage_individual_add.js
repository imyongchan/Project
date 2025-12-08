$(document).ready(function () {

    // 생년월일 Flatpickr 초기화
    flatpickr("#i_accident_date", {
        locale: "ko",
        dateFormat: "Y-m-d",
        maxDate: "today",
    });

    const industryMap = {

    "광업": [
        "석탄광업 및 채석업",
        "석회석·금속·비금속광업 및 기타광업"
    ],

    "제조업": [
        "식료품제조업",
        "섬유 및 섬유제품 제조업",
        "목재 및 종이제품 제조업",
        "출판·인쇄·제지업",
        "화학 및 고무제품 제조업",
        "의약품·화장품·연탄·석유제품제조업",
        "기계기구·금속·비금속광물제품제조업",
        "금속제련업",
        "전기기계기구·정밀기구·전자제품제조업",
        "자동차 및 수리업",
        "수제품 및 기타제품 제조업"
    ],

    "전기·가스·증기 및 수도사업": [
        "전기·가스·증기 및 수도사업"
    ],

    "건설업": [
        "건설업"
    ],

    "운수·창고 및 통신업": [
        "철도·항공·창고·운수관련서비스업",
        "육상 및 수상운수업",
        "통신업"
    ],

    "임업": ["임업"],
    "어업": ["어업"],
    "농업": ["농업"],

    "금융 및 보험업": ["금융 및 보험업"],

    "기타의 사업": [
        "시설관리및사업지원서비스업",
        "해외파견자",
        "전문·보건·교육·여가관련서비스업",
        "도소매·음식·숙박업",
        "부동산업 및 임대업",
        "국가 및 지방자치단체의 사업",
        "주한미군",
        "기타의 각종사업"
    ]
};

// ⬆ 중분류1 채우기

    const $cat1 = $("#i_industry_type1");

    $.each(industryMap, function (key, value) {
        $cat1.append(`<option value="${key}">${key}</option>`);
    });

    // 중분류1 → 중분류2 연동
    $("#i_industry_type1").on("change", function () {
        const selected = $(this).val();
        const $cat2 = $("#i_industry_type2");

        $cat2.empty().append(`<option value="">중분류2 선택</option>`);

        if (!selected) return;

        $.each(industryMap[selected], function (idx, item) {
            $cat2.append(`<option value="${item}">${item}</option>`);
        });
    });

    $("#applyType").on("click", function () {
        const injury = $("#occurrenceType").val();
        const disease = $("#diseaseType").val();

        // hidden input 에 값 넣기
        $("#i_injury").val(injury);
        $("#i_disease_type").val(disease);

        // 화면 표시
        $("#selectedType").val(`발생형태: ${injury}, 질병: ${disease}`);
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