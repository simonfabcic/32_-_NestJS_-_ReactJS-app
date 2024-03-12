import React from 'react'
import { Link } from "react-router-dom"

const Register = () => {

  const styleInputText = "border rounded-md"

  const handleSubmit  = (event: React.SyntheticEvent<HTMLFormElement>) => {
    event.preventDefault()
  }

  return (
    <div className="max-w-sm mx-auto">
      SignUp
      <form
        action="submit"
        className="flex flex-col"
        onSubmit={handleSubmit}
      >
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

      <button
        type="submit"
      >
        Create an account
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