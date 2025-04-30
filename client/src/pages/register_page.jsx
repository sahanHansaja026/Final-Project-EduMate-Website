import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import authService from "../services/authService";
import "../css/login.css";
import Loginimge from "../images/login.png";

function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate(); // useNavigate replaces useHistory

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await authService.register({ username, email, password });
      navigate("/login"); // use navigate to redirect the user
    } catch (error) {
      console.error("Registration failed", error);
    }
  };
  return (
    <div className="login">
      <div className="formbox">
        <h1>Create Your Account</h1>
        <p>
          Join our global learning community! Whether you're a teacher, student,
          or parent, sign up and start your journey today
        </p>
        <div className="content">
          <img src={Loginimge} alt="Example" />
          <form onSubmit={handleSubmit}>
          <label>
              User Name :-
              <br />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </label>
            <br />
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
            <br />
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
            <br />
            <br />
            <button className="submit" type="submit">
              Register
            </button>
            <br />
            <div className="change">
              Already registered{" "}
              <a href="/login">
                ? <u>Log in here</u>
              </a>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Register;
