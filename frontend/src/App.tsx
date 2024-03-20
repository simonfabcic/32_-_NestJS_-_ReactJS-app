import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from './pages/HomePage'
import Header from './pages/components/Header'
import Login from './pages/restricted/Login';
import RegisterMe from './pages/restricted/RegisterMe';
import PrivateRoute from './pages/utils/PrivateRoute';
import Dashboard from "./pages/dashboard/Dashboard";
import Orders from "./pages/Orders";
import Users from "./pages/dashboard/users/Users";
import { AuthProvider } from "./pages/context/AuthContext";
import RestrictedRoute from "./pages/utils/RestrictedRoute";
import Footer from "./pages/components/Footer";

export default function App() {
  return (
    <div className="max-w-screen-lg mx-auto">
      <BrowserRouter>
        <AuthProvider>

          <div className="flex flex-col min-h-screen justify-between">
            <div>
              <Header />
              <Routes>
                <Route path='/'  element={<HomePage />} />
                <Route element={<RestrictedRoute />} >
                  <Route path="login" element={<Login />} />
                  <Route path="register" element={<RegisterMe />} />
                </Route>
                <Route element={<PrivateRoute />}>
                  <Route path="dashboard">
                    <Route index element={<Dashboard />} />
                    <Route path="users" element={<Users />} />
                    <Route path="roles" element={<Users />} />
                    <Route path="products" element={<Users />} />
                    <Route path="orders" element={<Orders />} />
                  </Route>
                  <Route path="user/add-edit/:user_id?" element={<RegisterMe />} />
                  <Route path="me" element={<RegisterMe />} />
                </Route>
                <Route path="*" element={<h1>Page not found</h1>} />
              </Routes>
            </div>
            <Footer />
          </div>
        </AuthProvider>
      </BrowserRouter>
    </div>
  )
}