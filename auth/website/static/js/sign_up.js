function getTodayStr() {
    today.getMonth() + '/' + today.getDay() + '/' + today.getFullYear()
}

$(function () {
    let today = new Date();
    bulmaCalendar.attach('[type="date"]', {
        overlay: false,
        maxDate: today.getMonth() + '/' + today.getDay() + '/' + today.getFullYear()
    });
});