import { Link, useNavigate } from "react-router-dom";

export default function SignUpPage() {

  const navigate = useNavigate();

  function handleSignUp() {
    navigate("/raphael");
  }

  return (
    <div className="auth-page">

      <div className="auth-card">

        <h1>Create Account</h1>

        <input
          type="text"
          placeholder="Username"
        />

        <input
          type="email"
          placeholder="Email"
        />

        <input
          type="password"
          placeholder="Password"
        />

        <button onClick={handleSignUp}>
          Sign Up
        </button>

        <Link to="/">
          Back To Login
        </Link>

      </div>

    </div>
  );
}