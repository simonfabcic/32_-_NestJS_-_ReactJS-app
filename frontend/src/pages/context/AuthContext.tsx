import { ReactNode, createContext, useState } from "react"
import { useNavigate } from "react-router-dom";

interface AuthContextType {
  loggedInUser: string;
  setUser: React.Dispatch<React.SetStateAction<string>>;
  loginUser: () => void;
  logoutUser: () => void;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType)
export default AuthContext

export const AuthProvider = ({children}: {children: ReactNode}) => { // TODO which type should be here

  const [user, setUser] = useState("user_one")
  const navigate = useNavigate()

  // let loginUser = async () => {
  // }

  let loginUser = () => {
    setUser("user_one")
  }

  let logoutUser = () => {
    setUser("")
    navigate("/")
  }

  let contextData = {
    loggedInUser: user,
    setUser: setUser,
    loginUser: loginUser,
    logoutUser: logoutUser,
  }

  return (
    <AuthContext.Provider value={contextData}>
      {children}
    </AuthContext.Provider>
  )
}