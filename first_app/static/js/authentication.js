function isAuthenticated(){
    let token = localStorage.getItem("token");
    return Boolean(token);
}

function authHeaders(){
    let token = localStorage.getItem("token");
    let prefix = "Bearer";
    return {"Authorization": `${prefix} ${token}`}
}