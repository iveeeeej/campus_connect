(() => {
    const logoutButton = document.getElementById("logoutButton");

    if (!logoutButton) {
        return;
    }

    const loginStorageKeys = [
        "campusConnectAccessToken",
        "campusConnectRefreshToken",
        "campusConnectUser",
        "accessToken",
        "access_token",
        "access",
        "refreshToken",
        "refresh_token",
        "refresh",
        "user"
    ];

    const clearStoredLogin = () => {
        loginStorageKeys.forEach((key) => {
            localStorage.removeItem(key);
            sessionStorage.removeItem(key);
        });
    };

    logoutButton.addEventListener("click", (event) => {
        event.preventDefault();
        clearStoredLogin();
        window.location.href = logoutButton.dataset.logoutRedirect || "../../index.html";
    });
})();
