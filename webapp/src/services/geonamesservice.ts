import axios from 'axios';


const cities = {
  async fetchCities(cityName: string) {
    const username = 'lipncarbonapi';
    const maxRows = 5;
    const url = `http://api.geonames.org/searchJSON?q=${encodeURIComponent(cityName)}&username=${username}`;
    try {
      const response = await axios.get(url);
      const data = response.data;
      if (data.geonames && data.geonames.length > 0) {
        return data.geonames;
      } else {
        throw new Error("No results found");
      }
    } catch (error) {
      console.error('GeoNames API error:', error);
      throw error;
    }
  }
};


export default cities;