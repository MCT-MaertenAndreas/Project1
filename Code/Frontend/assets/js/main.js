class Main extends Helpers {
    constructor() {
        super();

        this.login = new LoginUtils(this);
        this.func = new Function(this);
    }

    async checkSession() {
        const session_valid = await this.login.isSessionValid()
            .catch((e => console.error(e)));

        if (session_valid) {
            this.openMainMenu();

            return;
        }

        // Reauthentication needed
        this.openLoginPage();
    }

    domLookup() {
        this.body = document.getElementsByTagName('body')[0];
        this.contentWrapper = document.getElementById('content-wrapper');

        this.checkSession();
    }

    mainMenuDomLookup() {
        document.getElementById('logout').addEventListener('click', (e) => this.login.logout());

        this.navbar = document.querySelector('nav');

        this.navPopouts = document.getElementsByClassName('hasPopout');
        this.popouts = document.getElementsByClassName('nav-popout');

        this.fileBody = document.querySelector('.file-viewer > tbody');
        this.storagePopout = document.getElementById('storagePopout');
    }

    async openLoginPage() {
        await this.func.updateContent('/assets/content/login.html');

        this.login.domLookup();
    }

    async openMainMenu() {
        await this.func.updateContent('/assets/content/main.html');

        this.mainMenuDomLookup();

        this.func.popoutListeners();

        this.func.alignPopouts();
    }
}
