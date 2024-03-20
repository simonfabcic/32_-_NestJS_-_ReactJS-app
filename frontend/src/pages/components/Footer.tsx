import React from 'react'
import { Link } from "react-router-dom"

const Footer = () => {
  return (
    // CONTINUE here - footer is not at the bottom of page
    <div className="h-20 bg-gray-200 rounded-t-2xl">
      <div className="flex justify-between h-11 items-center px-3">
        <Link to="/">
          <img
            src="../images/logo.png"
            alt="skillup mentor logo"
            className="h-11 py-2"
          />
        </Link>
        <p>
        &copy; 2023
        </p>
      </div>
    </div>
  )
}

export default Footer