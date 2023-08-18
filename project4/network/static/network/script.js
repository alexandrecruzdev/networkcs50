function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }
  

const save = (id) =>{
    let card_body = document.getElementById(id)
    let new_value = card_body.children[3].value
    let content = card_body.children[2]
    content.innerText = new_value
    card_body.children[2].style.display = 'block'
    card_body.children[3].style.display = 'none'

    const url = `/editPost/${id}/${new_value}`;

    const csrftoken = getCookie('csrftoken');

    const requestOptions = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // ou 'application/x-www-form-urlencoded', dependendo do que sua view espera
        'X-CSRFToken': csrftoken,  // Inclui o token CSRF no cabeçalho
    },
      body: JSON.stringify({ id, new_value: new_value})  // Transforma os dados em JSON
    };
    
    // Realiza a requisição
    fetch(url, requestOptions)
      .then(response => response.text())  // Extrai o conteúdo de texto da resposta
      .then(data => {
        console.log(data);  // Aqui você pode lidar com a resposta da view
      })
      .catch(error => {
        console.error('Erro:', error);
      });




  

}

const handlerOnclickEdit = (id) => {
    let card_body = document.getElementById(id)
    card_body.children[2].style.display = 'none'
    value = card_body.children[2].innerText
    card_body.children[3].style.display = 'block'
    card_body.children[3].value = value.trim()
    card_body.children[5].style.display = 'block'
}
