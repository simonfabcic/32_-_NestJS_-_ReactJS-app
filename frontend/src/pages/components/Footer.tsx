import React from 'react'
import { Link } from "react-router-dom"

const Footer = () => {
  return (
    // CONTINUE here - footer is not at the bottom of page
    <div className="flex justify-between h-11">
      <Link to="/">
        <img
          src="../images/logo.png"
          alt="skillup mentor logo"
          className="h-full py-2 pl-3 ${}"
        />
      </Link>
      <p>
      &copy; 2023
      </p>
    </div>
  )
}

export default Footer