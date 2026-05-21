(() => {
    const logoutButtons = new Set();
    const explicitLogoutButton = document.getElementById("logoutButton");
    if (explicitLogoutButton) {
        logoutButtons.add(explicitLogoutButton);
    }

    document.querySelectorAll(".user-dropdown a").forEach((link) => {
        if (link.textContent.trim().toLowerCase() === "logout") {
            logoutButtons.add(link);
        }
    });

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

    logoutButtons.forEach((logoutButton) => {
        logoutButton.addEventListener("click", (event) => {
            event.preventDefault();
            clearStoredLogin();
            window.location.href = logoutButton.dataset.logoutRedirect || "../../index.html";
        });
    });
})();
