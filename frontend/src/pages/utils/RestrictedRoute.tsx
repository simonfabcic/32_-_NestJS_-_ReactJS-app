import { Navigate, Outlet } from 'react-router-dom'
import AuthContext from "../context/AuthContext"
import { useContext } from "react"


const RestrictedRoute = () => {
  // TODO check if user exists
  // let { user } = useContext(AuthContext)
  let { userAccessToken: loggedInUser } = useContext(AuthContext)
  return (
    !loggedInUser ? (
      <Outlet />
    ) : (
      <Navigate to="/" />
    )
  )
}

export default RestrictedRoute