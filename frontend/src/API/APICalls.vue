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
  first_name: string;
  last_name: string;
  password: string;
  password2: string;
  email: string;
}) => {
  console.log(data);
  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/register/",
      data,
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

const getCategories = async () => {
  try{
    const response = await
      axios.get("http://127.0.0.1:8000/ecoquest/categories/");
    response.data.success = true;
    return response.data;
  } catch (e: any) {
    return {error: e.message , success:false}
  }

};

// Function to get a new access token if needed
const getAccessToken = async () => {


  // Get the access token and refresh token from local storage
  const accessToken : any = localStorage.getItem('accessToken');
  const refreshToken : any = localStorage.getItem('refreshToken');

  // If no refresh token is available, return null
  if (!refreshToken || refreshToken === "") {
    return null;
  }

  // Check if the access token has expired
  const decodedToken: any = jwtDecode(accessToken);
  const currentTime = Date.now() / 1000; // Convert milliseconds to seconds
  if (decodedToken.exp < currentTime) {
    // Access token has expired, send request with refresh token to get a new access token
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/token/refresh",
          {refresh: refreshToken},
          {
              headers:{
                'Content-Type': 'application/json',
              }
      });
      if (response.status === 200) {
        const data = await response.data;
        const newAccessToken = data.access_token;

        // Store the new access token in local storage
        localStorage.setItem('access', newAccessToken);

        return newAccessToken;
      }
    } catch (error) {
      console.error('Error refreshing access token:', error);
    }

    return null; // Failed to refresh access token
  }

  // Access token is still valid
  return accessToken;
};
const CreateSavedSearch = async (data : any) => {
  console.log(data);
  // alert("Called");
  const accessToken = await getAccessToken();
  alert(accessToken);
  if(!accessToken){
    return { success: false, message : "You must Login to create a saved search", data: null}
  }

  const response = await axios.post("http://127.0.0.1:8000/ecoquest/searches/", data, {
    headers : {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + accessToken
    }
  })

  if(response.status === 201){
      return {success: true, message : 'Created New Search', data: response.data}
  }

  return {success: false, message : 'Failed to Create New Search', data: response.data}

};

const SearchPois = async (data: any) => {

  try{
    const response = await axios.post(
      `http://127.0.0.1:8000/ecoquest/search/pois/?page=${data.page}`,
      data,
      {
        headers: {
          "Content-Type": "application/json",
        },
      });

    if(response.status === 200){
      return {success: true , message: '200 OK', data: response.data}
    }

    return {success: false , message: 'Error fetching Data', data: null}

  } catch (e) {
    return {success: false , message: e, data: null}
  }

}
export { loginAuthenticate, register, getCategories, CreateSavedSearch, SearchPois };
</script>
