import React, { useContext } from 'react'
import AuthContext from "../context/AuthContext"

const Login = () => {
  let { loginUser } = useContext(AuthContext)


  return (
    <div>
      <p>Login user with click:</p>
      {/*  TODO: Implement login functionality */}
      <button
        onClick={loginUser}
      >Login now</button>
    </div>
  )
}

export default Login