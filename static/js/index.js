const loadingView = document.querySelector('#loading')
const play = document.querySelector('#play')
const main = document.querySelector('#main') 

play.addEventListener('click', (e)=>{
    // e.preventDefault()
    main.classList.add('hide')
    loadingView.classList.remove('hide')
})