import React from "react";
import { Link, NavLink } from "react-router-dom";

interface NavbarProps {
    setShowNavbar: React.Dispatch<React.SetStateAction<boolean>>;
    showNavbar: boolean;
}

const Navbar: React.FC<NavbarProps> = ({ setShowNavbar, showNavbar }) => {
    const styleLink = " ";
    return (
        <div
            className={`
                fixed top-0 w-1/4 h-full rounded-r-2xl 
                ${showNavbar ? "translate-x-0 opacity-100 duration-500 " : "-translate-x-full opacity-0 duration-500 "}
            `}
        >
            {/* <div className={`
                fixed top-0 w-1/4 h-full rounded-r-2xl
                ${showNavbar ? 'duration-300 ' : 'scale-0 duration-300 origin-top-left'}
                `}
            > */}

            <div className="h-20 flex flex-col justify-end rounded-bl-2xl bg-gray-300">
                <div className="flex h-11">
                    <div className="text-2xl pl-3 my-auto">
                        <span
                            className="font-semibold cursor-pointer"
                            onClick={() => {
                                setShowNavbar(false);
                            }}
                        >
                            &#x2715;
                        </span>
                    </div>
                    <Link to="/">
                        <img
                            src="/images/logo.png"
                            alt="skillup mentor logo"
                            className="h-full py-2 pl-3 ${}"
                        />
                    </Link>
                </div>
            </div>

            <nav
                className="
        flex flex-col gap-y-5
        border-t-4 border-gray-200 rounded-t-2xl bg-gray-300 h-full p-3
        "
            >
                {[
                    { url: "/dashboard", content: "Dashboard" },
                    { url: "/dashboard/users", content: "Users" },
                    { url: "/dashboard/roles", content: "Roles" },
                    { url: "/dashboard/products", content: "Products" },
                    { url: "/dashboard/orders", content: "Orders" },
                ].map((navbarItem) => (
                    <NavLink
                        key={navbarItem.content}
                        to={navbarItem.url}
                        className={
                            styleLink +
                            (location.pathname === navbarItem.url
                                ? "font-bold "
                                : " ") +
                            ""
                        }
                        onClick={() => setShowNavbar(false)}
                    >
                        {navbarItem.content}
                    </NavLink>
                ))}
            </nav>
        </div>
    );
};

export default Navbar;
