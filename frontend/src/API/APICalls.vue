<script lang="ts">
import axios from "axios";

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
      "http://127.0.0.1:8000/register",
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
