const savedAssuntos = [];

function create() {
    if (!savedAssuntos.length) {
        return null
    }

    let count = savedAssuntos.length

    savedAssuntos.forEach((obj, index) => {
        let ajax = new XMLHttpRequest()
        ajax.open('POST', 'http://localhost:5000/assuntos/create', true)
        ajax.setRequestHeader('Content-Type', 'application/json')

        ajax.onload = (() => {
            count--
            const res = JSON.parse(ajax.responseText)
            if (count == 1) {
                if (!res.error) {
                    window.location.href = '/assuntos/'
                }
            } else {
                if (res.error) {
                    alert('Erro de cadastro')
                }
            }
        })

        ajax.onerror = (error => {
            console.log('ajax error:', error)
        })

        ajax.send(JSON.stringify(obj))
    })
}

function addAssunto() {
    document.getElementById('submit-assuntos').disabled = false;
    const assunto = document.getElementById('assunto-name')
    savedAssuntos.push({name: assunto.value})
    assunto.value = ''
    const listAssuntos = document.getElementById('listAssuntos')
    listAssuntos.innerText = savedAssuntos.map(i => i.name).join(', ')
}
