import { useNavigate } from "react-router-dom"; 
import Form from "../components/Form";
import NavBar from "../components/Navbar.jsx";
import React, { useState } from "react";
import "./styles/CreateListing.css";

function CreateListing() {
    const navigate = useNavigate(); 
    const [imagePreview, setImagePreview] = useState(null);
    const [tags, setTags] = useState([]);  
    const [currentTag, setCurrentTag] = useState("");  

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

    const handleTagChange = (e) => {
        setCurrentTag(e.target.value);  
    };

    const addTag = () => {
        if (currentTag.trim() !== "") {
            setTags((prevTags) => [...prevTags, currentTag.trim()]); 
            setCurrentTag("");  // Clear the input field
        }
    };

    const removeTag = (index) => {
        setTags(tags.filter((_, i) => i !== index));  
    };

    return (
        <>
            <NavBar />
            <div className="createlisting-container">
                <h1>Create Listing</h1>
                <form className="form-container">
                    <input
                        className="form-input"
                        type="text"
                        placeholder="Item Name"
                        name="itemname"
                    />
                    <input
                          className="form-input"
                          type="number"
                          placeholder="Price (in USD $)"
                          name="price"
                          step="0.01"  
                          min="0"     
                    />
                    <input
                        className="form-input"
                        type="text"
                        placeholder="Condition"
                        name="condition"
                    />

                    {/*tags input */}
                    <div className="tags-input-container">
                        <input
                            className="form-input"
                            type="text"
                            placeholder="Enter a tag"
                            name="tags"
                            value={currentTag}
                            onChange={handleTagChange} 
                        />
                        <button type="button" className="add-tag-button" onClick={addTag}>Add Tag</button>
                    </div>

                    {/*display entered tags */}
                    <div className="tags-container">
                        {tags.map((tag, index) => (
                            <div key={index} className="tag">
                                {tag} 
                                <span className="remove-tag" onClick={() => removeTag(index)}></span>
                            </div>
                        ))}
                    </div>

                    <textarea
                        className="form-input"
                        placeholder="Description"
                        name="description"
                        rows="5"  
                        cols="50"  
                    ></textarea>

                    <label className="form-input">
                        Upload item image:&nbsp; 
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
                        Create Listing
                    </button>
                </form>
            </div>
        </>
    );
}

export default CreateListing;
