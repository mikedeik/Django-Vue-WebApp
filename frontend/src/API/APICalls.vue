<script lang="ts">
import axios from "axios";
import jwtDecode from 'jwt-decode';

const loginAuthenticate = async (data: {
  username: string;
  password: string;
}) => {
  console.log(data);
  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/api/token/",
      JSON.stringify(data),
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    try {
        const decoded: any = jwtDecode(response.data.access);
        response.data.user_id = decoded.user_id; // Assumes that the user ID is stored in the 'UserId' claim
      } catch (error) {
        console.error('Error decoding token:', error);
        return { status:401, error: error };
      }
    response.data.status = 200;
    return response.data;
  } catch (e: any) {
    return { status:401, error: e.message };
  }
};

const register = async (data: {
  username: string;
  password: string;
  email: string;
}) => {
  console.log(data);
  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/ecoquest/register",
      JSON.stringify(data),
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    return response.data;
  } catch (e: any) {
    return { error: e.message };
  }
};
export { loginAuthenticate, register };
</script>
