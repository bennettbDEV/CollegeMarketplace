import { useState } from "react";
import { useNavigate } from "react-router-dom";
import NavBar from "../components/Navbar.jsx";
import api from "../api";
import "./styles/CreateListing.css";

function CreateListing() {
    const navigate = useNavigate();
    const [title, settitle] = useState("");
    const [price, setPrice] = useState("");
    const [condition, setCondition] = useState("Factory New");
    const [description, setDescription] = useState("");
    const [tags, setTags] = useState([]);
    const [currentTag, setCurrentTag] = useState("");
    const [image, setImage] = useState(null);
    const [imagePreview, setImagePreview] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            setImage(file); // Store the file
            const reader = new FileReader();
            reader.onload = () => {
                setImagePreview(reader.result); // Display preview
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
            setCurrentTag(""); // Clear the input field
        }
    };

    const removeTag = (index) => {
        setTags(tags.filter((_, i) => i !== index));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const formData = new FormData();
            formData.append("title", title);
            formData.append("price", price);
            formData.append("condition", condition);
            formData.append("description", description);
            tags.forEach((tag) => formData.append("tags", tag)); 
            formData.append("image", image);

            const res = await api.post("/api/listings/", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });

            alert("Listing created successfully!");
            navigate("/profile"); // Redirect to home or another page
        } catch (error) {
            alert("Error creating listing: " + error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <NavBar />
            <div className="createlisting-container">
                <h1>Create Listing</h1>
                <form className="form-container" onSubmit={handleSubmit}>
                    <input
                        className="form-input"
                        type="text"
                        value={title}
                        onChange={(e) => settitle(e.target.value)}
                        placeholder="Item Name"
                        name="title"
                        required
                    />
                    <input
                        className="form-input"
                        type="number"
                        value={price}
                        onChange={(e) => setPrice(e.target.value)}
                        placeholder="Price (in USD $)"
                        name="price"
                        step="0.01"
                        min="0"
                        required
                    />

                    <select
                        className="form-input"
                        value={condition}
                        onChange={(e) => setCondition(e.target.value)}
                        name="condition"
                        required
                    >
                        <option value="Factory New">Factory New</option>
                        <option value="Minimal Wear">Minimal Wear</option>
                        <option value="Fair">Fair</option>
                        <option value="Well Worn">Well Worn</option>
                        <option value="Refurbished">Refurbished</option>
                    </select>

                    <div className="tags-input-container">
                        <input
                            className="form-input"
                            type="text"
                            placeholder="Enter a tag"
                            name="tags"
                            value={currentTag}
                            onChange={handleTagChange}
                        />
                        <button type="button" className="add-tag-button" onClick={addTag}>
                            Add Tag
                        </button>
                    </div>

                    <div className="tags-container">
                        {tags.map((tag, index) => (
                            <div key={index} className="tag">
                                {tag}
                                <span className="remove-tag" onClick={() => removeTag(index)}>
                                    &times;
                                </span>
                            </div>
                        ))}
                    </div>

                    <textarea
                        className="form-input"
                        placeholder="Description"
                        name="description"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        rows="5"
                        cols="50"
                        required
                    ></textarea>

                    <label className="form-input">
                        Upload item image:&nbsp;
                        <input
                            type="file"
                            accept="image/*"
                            onChange={handleImageUpload}
                            className="file-input"
                            required
                        />
                    </label>

                    {imagePreview && (
                        <img
                            className="form-submit-image"
                            src={imagePreview}
                            alt="Item Preview"
                        />
                    )}

                    <button className="form-button" type="submit" disabled={loading}>
                        {loading ? "Submitting..." : "Create Listing"}
                    </button>
                </form>
            </div>
        </>
    );
}

export default CreateListing;