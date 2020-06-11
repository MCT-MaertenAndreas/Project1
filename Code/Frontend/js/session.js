(async () => {
    const res = await Data.get('/api/v1/auth/session/', null, {
        'Authorization': sessionStorage.getItem('sess_token')
    });

    if (res.ok) {
        const json = await res.json();

        if (json.data.status === true) {
            window.location = '/main.html';
        }
    }

    window.location = 'login.html';
})();
