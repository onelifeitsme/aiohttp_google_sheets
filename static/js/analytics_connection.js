let analytics_connection = function () {
    $.ajax({
        url: '/dashboard/analytics/new-connection/',
        type: 'POST',
        data: key = '123',
        success: function (response) {
        },
        error: function (response) {
            alert('ошбка получения id транзакции.');
        }
    });
}