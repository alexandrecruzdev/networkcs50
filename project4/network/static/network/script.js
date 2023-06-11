
const save = (id) =>{
    let card_body = document.getElementById(id)
    console.log(card_body.children[3].value)
    fetch()

}

const handlerOnclickEdit = (id) => {
    let card_body = document.getElementById(id)
    card_body.children[2].style.display = 'none'
    value = card_body.children[2].innerText
    card_body.children[3].style.display = 'block'
    card_body.children[3].value = value.trim()
    card_body.children[5].style.display = 'block'
}
