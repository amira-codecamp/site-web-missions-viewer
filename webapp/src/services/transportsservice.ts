
import axios from 'axios';
import { Transport } from '@/models/Transport';

const API_URL = process.env.VUE_APP_SERVER;


const transports = {
  async fetchTransports(token: string): Promise<Transport[]> {
    const response = await axios.get<Transport[]>(
      `${API_URL}/api/transports`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  },
};


export default transports;