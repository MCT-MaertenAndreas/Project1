class Main {
    constructor() {

    }

    domLookup() {
        this.fountain_wrapper = document.querySelector('.cards > ul');

        this.loadFountains();
    }

    async loadFountains() {
        const devices = await Device.get_all();

        this.fountain_wrapper.innerHTML = '';

        for (const device of devices) {
            const html =
            `<li>
                <a href="/fountain.html?id=${device.device_id}">
                    <div class="icon">
                        <i class="fas fa-server"></i>
                    </div>

                    <div class="content">
                        <div class="heading">
                            <h3>${device.name}</h3>
                        </div>

                        <div class="description">${device.description}</div>
                    </div>
                </a>
            </li>`;

            this.fountain_wrapper.insertAdjacentHTML('beforeend', html);
        }
    }
}

const main = new Main();

document.addEventListener('DOMContentLoaded', () => main.domLookup());
