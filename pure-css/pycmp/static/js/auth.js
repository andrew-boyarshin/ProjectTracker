function submit_register(login) {
    var auth_form = document.getElementById("auth_form");
    var auth_form_mobile = document.getElementById("auth_form_mobile");
    ac = (login == true)? "/user/login" : "/user/register";
    auth_form.action = ac;
    auth_form_mobile.action = ac;
    is_mobile = (auth_form_mobile.style.display == "block");
    if (is_mobile == true) {
        auth_form_mobile.submit();
    } else {
        auth_form.submit();
    }
}