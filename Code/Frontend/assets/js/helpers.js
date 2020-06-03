class Helpers {
    constructor() {

    }

    /**
     * @param {String} url A valid url
     * @param {Object} data Json object to POST
     * @param {Object} headers Custom object of headers
     */
    async delete(url, data = {}, headers = { 'Content-Type': 'application/json' }) {
        const response = await fetch(url, {
            method: 'DELETE',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers: headers,
            redirect: 'follow',
            body: JSON.stringify(data)
        }).catch(e => { throw e.stack });

        return response;
    }

    /**
     * @param {String} url A valid url
     * @param {Object} params Object of GET params
     * @param {Object} headers Custom object of headers
     */
    async get(url, params = null, headers = { 'Content-Type': 'application/json' }) {
        let request = null;
        try {
            request = new URL(url);
        } catch (e) {
            request = new URL(`${window.location.origin}${url}`)
        }

        const settings = {
                method: 'GET',
                mode: 'cors',
                cache: 'no-cache',
                credentials: 'same-origin',
                headers: headers,
                redirect: 'follow'
            };

        if (params != null) {
            request.search = new URLSearchParams(params);
        }

        return await fetch(request, settings).catch(e => { throw e });
    }

    /**
     * @param {String} url A valid url
     * @param {Object} data Json object to POST
     * @param {Object} headers Custom object of headers
     */
    async post(url, data = {}, headers = { 'Content-Type': 'application/json' }) {
        const response = await fetch(url, {
            method: 'POST',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers: headers,
            redirect: 'follow',
            body: JSON.stringify(data)
        }).catch(e => { throw e.stack });

        return response;
    }
}
