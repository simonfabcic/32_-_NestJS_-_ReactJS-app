import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from './pages/HomePage'
import Header from './pages/components/Header'
import Login from './pages/restricted/Login';
import Register from './pages/restricted/Register';
import PrivateRoute from './pages/utils/PrivateRoute';
import Dashboard from "./pages/Dashboard";
import Orders from "./pages/Orders";
import Users from "./pages/users/Users";
import { AuthProvider } from "./pages/context/AuthContext";

export default function App() {
  return (
    <div className="max-w-screen-lg mx-auto">
      <BrowserRouter>
        <AuthProvider>
          <Header />
          <Routes>
            <Route path='/'  element={<HomePage />} />
            <Route path="login" element={<Login />} />
            <Route path="register" element={<Register />} />
            <Route element={<PrivateRoute />}>
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="orders" element={<Orders />} />
              <Route path="users" element={<Users />} />
              <Route path="user/add-edit/:user_id?" element={<Users />} />
            </Route>
            <Route path="*" element={<h1>Page not found</h1>} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </div>
  )
}