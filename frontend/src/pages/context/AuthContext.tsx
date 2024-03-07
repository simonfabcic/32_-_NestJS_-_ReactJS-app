import { ReactNode, createContext } from "react"

interface AuthContextType {
  key1: string;
  isAuthenticated: boolean;
  loggedInUser: string;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType)
export default AuthContext

export const AuthProvider = ({children}: {children: ReactNode}) => { // TODO which type should be here


  let contextData = {
    key1:  'value1',
    isAuthenticated: false,
    loggedInUser: 'User1',
  }

  return (
    <AuthContext.Provider value={contextData}>
      {children}
    </AuthContext.Provider>
  )
}