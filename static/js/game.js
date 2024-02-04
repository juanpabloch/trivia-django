window.addEventListener('load', function(e){
    const question = document.querySelector(".card-container")
    const bet = document.querySelector(".bet-container")
    const submitBtn = document.querySelector('input[type="submit"]')
    const betOptions = bet.querySelectorAll('input[type="radio"]')
    const backBtn = document.querySelector('#backBtn')
    const form = document.querySelector('form')

    const containerResult = this.document.querySelector('.container-result')
    const correctCard = this.document.querySelector('.correct')
    const incorrectCard = this.document.querySelector('.incorrect')

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


    submitBtn.addEventListener('click', (e)=>{
        clearTimeout(timerId);
        e.preventDefault()
        
        const answer = this.document.querySelector('input[name="answer"]:checked').value;
        const time = document.querySelector('.countdown-box h1').textContent;
        const currentTime = this.document.querySelector('input[name="current_time"]');
        currentTime.value = time
        const bet = document.querySelector('input[name="bet"]:checked').value;
        const token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const points_card = this.document.querySelectorAll('.points span')
        var formData = new FormData();
        formData.append("answer", answer)
        formData.append("time", time)
        formData.append("bet", bet)
        // crear codigo para cuando se 
        $.ajax({
            type:"POST",
            url:"/questions_form/",
            processData: false,
            contentType: false,
            headers:{'X-CSRFToken': token},
            data: formData,
            complete: function(data){
                if(typeof(data.status) != 'undefined'){
                    if(data.status == 200){
                        points_card.forEach(item=>{
                            item.textContent = data.responseJSON.points
                        })
                        containerResult.classList.remove('hide')
                        if(data.responseJSON.result === 'correct'){
                            correctCard.classList.remove('hide')
                        }else{
                            incorrectCard.classList.remove('hide')
                            incorrectCard.querySelector('.correct_a').textContent = data.responseJSON.correct_a
                        }

                        setTimeout(function () {
                            form.submit()
                        }, 3000)
                    } else {
                        console.log("Error");
                        window.location.replace(url_home);
                    }
                } else {
                    console.log("response.status is undefined");
                }
            }
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