import { Navigate, Outlet } from 'react-router-dom'
import AuthContext from "../context/AuthContext"
import { useContext } from "react"


const PrivateRoute = () => {
  // TODO check if user exists
  // let { user } = useContext(AuthContext)
  let { loggedInUser } = useContext(AuthContext)
  return (
    loggedInUser ? (
      <Outlet />
    ) : (
      <Navigate to="/login" />
    )
  )
}

export default PrivateRoute