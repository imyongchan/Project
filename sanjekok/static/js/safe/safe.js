function toggleAllTypes(allCheckbox) {
    // 전체 클릭 시 → 나머지 체크 모두 해제
    const checkboxes = document.querySelectorAll('input[name="type"]');
    checkboxes.forEach(box => {
        if (box !== allCheckbox) box.checked = false;
    });
}

function uncheckAll(checkBox) {
    // 나머지 유형 클릭 시 → 전체 체크 해제
    const allBox = document.querySelector('input[name="type"][value="전체"]');
    if (allBox) allBox.checked = false;
}

