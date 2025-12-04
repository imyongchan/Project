$(document).ready(function () {

    const usernameInput = $("#username");
    const pw1Input = $("#password1");
    const pw2Input = $("#re-password2");

    const usernameCheckMsg = $("#usernameCheckMsg");
    const passwordError = $("#passwordError");
    const rePasswordError = $("#rePasswordError");

    const usernameRegex = /^[a-z0-9]{6,16}$/;
    const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*]).{8,16}$/;

    let isUsernameAvailable = false; // 아이디 중복 확인 상태

    // 아이디 입력 시 중복 확인 상태 초기화
    usernameInput.on("input", function () {
        isUsernameAvailable = false;
        usernameCheckMsg.text("");
    });
    
    // 아이디 중복 확인 버튼 클릭 이벤트
    $("#checkUsernameBtn").on("click", function () {
        const username = usernameInput.val().trim();
        const checkUrl = $(this).data("url"); // data-url 속성에서 URL 가져오기

        if (!usernameRegex.test(username)) {
            usernameCheckMsg.text("아이디 양식을 다시 확인해주세요.").css("color", "red");
            return;
        }

        $.ajax({
            url: checkUrl,
            data: {
                'username': username
            },
            dataType: 'json',
            success: function (data) {
                if (data.is_taken) {
                    usernameCheckMsg.text("이미 사용중인 아이디입니다.").css("color", "red");
                    isUsernameAvailable = false;
                } else {
                    usernameCheckMsg.text("사용 가능한 아이디입니다.").css("color", "green");
                    isUsernameAvailable = true;
                }
            },
            error: function() {
                usernameCheckMsg.text("오류가 발생했습니다. 다시 시도해주세요.").css("color", "red");
                isUsernameAvailable = false;
            }
        });
    });

    // 비밀번호 blur 검증
    pw1Input.on("blur", function () {
        if (!passwordRegex.test(pw1Input.val())) {
            passwordError.show();
        } else {
            passwordError.hide();
        }
    });

    // 비밀번호 확인 blur 검증
    pw2Input.on("blur", function () {
        if (pw1Input.val() !== pw2Input.val()) {
            rePasswordError.show();
        } else {
            rePasswordError.hide();
        }
    });

    // 폼 제출 검증
    $("#registerForm").on("submit", function (e) {
        let valid = true;

        if (!usernameRegex.test(usernameInput.val().trim())) {
            usernameCheckMsg.text("아이디 양식을 다시 확인해주세요.").css("color", "red");
            valid = false;
        } else if (!isUsernameAvailable) {
            usernameCheckMsg.text("아이디 중복 확인을 해주세요.").css("color", "red");
            valid = false;
        }

        if (!passwordRegex.test(pw1Input.val())) {
            passwordError.show();
            valid = false;
        }

        if (pw1Input.val() !== pw2Input.val()) {
            rePasswordError.show();
            valid = false;
        }

        if (!valid) {
            e.preventDefault();
        }
    });
});
