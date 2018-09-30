function refreshToken() {
    let refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken === null) {
        //console.log('Refresh token not found!');
        return false;
    }
    //console.log('Refresh token: ' + refreshToken);
    return true;
}

function initOAuth2() {
    let accessToken = localStorage.getItem('access_token');
    return accessToken !== null || refreshToken();
}