
import axios from 'axios';

const API_URL = process.env.VUE_APP_SERVER;


interface Credentials {
  login: string;
  password: string;
}

interface Token {
  access: string;
  refresh: string;
}


const auth = {
  async login(credentials: Credentials): Promise<Token> {
    const response = await axios.post<Token>(
      `${API_URL}/auth/jwt/create`,
      credentials
    );
    return response.data;
  },
};

export default auth;