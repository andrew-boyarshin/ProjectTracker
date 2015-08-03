var range_slider_quiz;
var text_quiz;
var range_slider_contest;
var text_contest;
var form_quiz;
var form_contest;
function slider_quiz(value) {
    text_quiz.innerHTML = value;
}
function slider_contest(value) {
    text_contest.innerHTML = value;
}
function submit_cmp_quiz() {
	form_quiz.submit();
}
function submit_cmp_contest() {
	form_contest.submit();
}
docReady(function() {
    range_slider_quiz = document.getElementById("range-slider_quiz");
    text_quiz = document.getElementById("range-content_quiz");
    range_slider_contest = document.getElementById("range-slider_contest");
    text_contest = document.getElementById("range-content_contest");
    form_quiz = document.getElementById("save_form_quiz");
    form_contest = document.getElementById("save_form_contest");
    slider_quiz(range_slider_quiz.value);
    slider_contest(range_slider_contest.value);
});