import axios from "axios";
const API_URL = "http://127.0.0.1:7000/api/token/";
const REGISTER_URL = "http://127.0.0.1:7000/api/register/"
const LOGIN_URL = "http://127.0.0.1:7000/api/login/"
class AuthService {
    login(username, password) {
        axios
            .post(LOGIN_URL, {
                username,
                password
            }).then(() => {
                console.log('111')
        })
        return axios
            .post(API_URL, {
                username,
                password
            })
            .then(response => {
                if (response.data.access) {
                    localStorage.setItem('key', JSON.stringify(response.data));
                    console.log(response.data['access']);
                }
            })






    }
    logout() {
        localStorage.removeItem('key');
    }
    register(username, password, password2, email, first_name, last_name) {
        return axios.post(REGISTER_URL, {
            username,
            password,
            password2,
            email,
            first_name,
            last_name

        });
    }
    getCurrentUser() {
        return JSON.parse(localStorage.getItem('key'));;
    }
}
export default new AuthService();