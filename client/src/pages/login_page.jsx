import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "../css/login.css";
import Loginimge from "../images/login.png";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Make a POST request to the login endpoint
      const response = await axios.post(
        "http://localhost:9001/api/auth/login",
        {
          email,
          password,
        }
      );

      // Store the token in local storage
      localStorage.setItem("token", response.data.token);

      // Navigate to the home page upon successful login
      navigate("/home");
    } catch (error) {
      console.error("Login failed", error);
      if (error.response) {
        alert(`Login failed: ${error.response.data.error}`);
      } else {
        alert("Login failed: Network error or server not reachable");
      }
    }
  };

  return (
    <div className="login">
      <div className="formbox">
        <h1>Welcome Back!</h1>
        <p>Access your account to continue learning or teaching. Let’s make today productive!</p>
        <div className="content">
          <img src={Loginimge} alt="Example" />
          <form onSubmit={handleSubmit}>
            <label>
              Email Address :-
              <br />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </label>

            <label>
              Password :-
              <br />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </label>

            <div className="remember">
              <input type="checkbox" /> <h2>Remember Me</h2>
            </div>

            <button className="submit" type="submit">
              Login
            </button>
            <br/>
            <div className="change">
            New here? Create an account t<a href="/registar">o <u>get started!</u></a>
            </div>   
          </form>
        </div>
      </div>
    </div>
  );
}
export default Login;
