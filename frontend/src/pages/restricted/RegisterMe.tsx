import React, { useEffect, useState } from 'react'
import { Link, useLocation, useParams } from "react-router-dom"
import useAxios from "../utils/useAxios"

const Register = () => {

  // INTERFACES ---------------------------------------------------------------
  // --------------------------------------------------------------------------

  // VARIABLES ----------------------------------------------------------------
  // --------------------------------------------------------------------------

  let api = useAxios()

  const paramUsername = useParams().username

  const [formFirstName, setFormFirstName] = useState("")
  const [formLastName, setFormLastName] = useState("")
  const [formEmail, setFormEmail] = useState("")
  const [formPassword, setFormPassword] = useState("")
  const [formConfirmPassword, setFormConfirmPassword] = useState("")

  // API REQUESTS -------------------------------------------------------------
  // --------------------------------------------------------------------------

  // Get user profile, if parameter present -----
  useEffect(() => {
    getProfile()
  }, [])
  let getProfile = async () => {
    try {
      let response = await api.get((`/shop-api-v1/profile/${paramUsername}`))
      console.log(response)
      if (response.status === 200) {
        // setTableData(response.data)
        setFormFirstName(response.data.first_name)
        setFormLastName(response.data.last_name)
        setFormEmail(response.data.email)
      }

    } catch (err: any) {
      console.error("During getting 'Profiles', err occurred: ", err.message);
    }
  }

  const location =  useLocation()

  const styleInputText = "border rounded-md"

  // const handleSubmit  = (event: React.FormEvent<HTMLFormElement>) => {
  const handleSubmit: React.FormEventHandler<HTMLFormElement>  = (event) => {
    event.preventDefault()
    console.log("form submitted")
    // TODO handle form submission
  }

  // function handleSubmit2 (event: React.FormEvent<HTMLFormElement>) {
  //   console.log(event)
  // }

  // RETURN -------------------------------------------------------------------
  // --------------------------------------------------------------------------

  return (
    <div className="max-w-sm mx-auto">
      {location.pathname === "/register" && ("Register")}
      {location.pathname === "/me" && "Edit profile"}
      
      <form
        action="submit"
        className="flex flex-col"
        onSubmit={handleSubmit}
        // onSubmit={handleSubmit2}
      >
        <label htmlFor="avatar">Avatar:</label>
        <input type="file" />

        <label htmlFor="firstName">First name:</label>
        <input
          type="text"
          id="firstName"
          name="firstName"
          className={styleInputText}
          autoComplete="given-name"
          value={formFirstName}
          onChange={(e) => setFormFirstName(e.target.value)}
        />

        <label htmlFor="lastName">Last name:</label>
        <input
          type="text"
          id="lastName"
          name="lastName"
          className={styleInputText}
          autoComplete="family-name"
          value={formLastName}
          onChange={(e) => setFormLastName(e.target.value)}
        />

        <label htmlFor="email">Email address:</label>
        <input
          type="email"
          id="email"
          name="email"
          className={styleInputText}
          required
          autoComplete="email"
          value={formEmail}
          onChange={(e) => setFormEmail(e.target.value)}
        />

        <label htmlFor="password">Password:</label>
        <input
          type="password"
          id="password"
          name="password"
          className={styleInputText}
          autoComplete="new-password"
          value={formPassword}
          onChange={(e) => setFormPassword(e.target.value)}
        />

        <label htmlFor="confirmPassword">Confirm password:</label>
        <input
          type="password"
          id="confirmPassword"
          name="confirmPassword"
          className={styleInputText}
          autoComplete="new-password"
          value={formConfirmPassword}
          onChange={(e) => setFormConfirmPassword(e.target.value)}
        />
        { formConfirmPassword !== "" && formPassword !== formConfirmPassword && <p className="text-red-500">Passwords are not the same...</p>}

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
        
        {location.pathname === "/register" && "Create an account"}
        {location.pathname  === "/me" || location.pathname.startsWith("/dashboard/users") && "Edit account"}
      </button>
      </form>
    </div>

  )
}

export default Register