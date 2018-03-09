
// $(document).ready(function() {

var time = [10, 25, 20, 15, 60,25, 20, 15, 60,25, 20, 15, 60,25, 20, 15, 60,25, 20, 15, 60,25, 20, 15 ];
var activity = ['Ready', 'Easy', 'Medium', 'Hard', 'Rest', 'Medium', 'Hard', 'Easy', 'Rest', 'Hard', 'Easy', 'Medium', 'Rest',
                'Easy', 'Medium', 'Hard', 'Rest', 'Medium', 'Hard', 'Easy', 'Rest', 'Hard', 'Easy', 'Medium'];

var routine = [['Ready', 3], ['Easy',25],['Medium',20], ['Hard',15]]



function timerEvent(time, activity, initial = true){
    var timer = new Timer();
    var currentTime = time.shift()
    var currentActivity = activity.shift()
    var utterance = new SpeechSynthesisUtterance(currentActivity);

    $(timer.start({countdown: true, startValues: {seconds: currentTime}
    }));


    // if (initial == true){
    //   timer.pause();
    // };


    window.speechSynthesis.speak(utterance);

    $('#timer .current').html(currentActivity + ' ' + currentTime.toString()+' ' + 'seconds');
    $('#timer .next').html(activity[0] + ' ' + time[0].toString() + ' ' + 'seconds');


    $('#timer .startButton').click(function () {
        timer.start();
    });

    $('#timer .pauseButton').click(function () {
        timer.pause();
    });

    timer.addEventListener('secondsUpdated', function (e) {
        $('#timer .values').html(timer.getTimeValues().toString());
    });

    timer.addEventListener('targetAchieved', function (e) {
        console.log(time.length)
        if(time.length > 0){
        timerEvent(time, activity, false);

        }
    });


};


// });
// function timerEvent2(routine, counter=0, initial = true){
//   var timer = new Timer();
//   var currentTime = routine[0][1]
//   var currentActivity = routine[0][0]
//   var utterance = new SpeechSynthesisUtterance(currentActivity);
//
//   timer.start({countdown: true, startValues: {seconds: currentTime}
//   });
//   if (initial == true){
//     timer.pause();
//   };
//   window.speechSynthesis.speak(utterance);
//
//   $('#timer .current').html(currentActivity + ' ' + currentTime.toString()+' ' + 'seconds');
//   $('#timer .next').html( currentActivity+ ' ' + currentTime.toString() + ' ' + 'seconds');
//
//   $('#timer .startButton').click(function () {
//       timer.start();
//   });
//
//   $('#timer .pauseButton').click(function () {
//       timer.pause();
//   });
//
//   timer.addEventListener('secondsUpdated', function (e) {
//       $('#timer .values').html(timer.getTimeValues().toString());
//   });
//
//   timer.addEventListener('targetAchieved', function (e) {
//       if(routine.length > 0){
//       timerEvent(routine, false);
//
//       }
//   });
//
// };
//
// // });
