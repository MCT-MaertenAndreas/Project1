class Notification {
    constructor(message, color, time, uniqueId, queue) {
        this.message = message;
        this.color = color;
        this.time = time;

        this.uniqueId = uniqueId;
        this.queue = queue;
    }

    calculatePosition(length = null) {
        if (!length) {
            length = this.queue.children.length - 1;
        }

        this.position = 10;

        for (let i = 0; i < length; i++) {
            const notification = this.queue.children.item(i);

            if (!notification.dataset.deleting) {
                this.position += notification.offsetHeight + 15;
            }
        }
    }

    createNode() {
        if (this.color) {
            this.color = `notification-${this.color}`;
        }

        const tempObject = `
            <div id="notify-${this.uniqueId}" class="notification ${this.color}">
                <p>
                    ${this.message}
                </p>
            </div>`;

        this.queue.insertAdjacentHTML('beforeend', tempObject);

        this.object = document.getElementById(`notify-${this.uniqueId}`);
    }

    delete() {
        let newQueue = [];

        for (let i = 0; i < this.queue.children.length; i++) {
            const notification = this.queue.children.item(i);

            if (notification.id == this.object.id) {
                this.removeSelf();

                continue;
            }

            if (notification.dataset.deleting) {
                continue;
            }

            newQueue.push(notification);
        }

        // newQueue.reverse();

        for (let i = 0; i < newQueue.length; i++) {
            const notification = newQueue[i];

            this.calculatePosition(i);

            notification.style.top = `${this.position}px`;
            notification.style.transition = '0.3s';
        }
    }

    pop() {
        this.createNode();

        this.calculatePosition();

        this.setPosition();

        this.startRemoveTimer();
    }

    removeSelf() {
        this.object.dataset.deleting = true;
        this.object.style.top = '';
        this.object.style.transition = '';
        this.object.style.transform = 'scale(0.98)';
        const el = this.object;

        setTimeout(() => {
            el.remove();
        }, 800);
    }

    async setPosition() {
        this.object.style.zIndex = 1000 - this.uniqueId;

        setTimeout(() => { this.object.style.top = `${this.position}px`; }, 10);
    }

    startRemoveTimer() {
        const self = this;

        setTimeout(() => {
            self.delete();
        }, this.time + 10);
    }
}
