function pageLoader() {
    const loader = document.querySelector("#loader-container")
    const bodyContent = document.querySelector('#body-content');
    window.onload = function () {
        bodyContent.removeAttribute('style');
        loader.classList.add('removeloader');
        setTimeout(() => {
            loader.remove();
        }, 700);
    }
}

pageLoader();