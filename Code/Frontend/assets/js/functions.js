class Function {
    constructor(main) {
        this.parent = main;
    }

    alignPopouts() {
        const
            navPopouts = this.parent.navPopouts,
            winHeight = window.innerHeight;

        for (let i = 0; i < navPopouts.length; i++) {
            let
                height = 0,
                element = navPopouts[i],
                elementBounds = element.getBoundingClientRect(),
                popout = document.getElementById(element.getAttribute('data-target')),
                popoutBounds = popout.getBoundingClientRect(),
                alignment = popout.getAttribute('data-align');

            if (alignment == "bottom") {
                height = winHeight - elementBounds.bottom - 10;

                popout.style = "bottom: " + height + "px;";
            }
            else if (alignment == "top") {
                height = elementBounds.top - 10;

                popout.style = "top: " + height + "px;";
            }
            else if (alignment == "middle") {
                /*if (popoutBounds.height < (elementBounds.height - 5)) {
                    height = elementBounds.top + (elementBounds.height / 2) - (popoutBounds.height / 2);
                }
                else {
                    height = elementBounds.top + (elementBounds.height / 2) - (popoutBounds.height / 2);
                }*/
                height = elementBounds.top + (elementBounds.height / 2) - (popoutBounds.height / 2);

                popout.style = "top: " + height + "px;";
            }
        }
    }

    getPercentage(value, total) {
        return value / total * 100;
    }

    popNotification(message, color = null, time = 6500) {
        if (!this.notificationQueue) {
            const notificationQueue = '<section id="notification-queue"></section>';

            this.parent.body.insertAdjacentHTML('afterbegin', notificationQueue);

            this.notificationQueue = document.getElementById('notification-queue');
            this.notifyId = 0;
        }

        const notification = new Notification(message, color, time, this.notifyId, this.notificationQueue);

        notification.pop();

        this.notifyId++;
    }

    popoutAppear(e) {
        // Remove all hover states from the last active one
        if (this.lastActive) {
            this.lastActive.classList.remove('nav-popout_hover');
            this.parent.navbar.classList.remove('nav_hover');

            const navPopout = document.querySelector(`[data-target="${this.lastActive.id}"]`);
            navPopout.classList.remove('nav-list_hover');

            this.lastActive = null;
        }

        const el = e.target;

        if (el.classList.contains('hasPopout')) {
            const
                target = document.getElementById(el.dataset.target),
                direction = target.dataset.direction;

            target.classList.add('nav-popout_hover');

            if (direction == 'right') {
                target.style.left = 'var(--nav-width)';
            }
            else {
                target.style.right = 'var(--nav-width)';
            }

            this.lastActive = target;

            return;
        }

        this.parent.navbar.classList.add('nav_hover');

        const navPopout = document.querySelector(`[data-target="${el.id}"]`);
        navPopout.classList.add('nav-list_hover');

        const direction = el.dataset.direction;
        el.classList.add('nav-popout_hover');

        if (direction == 'right') {
            el.style.left = 'var(--nav-width)';
        }
        else {
            el.style.right = 'var(--nav-width)';
        }

        this.lastActive = el;
    }

    popoutDissapear(e) {
        // Remove all hover states from the last active one
        if (this.lastActive) {
            this.lastActive.classList.remove('nav-popout_hover');
            this.lastActive.style.left = '';
            this.lastActive.style.right = '';

            this.parent.navbar.classList.remove('nav_hover');

            const navPopout = document.querySelector(`[data-target="${this.lastActive.id}"]`);
            navPopout.classList.remove('nav-list_hover');

            this.lastActive = null;

            return;
        }
    }

    popoutListeners() {
        for (let i = 0; i < this.parent.navPopouts.length; i++) {
            this.parent.navPopouts[i].addEventListener('mouseenter', (e) => this.popoutAppear(e));
            this.parent.navPopouts[i].addEventListener('mouseleave', (e) => this.popoutDissapear(e));
        }

        for (let i = 0; i < this.parent.popouts.length; i++) {
            this.parent.popouts[i].addEventListener('mouseenter', (e) => this.popoutAppear(e));
            this.parent.popouts[i].addEventListener('mouseleave', (e) => this.popoutDissapear(e));
        }
    }

    promTimeout(timeout) {
        return new Promise((resolve, reject) => setTimeout(resolve, timeout));
    }

    async updateContent(filePath) {
        const
            response = await this.parent.get(filePath),
            html = await response.text();

        this.parent.contentWrapper.innerHTML = html;
    }
}
