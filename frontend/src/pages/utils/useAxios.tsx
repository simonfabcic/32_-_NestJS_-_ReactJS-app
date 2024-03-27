import axios from 'axios'   
import { jwtDecode } from 'jwt-decode'
import dayjs from 'dayjs'
import { useContext } from 'react'
import AuthContext from '../context/AuthContext'

interface AuthTokens {
  access: string;
  refresh: string;
}

const baseURL = "http://127.0.0.1:8456"
// const baseURL = process.env.REACT_APP_API_ENDPOINT
// const baseURL = import.meta.env.VITE_REACT_APP_API_ENDPOINT || 'default_value_if_not_defined';

const useAxios = () => {
  const {authTokens, setUserAccessToken, setAuthTokens, logoutUser} = useContext(AuthContext)

  const axiosInstance = axios.create({
    baseURL,
    headers: {
      Authorization: `Bearer ${authTokens?.access}`
    }
  });

  axiosInstance.interceptors.request.use(async req =>  {
    // https://chat.openai.com/c/3f71ef7e-84ad-4648-8c73-a3dfa7a9f2e7
    if (authTokens) {
      const userAccessToken = jwtDecode(authTokens.access)
      // const userAccessToken: any = jwtDecode<AuthTokens>(authTokens.access);
      const isAccessTokenExpired = userAccessToken.exp && dayjs.unix(userAccessToken.exp).diff(dayjs(), 'second') < 10;
      if(isAccessTokenExpired){
        const userRefreshToken = jwtDecode(authTokens.refresh)
        const isRefreshTokenExpired = userRefreshToken.exp && dayjs.unix(userRefreshToken.exp).diff(dayjs(), 'second') < 10;
        if (isRefreshTokenExpired){
          // console.log("Refreshing token expired!")
          logoutUser()
          return Promise.reject(new Error('Both tokens expired. User needs to log in again.'));
        } else {
          const response = await axios.post(`${baseURL}/core-api-v1/token/refresh/`, {
            refresh: authTokens?.refresh
          })
          // console.log("response.status: ", response)
          if (response.status === 200) {
            localStorage.setItem("authTokens", JSON.stringify(response.data))
            setAuthTokens(response.data)
            setUserAccessToken(jwtDecode(response.data.access))
            req.headers.Authorization = `Bearer ${response.data?.access}`
            // console.log(response.data)
            // console.log("tokens are equal: ", authTokens === response.data)
          }
        }
      } else {
        req.headers.Authorization = `Bearer ${authTokens?.access}`
      }
    }
    return req
  })

  return axiosInstance
}

export default useAxios;