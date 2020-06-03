class Routing extends Helpers {
    constructor() {
        super();
    }

    async changeRoute(path = null) {
        if (path != null) {
            history.replaceState(null, '', `/#${path}`);

            if (path.includes('?'))
                path = this.getHash('#' + path);
        }
        else {
            path = this.getHash();
        }

        sessionStorage.setItem('last', path);

        if (path == '') {
            path = '/home';
        }

        const filePath = `/assets/content${path}.html`;

        const res = await this.get(filePath);
        this.app_content.innerHTML = await res.text();

        this.app_content.scrollTo(0,0, 'smooth');

        this.initClassForPath(path);
    }

    getHash(path = null) {
        const url = path ? path.split('?') : window.location.hash.split('?');

        this.route = url[0].substr(1);

        this.query = url[1];

        return this.route;
    }

    getQuery(key) {
        const search = this.query;
        if (!search) return null;

        const vars = search.split('&');

        for (let i = 0; i < vars.length; i++) {
            const pair = vars[i].split('=');
            if (decodeURIComponent(pair[0]) == key) {
                return decodeURI(pair[1]);
            }
        }

        return null;
    }

    initClassForPath(path) {
        switch (path) {
            case '/devices': {

                break;
            }
            case '/device':

                break;
            default: {

            }
        }
    }

    routingLookup() {
        this.routes = document.querySelectorAll('.routing a:not(.ignore)');

        this.routes.forEach((element) => element.addEventListener('click', (e) => this.routeUpdate(e)));

        this.changeRoute();
    }

    routeUpdate(e) {
        e.preventDefault();

        if (e.currentTarget.dataset.title) {
            window.title = e.currentTarget.dataset.title;
        }

        this.changeRoute(e.currentTarget.hash.substr(1));
    }

    setHistory(path) {
        history.replaceState(null, '', path);
    }
}
