function detect_automation() {
    if (window._phantom || window.__nightmare || window.navigator.webdriver || window.Cypress) return true;

    if (window.outerWidth === 0 || window.outerHeight === 0) return true;

    const automation_ua_list = ['HeadlessChrome', 'PhantomJS', 'Nightmare', 'Cypress'];
    if (automation_ua_list.some(ua => navigator.userAgent.includes(ua))) return true

    return false;
}

function track_event() {
    if (!base_url.includes('127.0.0.1') && !base_url.includes('localhost')) {
        if (location.hostname === 'localhost' || location.hostname === '127.0.0.1') {
            console.log('Ignoring localhost');
            return;
        }
    }

    if (location.protocol !== 'https:' && location.protocol !== 'http:') {
        console.log('Ignoring not http');
        return;
    }

    if (detect_automation()) {
        console.log('Ignoring browser automation');
        return;
    }

    var api_url = base_url + '/track';
    var data = {
        client_id: document.currentScript.getAttribute('data-code'),
        user_agent: navigator.userAgent,
        url: location.href,
        referrer: document.referrer || '',
        screen_width: window.screen.width,
        screen_height: window.screen.height,
    };
    console.log(JSON.stringify(data));

    var xhr = new XMLHttpRequest();
    xhr.open('POST', api_url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(data));

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log('Response from server:', xhr.responseText);
        }
    };
}

const base_url = 'http://127.0.0.1:5000';
track_event();