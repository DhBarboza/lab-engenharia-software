function deleteObj(id) {
    if (!id) {
        return null
    }

    let ajax = new XMLHttpRequest()
    ajax.open('DELETE', `http://localhost:5000/assuntos/delete/${id}`, true)
    ajax.setRequestHeader('Content-Type', 'application/json')

    ajax.onload = (() => {
        const res = JSON.parse(ajax.responseText)
        console.log(res)
        if (!res.error) {
            document.getElementById(`assunto_${id}`).remove()
        } else {
            alert('Existe uma notícia cadastrada com este assunto')
        }
    })

    ajax.onerror = (error => {
        console.log('ajax error:', error)
    })

    ajax.send(undefined)
}