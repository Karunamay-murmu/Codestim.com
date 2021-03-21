const deleteBtn = document.querySelectorAll('.delete')
const modalContainer = document.getElementById('modal-container')
const closeBtn = document.querySelectorAll('.close')

deleteBtn.forEach(function (btn) {
    btn.onclick = function (e) {
        modalContainer.classList.add('show')

        const postId = e.target.value
        const spanPostTitle = e.target.dataset.extra
        const confirmDeleteBtn = document.getElementById('confirm-delete')

        const span = document.getElementById('spanPostTitle')
        span.textContent = spanPostTitle
        confirmDeleteBtn.value = postId
    }
})

closeBtn.forEach(function (btn) {
    btn.onclick = function (e) {
        modalContainer.classList.remove('show')
    }

})