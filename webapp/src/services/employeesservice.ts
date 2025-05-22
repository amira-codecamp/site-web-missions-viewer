
import axios from 'axios';
import { Employee } from '@/models/Employee';

const API_URL = process.env.VUE_APP_SERVER;


const employees = {
  async fetchEmployees(token: string): Promise<Employee[]> {
    const response = await axios.get<Employee[]>(
      `${API_URL}/api/employees`,
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


export default employees;