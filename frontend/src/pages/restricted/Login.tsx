import React, { useContext } from 'react'
import AuthContext from "../context/AuthContext"
import { Link } from "react-router-dom"

const Login = () => {
  let { loginUser } = useContext(AuthContext)

  const styleInputText = "border rounded-md"

  const handleSubmit  = (event: React.SyntheticEvent<HTMLFormElement>) => {
    event.preventDefault()
  }

  return (
    <div className="max-w-sm mx-auto">
      <div className="border border-pink-600 w-fit px-3">
        <p>[tmp]Login user with click:</p>
        {/*  TODO: Implement login functionality */}
        <button
          // onClick={loginUser}
          className="rounded-md bg-yellow-200 px-3 border border-yellow-400 m-3"
        >Login now</button>
      </div>
      <form
        action="submit"
        className="flex flex-col"
        onSubmit={loginUser}
      >
        {/* TODO change login credentials from username to email */}
        <label htmlFor="username">Username:</label>
        <input type="text" id="username" name="username" autoComplete="current-username" className={styleInputText} required/>

        <label htmlFor="email">Email:</label>
        <input type="email" id="email" name="email" className={styleInputText} /> 

        <label htmlFor="password">Password:</label>
        <input type="password" id="password" name="password" className={styleInputText} autoComplete="current-password" />


        <div
          className="flex flex-row justify-between"
        >
          <p>Don't have an account yet?</p>
          <Link
            type="button"
            to={"/register"}
          >
            Register
          </Link>
        </div>

        <button
          type="submit"
        >        
          Login
        </button>
      </form>
    </div>
  )
}

export default Login