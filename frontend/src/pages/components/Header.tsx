import { Link, NavLink, useNavigate, useLocation } from "react-router-dom"
import { useContext } from "react"
import AuthContext from "../context/AuthContext"

const Header = () => {

  let { loggedInUser, logoutUser } = useContext(AuthContext)

  const location =  useLocation()
  const navigate = useNavigate()


  const styleLink = " "

  return (
    <div className="h-20 bg-gray-200 flex flex-col justify-end rounded-b-2xl">
      <div className="flex justify-between h-11 content-evenly w-full overflow-hidden"> 
        <Link to="/">
          <img
            src="../images/logo.png"
            alt="skillup mentor logo"
            className="h-full py-2 pl-3 ${}"
          />
        </Link>
        <div className="my-auto flex gap-4 pr-8">
          <NavLink
            to="/"
            className={
              styleLink +
              (location.pathname === "/" ? "font-bold " : " ") + 
              ""
            }
          >
            Home
          </NavLink>
          <NavLink
            to="dashboard"
            className={
              styleLink +
              (location.pathname === "/dashboard" ? "font-bold " : " ") + 
              ""
            }
          >
            Dashboard
          </NavLink>
          {loggedInUser ? (
            <>
              <button
                type="button"
                onClick={logoutUser}
              >
                Logout
              </button>
              {/* TODO if users image present, show image */}
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                className="w-6 h-6 cursor-pointer"
                onClick={() => navigate("/me")}
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
              </svg>
            </>
          ) : (
            <>
              <NavLink
                to="login"
                className={
                  styleLink +
                  (location.pathname === "/login" ? "font-bold " : " ") + 
                  ""
                }
              >
                Login
              </NavLink>
              <NavLink
                to="register"
                className={
                  styleLink +
                  (location.pathname === "/register" ? "font-bold " : " ") + 
                  ""
                }
              >
                Register
              </NavLink>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default Header