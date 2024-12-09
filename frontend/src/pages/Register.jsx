import React, { useState } from "react";
import NavBar from "../components/Navbar.jsx";
import "./styles/Register.css";

function Register() {
    const [imagePreview, setImagePreview] = useState(null);

    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = () => {
                setImagePreview(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    return (
        <>
            <NavBar />
            
            <div className="register-container">
            <h1>Register Account</h1>
                <form className="form-container">
                    <input
                        className="form-input"
                        type="text"
                        placeholder="*Username"
                        name="username"
                    />
                    <input
                        className="form-input"
                        type="password"
                        placeholder="*Password"
                        name="password"
                    />
                    <input
                        className="form-input"
                        type="text"
                        placeholder="Location"
                        name="location"
                    />
                    
                    <label className="form-input">
                        Upload profile picture:&nbsp; 
                        <input
                            type="file"
                            accept="image/*"
                            onChange={handleImageUpload}
                            className="file-input"
                        />
                    </label>

                    {imagePreview && (
                        <input
                            className="form-submit-image"
                            type="image"
                            src={imagePreview}
                            alt="Submit"
                        />
                    )}

                    <button className="form-button" type="submit">
                        Submit
                    </button>
                </form>
            </div>
        </>
    );
}

export default Register;
