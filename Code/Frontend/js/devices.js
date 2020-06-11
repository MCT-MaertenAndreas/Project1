class Devices {
    constructor() {

    }

    domLookup() {
        this.fountain_wrapper = document.querySelector('.cards > ul');

        this.loadFountains();
    }

    prettyDate(date) {
        date.setHours(date.getHours() - 2);

        const seconds = Math.floor((new Date() - date) / 1000);
        let interval = Math.floor(seconds / 31536000);

        if (interval > 1) {
            return interval + " years";
        }
        interval = Math.floor(seconds / 2592000);

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

    async loadFountains() {
        const devices = await Device.get_all();

        this.fountain_wrapper.innerHTML = '';

        for (const device of devices) {
            const html =
            `<li>
                <a href="/fountain.html?id=${device.device_id}">
                    <div class="heading"><h2>${device.name}</h2></div>
                    <div class="last-refilled">
                        <div class="title">Last Refilled</div>
                        <div class="time-ago">${this.prettyDate(new Date(device.last_refilled))} ago</div>
                    </div>
                </a>
            </li>`;

            this.fountain_wrapper.insertAdjacentHTML('beforeend', html);
        }
    }
}

const devices = new Devices();

document.addEventListener('DOMContentLoaded', () => devices.domLookup());
