
import axios from 'axios';
import { TravelEmission } from '@/models/Emission';

const API_URL = process.env.VUE_APP_SERVER;


const carbon_footprint = {
  async getCarbonFootprint(payload: TravelEmission, accessToken: string): Promise<any> {
    try {
      const response = await axios.post(
        `${API_URL}/emissions/travel/`,
        payload,
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          },
        }
      );
      return response.data;
    } catch (error: any) {
      if (error.response) {
        throw new Error(`API Error: ${error.response.status} - ${error.response.data}`);
      } else {
        throw new Error(`Network Error: ${error.message}`);
      }
    }
  },
};

export default carbon_footprint;