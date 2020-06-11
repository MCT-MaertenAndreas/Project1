document.addEventListener('DOMContentLoaded', async () => {
    const ip = document.querySelector('.interface-ip > .ip');

    const res = await Data.get('/api/v1/status/ip/');

    if (res.ok) {
        const json = await res.json();

        ip.innerHTML = json.ip;

        return;
    }

    ip.innerHTML = 'Unknown Address';
});
