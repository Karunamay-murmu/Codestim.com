function toggleSideMenu() {
    const burger = document.querySelector('#burger')
    const cross = document.querySelector('#cross')
    const nav = document.querySelector('#navigation-menu')

    burger.onclick = function () {
        nav.classList.add('showSideMenu')
        cross.classList.add('display')
    }

    cross.onclick = function () {
        nav.classList.remove('showSideMenu')
        cross.classList.remove('display')
    }
}

function toggleProfileOptions() {
    const profileIcon = document.getElementById('profileButton')
    if (!profileIcon) return;
    else {
        const optionCard = profileIcon.nextElementSibling;
        let optionCardVisible = false

        function profileOptionCard(e) {
            optionCard.classList.add('display');
            optionCardVisible = true;

            if (optionCardVisible) {
                e.stopImmediatePropagation();
                document.onclick = function () {
                    optionCard.classList.remove('display')
                }
                optionCardVisible = false
            }
        }
        profileIcon.addEventListener("click", profileOptionCard);
    }
}

function activeCategory() {
    const url = window.location.pathname.toLowerCase()
    const navItems = document.querySelectorAll('.nav-bar__menu__item');
    Array.from(navItems).forEach(n => {
        const categoryName = n.innerText.toLowerCase().replace(" ", "-")
        if (url === `/category/${categoryName}`) n.classList.add('active')
    })
}

activeCategory()
toggleSideMenu()
toggleProfileOptions()