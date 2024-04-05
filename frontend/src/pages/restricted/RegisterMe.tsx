import React, { useContext, useEffect, useState } from 'react'
import { Link, Navigate, useLocation, useParams } from "react-router-dom"
import useAxios from "../utils/useAxios"
import AuthContext from "../context/AuthContext"
import { useNavigate } from "react-router-dom";

const Register = () => {

  // INTERFACES ---------------------------------------------------------------
  // --------------------------------------------------------------------------

  // VARIABLES ----------------------------------------------------------------
  // --------------------------------------------------------------------------

  let api = useAxios()
  let { userAccessToken: loggedInUser } = useContext(AuthContext)
  const navigate = useNavigate()

  const paramProfileId = useParams().profile_id || (loggedInUser?.profile_id)
  const location =  useLocation()
  const [formFirstName, setFormFirstName] = useState("")
  const [formLastName, setFormLastName] = useState("")
  const [formEmail, setFormEmail] = useState("")
  const [formPassword, setFormPassword] = useState("")
  const [formConfirmPassword, setFormConfirmPassword] = useState("")
  const [emailAlreadyTaken, setEmailAlreadyTaken] = useState(false)

  const styleInputText = "border rounded-md"

  // API REQUESTS -------------------------------------------------------------
  // --------------------------------------------------------------------------

  // Get user profile, if parameter present -----
  useEffect(() => {
    if (location.pathname.endsWith("/add-new"))
      return
    getProfile()
  }, [])
  let getProfile = async () => {
    if (paramProfileId) {
      try {
        let response = await api.get((`/shop-api-v1/profile/${paramProfileId}`))
        // console.log(response)
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
  }


  // Create or update profile -------------------
  // const handleSubmit  = (event: React.FormEvent<HTMLFormElement>) => {
  const handleSubmit: React.FormEventHandler<HTMLFormElement>  = async (event) => {
    event.preventDefault()
    console.log("firstName: ", event.currentTarget.firstName.value)
    // POST -------
    if (location.pathname === "/register" || location.pathname.endsWith("/add-new")) {
      try {
        let response = await api.post(`/shop-api-v1/profile/`)
        if (response.statusText === "OK") {
          navigate("/users")
        }
        if (response.status === 409)
          setEmailAlreadyTaken(true)
      } catch (err) {
        if (err instanceof Error) {
          console.error("During creating 'Profile', err occurred: ", err.message);
        }
      }
    }
    // PUT --------
    // Edit user or my profile --
    else if (location.pathname.startsWith("/dashboard/users") || location.pathname  === "/me") {
      console.log("paramUserId: ", paramProfileId)
      try {
        let response = await api.put(`/shop-api-v1/profile/${paramProfileId}/`, {
          "firstName": event.currentTarget.firstName.value,
          "lastName": event.currentTarget.lastName.value,
          "email": event.currentTarget.email.value,
          "password": event.currentTarget.password.value,
          "userID": paramProfileId
        })
        if (response.statusText === "OK") {
          navigate("/users")
        }
      } catch (err) {
        if (err instanceof Error) {
          console.error("During creating 'Profile', err occurred: ", err.message);
        }
      }
    }
  }

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
          required
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
          required
        />

        <label htmlFor="email">Email address:</label>
        <input
          type="email"
          id="email"
          name="email"
          className={styleInputText}
          required
          autoComplete="email"
          value={location.pathname.endsWith("/add-new") ? "" : formEmail || loggedInUser?.email}
          onChange={(e) => setFormEmail(e.target.value)}
        />
        {emailAlreadyTaken &&
          <p className="text-red-500">Email already taken...</p>
        }

        <label htmlFor="password">Password:</label>
        <input
          type="password"
          id="password"
          name="password"
          className={styleInputText}
          autoComplete="new-password"
          value={formPassword}
          onChange={(e) => setFormPassword(e.target.value)}
          required={location.pathname === "/register" ? true : false}
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
        {
          (formPassword !== "" ||
          formConfirmPassword !== "") &&
          formPassword !== formConfirmPassword &&
            <p className="text-red-500">Passwords are not the same...</p>
        }

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
        disabled={
          ((formPassword !== "" ||
          formConfirmPassword !== "") &&
          formPassword !== formConfirmPassword) ?
          true
          :
          false
        }
        className={
          ((formPassword !== "" ||
          formConfirmPassword !== "") &&
          formPassword !== formConfirmPassword) ?
          "cursor-not-allowed"
          :
          ""
        }
      >
        {
          ((location.pathname === "/register" || location.pathname.endsWith("/add-new") ) && "Create an account")
        ||
          ((location.pathname  === "/me" || location.pathname.startsWith("/dashboard/users")) && "Edit account")
        }
      </button>
      </form>
    </div>

  )
}

export default Register