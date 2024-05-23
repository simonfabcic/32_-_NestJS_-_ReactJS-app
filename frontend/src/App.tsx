import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import Header from "./pages/components/Header";
import Login from "./pages/restricted/Login";
import RegisterMe from "./pages/restricted/RegisterMe";
import PrivateRoute from "./pages/utils/PrivateRoute";
import Dashboard from "./pages/dashboard/Dashboard";
import Orders from "./pages/Orders";
import Users from "./pages/dashboard/users/Users";
import { AuthProvider } from "./pages/context/AuthContext";
import RestrictedRoute from "./pages/utils/RestrictedRoute";
import Footer from "./pages/components/Footer";
import Roles from "./pages/dashboard/roles/Roles";
import Products from "./pages/dashboard/products/Products";

export default function App() {
    return (
        <div className="max-w-screen-lg mx-auto">
            <BrowserRouter>
                <AuthProvider>
                    <div className="flex flex-col min-h-screen justify-between">
                        <div>
                            <Header />
                            <div className="px-3">
                                <Routes>
                                    <Route path="/" element={<HomePage />} />
                                    <Route element={<RestrictedRoute />}>
                                        <Route
                                            path="login"
                                            element={<Login />}
                                        />
                                        <Route
                                            path="register"
                                            element={<RegisterMe />}
                                        />
                                    </Route>
                                    <Route element={<PrivateRoute />}>
                                        <Route path="dashboard">
                                            <Route
                                                index
                                                element={<Dashboard />}
                                            />
                                            <Route
                                                path="users"
                                                element={<Users />}
                                            />
                                            <Route
                                                path="users/add-new"
                                                element={<RegisterMe />}
                                            />
                                            <Route
                                                path="users/:profile_id?"
                                                element={<RegisterMe />}
                                            />
                                            <Route
                                                path="roles"
                                                element={<Roles />}
                                            />
                                            <Route
                                                path="products"
                                                element={<Products />}
                                            />
                                            <Route
                                                path="orders"
                                                element={<Orders />}
                                            />
                                        </Route>
                                        <Route
                                            path="me"
                                            element={<RegisterMe />}
                                        />
                                    </Route>
                                    <Route
                                        path="*"
                                        element={<h1>Page not found</h1>}
                                    />
                                </Routes>
                            </div>
                        </div>
                        <Footer />
                    </div>
                </AuthProvider>
            </BrowserRouter>
        </div>
    );
}
