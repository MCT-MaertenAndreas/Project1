class Login {
    constructor() {

    }

    domLookup() {
        this.form = document.getElementById('login_form');

        this.form.addEventListener('submit', () => this._login());
    }

    async _login() {
        const formData = new FormData(this.form);

        let json = {};
        formData.forEach((value, key) => {
            json[key] = value;
        });

        const res = await Data.post('/api/v1/auth/login/', json);

        if (res.ok) {
            const json = await res.json();

            if (json.status === 'success') {
                sessionStorage.setItem('sess_token', json.data.token);

                window.location = '/main.html';

                return;
            }
            alert(json.message);

            return;
        }

        alert(`${res.status} ${res.statusText}`);
    }
}

const login = new Login();

document.addEventListener('DOMContentLoaded', () => login.domLookup());
