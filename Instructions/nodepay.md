function printNpToken() {
    const npToken = localStorage.getItem("np_token");
    if (npToken) {
        console.log("np_token:", npToken);
    } else {
        console.log("np_token not found in Local Storage.");
    }
}

printNpToken()