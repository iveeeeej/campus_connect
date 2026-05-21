(() => {
    const requiredRole = document.currentScript?.dataset.requiredRole || "SUPER_ADMIN";
    const loginRedirect = document.currentScript?.dataset.loginRedirect || "../../index.html";

    const tokenKeys = [
        "campusConnectAccessToken",
        "accessToken",
        "access_token",
        "access"
    ];
    const refreshKeys = [
        "campusConnectRefreshToken",
        "refreshToken",
        "refresh_token",
        "refresh"
    ];
    const userKeys = [
        "campusConnectUser",
        "user"
    ];

    const getApiBaseUrl = () => {
        const configuredUrl = window.CAMPUS_CONNECT_API_BASE_URL || localStorage.getItem("campusConnectApiBaseUrl");
        if (configuredUrl) {
            return configuredUrl.replace(/\/$/, "");
        }

        const isDjangoOrigin = ["localhost", "127.0.0.1"].includes(window.location.hostname)
            && window.location.port === "8000";
        if (isDjangoOrigin) {
            return window.location.origin;
        }

        return "http://127.0.0.1:8000";
    };

    const getStoredToken = () => {
        for (const key of tokenKeys) {
            const localValue = localStorage.getItem(key);
            if (localValue) {
                return { token: localValue, storage: localStorage };
            }

            const sessionValue = sessionStorage.getItem(key);
            if (sessionValue) {
                return { token: sessionValue, storage: sessionStorage };
            }
        }

        return { token: null, storage: sessionStorage };
    };

    const clearStoredLogin = () => {
        [...tokenKeys, ...refreshKeys, ...userKeys].forEach((key) => {
            localStorage.removeItem(key);
            sessionStorage.removeItem(key);
        });
    };

    const redirectToLogin = () => {
        clearStoredLogin();
        window.location.replace(loginRedirect);
    };

    const protectPage = async () => {
        const { token, storage } = getStoredToken();
        if (!token) {
            redirectToLogin();
            return;
        }

        try {
            const response = await fetch(`${getApiBaseUrl()}/api/accounts/me/`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error("Session validation failed.");
            }

            const user = await response.json();
            if (user.role !== requiredRole || user.account_status !== "APPROVED" || user.is_active === false) {
                throw new Error("The current account is not allowed on this page.");
            }

            storage.setItem("campusConnectUser", JSON.stringify(user));
            window.CampusConnectCurrentUser = user;
        } catch (error) {
            redirectToLogin();
        }
    };

    protectPage();
})();
