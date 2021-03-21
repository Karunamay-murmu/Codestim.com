class Auth {
    constructor() {
        this.show = document.querySelector('#show-password');
        this.password = document.querySelector('#id_password1');
        this.inputs = document.querySelectorAll('.input');
        this.errors = document.querySelectorAll('.errors')
    }
    showPassword() {
        try {
            const password = this.password;
            this.show.onclick = () => {
                password.type === 'password'
                    ? password.type = 'text'
                    : password.type = 'password'

            }
        } catch (error) {
        }
    }


    /**
     * change color in form in normal state
     */
    addInputStyle() {
        try {
            this.inputs.forEach(input => {
                function changeColor() {
                    const border = input.nextElementSibling;
                    const label = input.parentElement.previousElementSibling;
                    const icon = input.nextElementSibling.nextElementSibling;

                    border.style.transform = 'translateX(0)';
                    label.style.color = '#25A98C';
                    icon.style.fill = '#25A98C';
                }

                input.onfocus = changeColor;
                if (input.value !== '') changeColor()
            })
        } catch (error) {
        }

        /**
         * change colors in form if any error occurred
         * */
        try {
            this.errors.forEach(error => {
                if (error.innerText) {
                    this.changeInputStyleOnError(error)
                }
            })
        } catch (error) {
            console.error(error);
        }
    }

    changeInputStyleOnError(error) {
        try {
            const border = error.previousElementSibling.children[1];
            const icon = error.previousElementSibling.children[2];
            const label = error.parentElement.children[0];

            border.style.transform = 'translateX(0)';
            border.style.backgroundColor = '#d11a2a';
            label.style.color = '#d11a2a';
            icon.style.fill = '#d11a2a';

        } catch (error) {
            console.error(error);
        }
    }
}
const form = new Auth()
form.showPassword()
form.addInputStyle()
form.changeInputStyleOnError()
