var questionNumber = 0;
var questions;


function generateQuestion() {
    if (questions.length == 0) {
        document.getElementById("question").innerText = "Unable to fetch questions.";
    }
    else {
        document.getElementById("question").innerText = questions[questionNumber];
        questionNumber++;
        questionNumber %= questions.length;
    }
}

function doneAnswering() {
    document.getElementById("answer").value = "";
    generateQuestion()
}


document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("button").onclick = doneAnswering;
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
        let tabUrl = tabs[0].url;
        tabUrl = tabUrl.split("?")[0];
        var url = 'https://ungypabgipau5dfpvbxxg6tir40inugb.lambda-url.us-east-1.on.aws/?key=bulldogs&url=' + '"' + tabUrl + '"';
        // Making our request 
        fetch(url, {
            method: 'GET'
        })
            .then(Result => Result.json())
            .then(string => {
                questions = string;
                generateQuestion();
            })
            .catch(errorMsg => { console.log(errorMsg); });

    });
});