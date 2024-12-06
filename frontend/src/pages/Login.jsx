import Form from "../components/Form";
import NavBar from "../components/Navbar.jsx";
import "./styles/Login.css";

function Login() {
    return(
    <>
       <NavBar />
            <div className="login-container">
                <Form route="/api/token/" method="login" />
            </div>
        </>
    );
}

export default Login