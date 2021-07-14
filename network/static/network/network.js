document.addEventListener('DOMContentLoaded', function() {
    edit_links = document.getElementsByClassName('edit_link');
    for(let edit_link of edit_links){
        edit_link.addEventListener('click', () => edit_post(edit_link));
    };
});

function edit_post(edit_link) {
    id = edit_link.id.slice(5);
    document.querySelector(`#textarea_${id}`).style.display = 'block';
    document.querySelector(`#textarea_${id}`).focus();
    document.querySelector(`#post_${id}`).style.display = 'none';
    document.querySelector(`#form_${id}`).onsubmit = function() {
        new_content = document.querySelector(`#content_${id}`).value;
        fetch(`/edit_post/${id}`, {
            credentials: 'same-origin',
            method: 'PUT',
            body: JSON.stringify({
                content: new_content,
            })
        });
        document.querySelector(`#textarea_${id}`).style.display = 'none';
        document.querySelector(`#card-text_${id}`).innerHTML = new_content;
        document.querySelector(`#post_${id}`).style.display = 'block';
        return false;
    };
}
