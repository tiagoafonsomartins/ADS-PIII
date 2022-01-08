function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

var percent = 0;

async function say_cenas() {
    console.log("Inside say_cenas()")
    for (let i = 0; i < 10; i++) {
        check_progess();
        update_progress();
        await sleep(700);
    }
}

$('.content').on('submit', function () {
    console.log("Button clicked");
    say_cenas();
    return true;
});

function check_progess() {
    $.ajax({
        type: "GET",
        url: "progress_bar",
        success: function(result) {
             if(result.error == 0) {
                percent = result.percent;
             }
        },
        error: function(result) {
            console.log('error');
        }
    });
}

function update_progress() {
    console.log("Progress at " + percent + "%");
}