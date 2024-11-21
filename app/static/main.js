document.addEventListener("DOMContentLoaded", () => {
    const startButton = document.getElementById("startGame");
    let cards = 3
    let rounds = 3
    let seconds = 60
    setPlayMode("easy")
    cardsSlider();
    roundsSlider();
    secondsSlider();

    document.getElementById("cards_slider").oninput = function() {
        cardsSlider()
        setPlayMode("custom")
    };
    function cardsSlider() {
       cards = document.getElementById("cards_slider").value //gets the oninput value
       document.getElementById('no_of_cards').innerHTML = cards //displays this value to the html page
    }

   
    document.getElementById("rounds_slider").oninput = function() {
        roundsSlider()
        setPlayMode("custom")
    }; 
    function roundsSlider() {
        rounds = document.getElementById("rounds_slider").value //gets the oninput value
        document.getElementById('no_of_rounds').innerHTML = rounds //displays this value to the html page
    }

    document.getElementById("seconds_slider").oninput = function() {
        secondsSlider()
        setPlayMode("custom")
    };
    function secondsSlider() {
    seconds = document.getElementById("seconds_slider").value //gets the oninput value
    document.getElementById('no_of_seconds').innerHTML = seconds //displays this value to the html page
    }

    function setPlayMode(level){
        if (level == "easy"){
            cards = 3;
            rounds = 3;
            seconds = 60;

            document.getElementById("cards_slider").value = 3;
            document.getElementById("rounds_slider").value = 3;
            document.getElementById("seconds_slider").value = 60; 

            cardsSlider();
            roundsSlider();
            secondsSlider();
        }
        else if (level == "medium"){
            cards = 4;
            rounds = 5;
            seconds = 50;

            document.getElementById("cards_slider").value = 4
            document.getElementById("rounds_slider").value = 5
            document.getElementById("seconds_slider").value = 50

            cardsSlider();
            roundsSlider();
            secondsSlider();
        }
        else if (level == "hard"){
            cards = 5;
            rounds = 5;
            seconds = 40;

            document.getElementById("cards_slider").value = 5
            document.getElementById("rounds_slider").value = 5
            document.getElementById("seconds_slider").value = 40

            cardsSlider();
            roundsSlider();
            secondsSlider();
        }
        else if (level == "custom"){
        }
    }


    // Start Game and Redirect to Round Page
    startButton.addEventListener("click", () => {
        window.location.href = "/round";
        return jsonify({
            
        })
    })

    document.getElementById("easyButton").addEventListener("click", () => setPlayMode("easy"))
    document.getElementById("mediumButton").addEventListener("click", () => setPlayMode("medium"))
    document.getElementById("hardButton").addEventListener("click", () => setPlayMode("hard"))

    // document.getElementById("cards_slider").addEventListener("click", () => setPlayMode("custom"))
    // document.getElementById("rounds_slider").addEventListener("click", () => setPlayMode("custom"))
    // document.getElementById("seconds_slider").addEventListener("click", () => setPlayMode("custom"))
});