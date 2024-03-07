import React from 'react'
import { Link, NavLink } from "react-router-dom"
import { useContext } from "react"
import AuthContext from "../pages/context/AuthContext"

const Header = () => {

  let { loggedInUser } = useContext(AuthContext)

  return (
    <>
      <div className="flex justify-between h-8">
        {/* CONTINUE */}
        {/* TODO adjust image height */}
        <Link to="/">
          <img
            src="../images/logo.png"
            alt="skillup mentor logo"
            // className="w-28"
          />
        </Link>
        <div>
          <NavLink to="/"> Home </NavLink>
          <NavLink to="/"> Dashboard </NavLink>
          {loggedInUser ? (
            <button type="button">Logout</button>
          ) : (
            <>
              <NavLink to="/"> Login </NavLink>
              <NavLink to="/"> Register </NavLink>
            </>
          )}
        </div>
      </div>
      {/* 
        TODO:  Implement a menu bar for the header.
          skillup mentor logo

          links:
          - Home
          - Dashboard
          if not logged in:
            - Login
            - Register
          else:
            - Avatar - on click > edit user
            - Logout
      */}
    </>
  )
}

export default Header