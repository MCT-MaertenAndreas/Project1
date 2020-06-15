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

    async getMeasurementsBySensorId(id, average = false) {
        let res;

        if (average)
            res = await Data.get(`/api/v1/sensors/${id}/measurements/`);
        else
            res = await Data.get(`/api/v1/sensors/${id}/measurements/last/`);

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
            <li>${sensor.hint_name}</li>
            <li class="${state.toLowerCase()}">${state}</li>
        </ul>`;
    }

    async getSensorGraphData(sensor) {
        const
            date = (new Date()).getDate(),
            results = await this.getMeasurementsBySensorId(sensor.sensor_id, true);

        results.reverse();

        let
            data = [],

            day = date - 6,
            hour = 0;

        for (let x = 0; x < results.length; x++) {
            const measurement = results[x];

            if (x == 0 && measurement.day != 1 && measurement.hour != 0) {
                data.push(0);

                continue;
            }

            const nullData = (() => {
                let weight = 0;

                if (day < measurement.day) {
                    if (hour < measurement.hour) {
                        weight += (measurement.day - day) * 24;
                        weight += (measurement.hour - hour);
                    }
                    else {
                        weight += (measurement.day - day - 1) * 24;
                        weight += (24 - measurement.hour + hour);
                    }
                }
                else {

                }

                return weight;
            })();

            for (let i = 0; i < nullData - 1; i++) data.push(null);

            data.push(measurement.average);

            day = measurement.day;
            hour = measurement.hour;
        }

        return data;
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
        this.drawGraph();

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

    generateLabels() {
        const
            days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            date = (new Date()).getDay();

        let labels = [];
        labels.length = 7 * 24;
        labels.fill('');

        for (let i = days.length; i > 0; i--) {
            const position = 24 * i - 12;
            if (i == 7) {
                labels[position] = 'Today';

                continue;
            }
            if (i == 6) {
                labels[position] = 'Yesterday';

                continue;
            }

            let difference = date - i;
            if (difference < 0) {
                difference += 6;
            }

            const day = days[7 - difference];
            labels[position] = day;
        }

        for (let i = 7 * 24 - 1; i > 0; i -= 24) {
            if ((i) % 24 == 0) {
                if (date - 1 == i / 24) {
                    labels.push('Yesterday');

                    continue;
                }
                if (date == i / 24) {
                    labels.push('Today');

                    continue;
                }

                const difference = date - i / 24;

                const day = days[date - difference];

                labels.push(day);

                continue;
            }
        }

        return labels;
    }

    async drawGraph() {
        const data = {
            // A labels array that can contain any sort of values
            labels: this.generateLabels(),
            // Our series array that contains series objects or in this case series data arrays
            series: [
                {
                    name: 'Distance Sensor (cm)',
                    data: await this.getSensorGraphData(this.getSensorByTaskAndTypeId('movement_detection', 5))
                },
                {
                    name: 'Light Level',
                    data: await this.getSensorGraphData(this.getSensorByTaskAndTypeId('case_open', 9))
                }
            ],
        };

        // Create a new line chart object where as first parameter we pass in a selector
        // that is resolving to our chart container element. The Second parameter
        // is the actual data object.
        new Chartist.Line(".ct-chart", data, {
            height: 200,

            plugins: [
                Chartist.plugins.legend()
            ]
        });
    }
}
