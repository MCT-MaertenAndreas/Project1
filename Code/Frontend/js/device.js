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

            actuators: document.getElementById('device_states'),

            data: document.getElementById('device_states'),

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

    async getMeasurementsBySensorId(id) {
        const res = await Data.get(`/api/v1/sensors/${id}/measurements/`);

        return res.json();
    }

    getSensorByTaskAndTypeId(task, typeId) {
        for (const sensor of this.sensors) {
            if (sensor.task_name == task && sensor.type == typeId) return sensor;
        }

        return -1;
    }

    async getSensorOnOffState(sensor) {
        const
            result = await this.getMeasurementsBySensorId(sensor.sensor_id),
            state = result[0].value == 0 ? 'Off' : 'On';

        return `<ul>
            <li>${sensor.name}</li>
            <li class="${state.toLowerCase()}">${state}</li>
        </ul>`;
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

    async setContent() {
        this.title.innerHTML = this.device.name;

        let date = new Date(this.device.last_refilled);
        date.setHours(date.getHours() - 2);

        this.last_updated.innerHTML = `Last refilled ${this.prettyDate(date)} ago`;

        if (Date.now() - date.getTime() > 1.21e9) {
            this.notice_container.style = 'display: initial';
            this.notice_list.innerHTML = '';

            this.notice_list.insertAdjacentHTML('beforeend', `<li>The last time this reservoir was filled was ${this.prettyDate(date)} ago, it's adviced to refill the reservoir every 2 weeks!</li>`)
        }

        this.water_reserve.innerHTML = `${this.device.reservoir_size} ml`;

        const
            water_pump = this.getSensorByTaskAndTypeId('pump', 8),
            buzzer = this.getSensorByTaskAndTypeId('alarm', 10),

            water_pump_state = await this.getSensorOnOffState(water_pump),
            buzzer_state = await this.getSensorOnOffState(buzzer);

        this.actuators.insertAdjacentHTML('beforeend', water_pump_state);
        this.actuators.insertAdjacentHTML('beforeend', buzzer_state);
    }
}
