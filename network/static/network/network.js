document.addEventListener('DOMContentLoaded', function() {
    edit_links = document.getElementsByClassName('edit_link');
    for(let edit_link of edit_links){
        edit_link.addEventListener('click', () => edit_post(edit_link));
    };
    like_links = document.getElementsByClassName('like_link');
    for(let like_link of like_links){
        like_link.addEventListener('click', () => like_post(like_link));
    };
});


function edit_post(link) {
    const id = link.id.slice(5);
    document.querySelector(`#textarea_${id}`).style.display = 'block';
    document.querySelector(`#textarea_${id}`).focus();
    document.querySelector(`#post_${id}`).style.display = 'none';
    document.querySelector(`#form_${id}`).onsubmit = function() {
        new_content = document.querySelector(`#content_${id}`).value;
        fetch(`/edit_post/${id}`, {
            credentials: 'same-origin',
            method: 'PUT',
            body: JSON.stringify({
                route: 'edit',
                content: new_content,
            })
        });
        document.querySelector(`#textarea_${id}`).style.display = 'none';
        document.querySelector(`#card-text_${id}`).innerHTML = new_content;
        document.querySelector(`#post_${id}`).style.display = 'block';
        return false;
    };
};


function like_post(link, route) {
    const id = link.id.slice(5);
    fetch(`/edit_post/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            route: 'like',
        })
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector(`#likes_count_${id}`).innerHTML = data.likes_count;
    });
    if (document.querySelector(`.liked_${id}`).innerHTML === 'favorite') {
        document.querySelector(`.liked_${id}`).innerHTML = 'favorite_border';
    } else {
        document.querySelector(`.liked_${id}`).innerHTML = 'favorite';
    }

}
