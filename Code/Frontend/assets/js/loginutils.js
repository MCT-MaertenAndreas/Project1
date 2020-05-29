class LoginUtils {
    constructor(main) {
        this.parent = main;
    }

    async animateOpenFileManager() {
        const duration = 2500;

        this.loginCircle.style.animation = `animateAway ${duration}ms ease forwards`;
        await this.parent.func.promTimeout(duration / 4);
        this.loginCard.remove();
        await this.parent.func.promTimeout(duration - duration / 1.5);

        this.parent.openMainMenu();
    }

    isSessionValid() {
        const token = sessionStorage.getItem('sess_token');

        return new Promise(async (resolve, reject) => {
            const res = await this.parent.get('/api/v1/auth/session/', null, { 'Authorization': token });

            if (res.ok) {
                let server_res = await res.text();
                try {
                    const json = JSON.parse(server_res);
                    server_res = json;
                } catch (e) {
                    console.log(server_res);
                    reject(e.stack)

                    return;
                }

                resolve(server_res.data.status);
            }

            reject(res.statusTxt);
        });
    }

    async loginAttempt(e) {
        e.preventDefault();

        const loginData = Object.fromEntries(new FormData(e.target));
        const res = await this.parent.post('/api/v1/auth/login/', loginData);

        if (res.ok) {
            const server_res = await res.json();
            if (server_res.status == 'success') {
                sessionStorage.setItem('sess_token', server_res.data.token);

                this.parent.func.popNotification(server_res.message, 'success', 3500);

                this.animateOpenFileManager();

                return;
            }

            this.parent.func.popNotification(server_res.message, 'warning', 3500);

            return;
        }

        this.parent.func.popNotification(`${res.status} ${res.statusText}`, 'error', 8000);
    }

    domLookup() {
        this.loginCircle = document.querySelector('.login-circle');
        this.loginForm = document.querySelector('form');
        this.loginCard = document.querySelector('.login-wrapper > .card');

        this.loginForm.addEventListener('submit', (e) => this.loginAttempt(e));
    }

    async logout() {
        const
            token = sessionStorage.getItem('sess_token'),
            res = await this.parent.delete('/api/v1/auth/logout/', { token: token });

        if (res.ok && res.status == 204) {
            sessionStorage.clear();

            this.parent.func.popNotification('You\'ve successfully been logged out!', 'success', 3500);

            this.parent.openLoginPage();

            return;
        }
    }
}
