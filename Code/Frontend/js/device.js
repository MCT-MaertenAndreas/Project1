class Device {
    constructor() {
        this.id = new URL(window.location.href).searchParams.get('id');

        this.getDeviceData();
    }

    static async get(id) {
        const res = await Data.get(`/api/v1/devices/${id}/`);

        return res.json();
    }

    static async get_all() {
        const res = await Data.get('/api/v1/devices/');

        return res.json();
    }

    static async get_sensors(id) {
        const res = await Data.get(`/api/v1/devices/${id}/sensors/`);

        return res.json();
    }

    domLookup() {
        Object.assign(this, {
            title: document.querySelector('.fountain-container > .heading > h3'),
            last_updated: document.querySelector('.fountain-container .last-updated'),

            notice_container: document.querySelector('.notices'),
            notice_list: document.querySelector('.notices > ul'),

            actuators: document.getElementsByClassName('actuators')[0],

            data: document.getElementsByClassName('actuators')[1],

            water_reserve: document.getElementById('water_reserve')
        });

        if (this.ready) {
            this.setContent();
        }
        this.ready = true;
    }

    async getDeviceData() {
        this.device = await Device.get(this.id);
        this.sensors = await Device.get_sensors(this.id);

        if (this.ready) {
            this.setContent();
        }
        this.ready = true;
    }

    prettyDate(date) {
        const seconds = Math.floor((new Date() - date) / 1000);
        let interval = Math.floor(seconds / 31536e3);

        if (interval > 1) {
            return interval + " years";
        }
        interval = Math.floor(seconds / 2592e3);

        if (interval > 1) {
            return interval + " months";
        }

        interval = Math.floor(seconds / 86400);
        if (interval > 1) {
            return interval + " days";
        }

        interval = Math.floor(seconds / 3600);
        if (interval > 1) {
            return interval + " hours";
        }

        interval = Math.floor(seconds / 60);
        if (interval > 1) {
            return interval + " minutes";
        }
        return Math.floor(seconds) + " seconds";
    }

    setContent() {
        this.title.innerHTML = `Last refilled ${this.device.name}`;

        let date = new Date(this.device.last_refilled);
        date.setHours(date.getHours() - 2);

        this.last_updated.innerHTML = this.prettyDate(date);

        if (Date.now() - date.getTime() > 1.21e9) {
            this.notice_container.style = 'display: initial';
            this.notice_list.innerHTML = '';

            this.notice_list.insertAdjacentHTML('beforeend', `<li>The last time this reservoir was filled was ${this.prettyDate(date)} ago, it's adviced to refill the reservoir every 2 weeks!</li>`)
        }

        this.water_reserve.innerHTML = `${this.device.reservoir_size} ml`;
    }
}
