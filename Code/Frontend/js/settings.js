class Settings {
    constructor() {

    }

    domLookup() {
        const form = document.getElementById('settings_form');

        this.settings = {
            light: document.getElementById('light_sens'),
            distance: document.getElementById('distance_sens')
        };

        form.addEventListener('submit', () => this.updateSettings());
    }

    updateSettings() {
        const result = Data.put('/api/v1/settings/', {
            distance_sensor_sens: this.settings.distance.value,
            light_sensor_sens: this.settings.distance.value
        });

        if (result.status == 204) {
            alert('Successfully updated settings');

            return;
        }

        alert('Failed to update settings!');
    }
}

const settings = new Settings();

document.addEventListener('DOMContentLoaded', () => settings.domLookup());
