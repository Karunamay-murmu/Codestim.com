function incrementLikeOnPost() {
    const likeButton = document.querySelector('#likeButton');
    const postid = postId;

    const incrementLikeAndChangeColor = likes => {
        const likesOnPost = document.querySelector('#postLikeCount');
        const likeButtonSVG = document.querySelector('#likeButtonSVG')

        likesOnPost.textContent = likes;
        likeButtonSVG.classList.add('liked')
    }

    function like(e) {
        const csrftoken = likeButton.previousElementSibling.getAttribute('value')
        const data = {
            postid
        }
        try {
            fetch(url, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify(data)
            }).then(data => data.json())
                .then(response => {
                    const likes = response.likes
                    incrementLikeAndChangeColor(likes)
                }).catch((error) => {
                    console.error(error)
                });
        } catch (error) {
            console.error(error)
        }
    }

    likeButton.addEventListener("click", like, { once: true })
}

function lazyload() {
    const images = Array.from(document.querySelectorAll('img'));
    console.log(images);

    const load = function (img) {
        const src = img.getAttribute("data-src");
        if (!src) {
            return;
        }
        img.src = src;
        img.classList.add('lazyload');
        img.removeAttribute('style');
    }
    const imageObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) {
                return;
            } else {
                load(entry.target);
                imageObserver.unobserve(entry.target)
            }
        })
    })
    images.forEach(image => {
        imageObserver.observe(image);
        const server = image.dataset.server
        if (server) {
            image.style.opacity = 0;
        }
    })
}

incrementLikeOnPost();
lazyload();