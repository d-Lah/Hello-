function isAuthenticated(){
    let token = localStorage.getItem("token");
    return Boolean(token);
}

function authHeaders(){
    let token = localStorage.getItem("token");
    let prefix = "Bearer";
    return {"Authorization": `${prefix} ${token}`};
}
function parseJWT(token){
    var base64Url = token.split('.')[1];
    var base64 = decodeURIComponent(atob(base64Url).split('').map((c)=>{
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(base64);
}