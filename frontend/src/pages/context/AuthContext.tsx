import { ReactNode, createContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { JwtPayload, jwtDecode } from "jwt-decode";

interface MyJwtPayload extends JwtPayload {
  user_id: string;
  email: string;
  profile_id: string;
}

interface AuthContextType {
  userAccessToken: MyJwtPayload | null;
  loading: boolean;
  authTokens: { access: string; refresh: string } | null;
  setUserAccessToken: (value: JwtPayload | null) => void;
  setAuthTokens: (value: JwtPayload | null) => void;
  loginUser: (event: React.FormEvent<HTMLFormElement>) => Promise<void>;
  logoutUser: () => void;
}

const baseURL = import.meta.env.VITE_BACKEND_BASE_URL;

const AuthContext = createContext<AuthContextType>({} as AuthContextType);
export default AuthContext;

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  // export const AuthProvider2 = (children: ReactNode) => {

  const navigate = useNavigate();
  let [userAccessToken, setUserAccessToken] = useState(() =>
    localStorage.getItem("authTokens")
      ? jwtDecode(localStorage.getItem("authTokens") as string)
      : null,
  );
  let [authTokens, setAuthTokens] = useState(() =>
    localStorage.getItem("authTokens")
      ? JSON.parse(localStorage.getItem("authTokens") as string)
      : null,
  );

  let loginUser = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      let response = await fetch(baseURL + "/core-api-v1/token/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          // 'username': event.currentTarget.username.value,
          email: event.currentTarget.email.value,
          password: event.currentTarget.password.value,
        }),
      });
      let data = await response.json();
      // console.log('data: ', data)
      // console.log('response: ', response)
      if (response.status === 200) {
        setAuthTokens(data);
        setUserAccessToken(jwtDecode(data.access));
        localStorage.setItem("authTokens", JSON.stringify(data));
        navigate("/");
      } else if (response.status === 401) {
        alert(
          "Unauthorized. Please check your username and password.\nServer returned response: " +
            response.status,
        );
      } else {
        alert(
          "Login failed.\nServer returned response:" +
            response.status +
            "\nData: " +
            data,
        );
      }
    } catch (error) {
      // console.log("error!!")
      alert(
        "During getting 'access' and 'refresh' token, error occur.\n" +
          "Possibility of backend server unavailability\n" +
          "Error data:\n" +
          error,
      );
    }
  };

  // let loginUser = () => {
  //   setUser("user_one")
  // }

  let logoutUser = () => {
    setAuthTokens(null);
    setUserAccessToken(null);
    localStorage.removeItem("authTokens");
    navigate("/");
  };

  let [loading, setLoading] = useState(true);

  useEffect(() => {
    if (authTokens) {
      setUserAccessToken(jwtDecode(authTokens.access));
    }
    setLoading(false);
  }, [authTokens, loading]);

  let contextData: AuthContextType = {
    userAccessToken: userAccessToken as MyJwtPayload,
    loading: loading,
    authTokens: authTokens,
    setUserAccessToken: setUserAccessToken,
    setAuthTokens: setAuthTokens,
    loginUser: loginUser,
    logoutUser: logoutUser,
  };

  return (
    <AuthContext.Provider value={contextData}>{children}</AuthContext.Provider>
  );
};
