import React from 'react'
import { Link, useLocation } from "react-router-dom"

const Register = () => {

  const location =  useLocation()

  const styleInputText = "border rounded-md"

  const handleSubmit  = (event: React.SyntheticEvent<HTMLFormElement>) => {
    event.preventDefault()
  }

  return (
    <div className="max-w-sm mx-auto">
      {location.pathname === "/register" && ("Register")}
      {location.pathname === "/me" && "Edit profile"}
      
      <form
        action="submit"
        className="flex flex-col"
        onSubmit={handleSubmit}
      >
        <label htmlFor="avatar">Avatar:</label>
        <input type="file" />

        <label htmlFor="firstName">First name:</label>
        <input type="text" id="firstName" name="firstName" className={styleInputText} />

        <label htmlFor="lastName">Last name:</label>
        <input type="text" id="lastName" name="lastName" className={styleInputText} />

        <label htmlFor="email">Email address:</label>
        <input type="email" id="email" name="email" className={styleInputText} required/>

        <label htmlFor="password">Password:</label>
        <input type="password" id="password" name="password" className={styleInputText} />

        <label htmlFor="confirmPassword">Confirm password:</label>
        <input type="password" id="confirmPassword" name="confirmPassword" className={styleInputText} />

        {location.pathname === "/register" && 
          <div
            className="flex flex-row justify-between"
          >
            <p>Already have an account?</p>
            <Link
              type="button"
              to={"/login"}
            >
              Login
            </Link>
          </div>
        }

      <button
        type="submit"
      >
        
        {location.pathname === "/register" && ("Create an account")}
        {location.pathname === "/me" && "Edit account"}
      </button>

      </form>
    {/* TODO: Implement sign up form
      - First name
      - Last name
      - Email
      - Password
      - Confirm password
      - Already account - redirect to login
    */}
      
    </div>

  )
}

export default Register