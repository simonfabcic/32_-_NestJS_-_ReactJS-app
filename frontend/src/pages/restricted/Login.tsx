import React, { useContext } from 'react'
import AuthContext from "../context/AuthContext"
import { Link } from "react-router-dom"

const Login = () => {
  let { loginUser } = useContext(AuthContext)

  const styleInputText = "border rounded-md mb-3 pl-2"

  return (
    <div className="max-w-sm mx-auto mt-8">
      <form
        action="submit"
        className="flex flex-col"
        onSubmit={loginUser}
      >
        {/* <label htmlFor="username">Username:</label>
        <input type="text" id="username" name="username" autoComplete="current-username" className={styleInputText} placeholder="John Doe" /> */}

        <label htmlFor="email">Email:</label>
        <input type="email" id="email" name="email" className={styleInputText} placeholder="email@example.com"/> 

        <label htmlFor="password">Password:</label>
        <input type="password" id="password" name="password" className={styleInputText} autoComplete="current-password" required placeholder="********" />


        <div
          className="flex flex-row justify-between mb-3"
        >
          <p>Don't have an account yet?</p>
          <Link
            type="button"
            to={"/register"}
            className="text-blue-600"
          >
            Register
          </Link>
        </div>

        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-700 text-white py-1 px-4 rounded-md"
        >        
          Login
        </button>
      </form>
    </div>
  )
}

export default Login