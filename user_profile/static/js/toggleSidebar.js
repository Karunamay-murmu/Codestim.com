class Sidebar {
    constructor() {
        this.burger = document.querySelector('#burger')
        this.cross = document.querySelector('#cross')
        this.navigation = document.querySelector('.dashboard__sidebar')
    }

    changeIcon(action) {
        if (action === 'show') {
            this.burger.style.display = 'none'
            this.cross.style.display = 'initial'
        } else {
            this.cross.style.display = 'none'
            this.burger.style.display = 'initial'
        }
    }

    show() {
        let burger = this.burger;
        burger.style.display = 'initial';
        burger.onclick = function () {
            this.navigation.style.transform = 'translateX(0)';
            this.changeIcon('show')
        }.bind(this)
    }

    hide() {
        let cross = this.cross;
        cross.onclick = function () {
            this.navigation.style.transform = 'translateX(-150%)';
            this.changeIcon('hide')
        }.bind(this)
    }
    
    static toggle() {
        const sidebar = new Sidebar()
        document.addEventListener('DOMContentLoaded', () => {
            let query = window.matchMedia('(max-width: 570px)')
            if (query.matches) {
                sidebar.show()
                sidebar.hide()
            }

            query.onchange = function () {
                if (query.matches) {
                    sidebar.navigation.style.transform = 'translateX(-150%)'
                    sidebar.show()
                    sidebar.hide()
                } else {
                    sidebar.navigation.style.transform = 'translateX(0)'
                    sidebar.burger.style.display = 'none'
                    sidebar.cross.style.display = 'none'
                }
            }
        })
    }

}
Sidebar.toggle()