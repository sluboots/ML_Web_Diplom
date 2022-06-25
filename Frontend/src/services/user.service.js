export default function authHeader() {
    const user = JSON.parse(localStorage.getItem('key_access'));
    console.log(user.access)
    if (user && user.access) {
        return { Authorization: 'Bearer ' + user.access };
    } else {
        return {};
    }
}