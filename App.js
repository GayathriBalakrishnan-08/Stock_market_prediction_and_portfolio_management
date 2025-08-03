import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./components/Home";
import Login from "./components/Login";
import SignUp from "./components/SignUp";
import ForgotPassword from "./components/ForgotPassword";
import User from "./components/User";
import Predict from "./components/Predict";
import Portfolio from "./components/Portfolio"; // ✅ Import the component

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/Login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/user" element={<User />} />
        <Route path="/predict" element={<Predict />} />
        <Route path="/portfolio" element={<Portfolio />} /> {/* ✅ New Route */}
      </Routes>
    </Router>
  );
}

export default App;
