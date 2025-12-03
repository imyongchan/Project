function searchAddress(targetId) {
    new daum.Postcode({
        oncomplete: function(data) {
            document.getElementById(targetId).value = data.address;
        }
    }).open();
}