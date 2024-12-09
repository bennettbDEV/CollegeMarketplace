import { useNavigate } from "react-router-dom"; 
import Form from "../components/Form";
import NavBar from "../components/Navbar.jsx";
import "./styles/Login.css";

function Login() {
    const navigate = useNavigate(); 

    return (
        <>
            <NavBar />
            <div className="login-container">
                <Form route="/api/token/" method="login" />
                <h3>New to ISU Marketplace?</h3>
                <button onClick={() => navigate("/register")}>
                    Click Here to Register an Account
                </button>
            </div>
        </>
    );
}

export default Login;