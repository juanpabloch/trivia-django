window.addEventListener('load', function(e){

    const question = document.querySelector(".card-container")
    const bet = document.querySelector(".bet-container")
    const submitBtn = document.querySelector('input[type="submit"]')
    const betOptions = bet.querySelectorAll('input[type="radio"]')
    const backBtn = document.querySelector('#backBtn')
    const loadingSection = document.querySelector('#loading')

    betOptions.forEach(option=>{
        option.addEventListener('change', (e)=>{
            question.classList.remove('hide')
            submitBtn.classList.remove('hide')
            bet.classList.add('hide')
            document.querySelector('#backBtn').addEventListener('click', e=>{
                e.preventDefault()
            })
            backBtn.classList.add('hide')
        })
    })

    // TIMER
    const countDown = document.querySelector('.countdown-box h1')
    var timeLeft = 30;
    
    var timerId = setInterval(countdown, 1000);
    
    function countdown() {
      if (timeLeft < 0) {
        clearTimeout(timerId);
        wrongAnswer()
      } else {
        countDown.innerHTML = timeLeft;
        timeLeft--;
      }
    }

    submitBtn.addEventListener('click', (e)=>{
        submitBtn.setAttribute('disabled', '')
        clearInterval(timerId)
        loadingSection.classList.remove('hide')
        document.querySelector('#result').textContent = document.querySelector('input[name="answer"]:checked').value == crtan ? 'CORRECTO' : 'INCORRECTO'
    })

    function wrongAnswer() {
        let bet = ''
        try {
            bet = document.querySelector('input[name="bet"]:checked').value;
        } catch (error) {
            bet = document.querySelector('input[name="bet"]').value;
        }
        const token = document.querySelector('input[name="csrfmiddlewaretoken"]').value
        var formData = new FormData();
        formData.append("bet", bet)
        console.log("TIME OUT!")
        // crear codigo para cuando se 
        $.ajax({
            type:"POST",
            url:"/wrong/",
            processData: false,
            contentType: false,
            headers:{'X-CSRFToken': token},
            data: formData,
            complete: function(data){
                if(typeof(data.status) != 'undefined'){
                    if(data.status == 200){
                        console.log("No se contesto la pregunta")
                        window.location.replace(url_home);
                    } else {
                        console.log("Error");
                    }
                } else {
                    console.log("response.status is undefined");
                }
            }
        })
    }
})