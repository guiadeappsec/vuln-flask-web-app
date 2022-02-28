const urlParams = new Proxy(new URLSearchParams(window.location.search), {
    get: (searchParams, prop) => searchParams.get(prop),
});


function showError(err) {
    console.error(err)
    alert(err)
}

function redirectToHome() {
    window.location.href = '/'
}


function resetDatabase() {
    document.getElementById('btnResetDatabase').classList.toggle('is-loading')

    setTimeout(() => {
        axios.post('/reset-database')
            .then(() => {
                alert('Database Reseted!')
                redirectToHome()
            })
            .catch(err => {
                showError(err)
            })
    }, 1000);

    
}