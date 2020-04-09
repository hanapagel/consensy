
$.get((`/poll/${poll_id}/outcome`), (res) => {

    console.log(res['name'], res['description'])

    $('#outcome_name').append(res['name'])
    $('#outcome_description').append(res['description'])
})

$.get((`/poll/${poll_id}/results_chart`), (res) => {

    const resultsChart = new Chart(

        $('#pie-chart'), {

            type: 'pie',

            data: {

                labels: ['Agree', 'Reservations', 'Stand-aside', 'Block'],
                datasets: [{
                    label: 'Poll results',
                    data: [res['agr'], res['rsv'], res['asd'], res['blk']],
                    backgroundColor: ['green', 'yellow', 'orange', 'red'],
                }]
            }
        }
    )
});