document.addEventListener("DOMContentLoaded", function () {

    // 자료유형 전체 클릭
    window.toggleAllTypes = function (allBox) {
        const boxes = document.querySelectorAll('input[name="type"]');

        if (allBox.checked) {
            boxes.forEach(b => {
                if (b !== allBox) b.checked = false;
            });
        }
    }

    // 개별 유형 클릭 시 전체 해제 + 전부 해제되면 전체 자동 선택
    window.clickTypeOption = function (box) {
        const allBox = document.querySelector('input[name="type"][value="전체"]');

        if (box.checked) {
            allBox.checked = false;
        }

        const anyChecked = [...document.querySelectorAll('input[name="type"]')]
                            .some(b => b.value !== "전체" && b.checked);

        if (!anyChecked) allBox.checked = true;
    }

    // 언어 선택 (checkbox UI + radio 동작)
    window.selectLang = function (clickedBox) {
        const boxes = document.querySelectorAll('input[name="lang"]');

        boxes.forEach(b => {
            if (b !== clickedBox) b.checked = false;
        });

        // 1개도 선택되지 않으면 전체 다시 체크
        const any = [...boxes].some(b => b.checked);
        if (!any) {
            boxes[0].checked = true;
        }
    }

});
