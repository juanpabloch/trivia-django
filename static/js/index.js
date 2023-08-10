const loadingView = document.querySelector('#loading')
const play = document.querySelector('#play')
const main = document.querySelector('#main') 


if(play){
    play.addEventListener('click', (e)=>{
        // e.preventDefault()
        main.classList.add('hide')
        loadingView.classList.remove('hide')
    })
}
