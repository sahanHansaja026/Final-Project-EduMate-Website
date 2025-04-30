import React, { Component } from "react";
import axios from "axios";
import { withNavigation } from "../utils/withNavigation"; // Correct relative path
import authService from "../services/authService";
import { v4 as uuidv4 } from "uuid";
import "../css/input.css";
import defaultImage from "../images/card.png";

class CreateCard extends Component {
  constructor(props) {
    super(props);
    this.state = {
      posts: [],
      newPost: {
        id: "",
        title: "",
        summery: "",
        card_id: "",
        image: null,
        tags: [],
      },
      userEmail: "",
      errorMessage: "",
      imagePreview: defaultImage,
      currentTag: "",
      suggestedTags: [],
      popularTags: [
        "Science",
        "Maths",
        "Video",
        "Tutorial",
        "Learning",
        "Physics",
        "Chemistry",
        "Biology",
        "Computer Science",
        "History",
        "Literature",
        "Geography",
        "Art",
        "Engineering",
        "Psychology",
        "Economics",
        "Philosophy",
        "Music",
        "Languages",
        "Technology",
        "Health",
      ],
    };
    this.fileInputRef = React.createRef();
  }

  async componentDidMount() {
    await this.fetchUserData();
    this.retrievePosts();
  }

  async fetchUserData() {
    try {
      const userData = await authService.getUserData();
      this.setState({ userEmail: userData.email });
    } catch (error) {
      console.error("Failed to fetch user data", error);
      this.setState({ errorMessage: "Failed to fetch user data." });
    }
  }

  retrievePosts() {
    axios
      .get("http://localhost:9001/posts")
      .then((res) => {
        if (res.data.success) {
          this.setState({ posts: res.data.existingPosts });
        } else {
          console.error("Error fetching posts:", res.data.error);
          this.setState({ errorMessage: res.data.error });
        }
      })
      .catch((error) => {
        console.error("Error fetching posts:", error);
        this.setState({ errorMessage: "Error fetching posts." });
      });
  }

  handleChange = (event) => {
    const { name, value } = event.target;
    this.setState((prevState) => ({
      newPost: {
        ...prevState.newPost,
        [name]: value,
      },
      errorMessage: "",
    }));
  };

  handleImageChange = (event) => {
    const file = event.target.files[0];
    this.setState({
      newPost: {
        ...this.state.newPost,
        image: file,
      },
      imagePreview: URL.createObjectURL(file),
      errorMessage: "",
    });
  };

  handleTagInputChange = (event) => {
    const currentTag = event.target.value;
    this.setState({
      currentTag,
      suggestedTags: this.state.popularTags.filter((tag) =>
        tag.toLowerCase().startsWith(currentTag.toLowerCase())
      ),
    });
  };

  handleTagAdd = (event) => {
    event.preventDefault();
    const { currentTag, newPost } = this.state;
    if (currentTag && !newPost.tags.includes(currentTag)) {
      this.setState((prevState) => ({
        newPost: {
          ...prevState.newPost,
          tags: [...prevState.newPost.tags, currentTag],
        },
        currentTag: "",
        suggestedTags: [],
      }));
    }
  };

  handleSuggestionClick = (suggestion) => {
    this.setState((prevState) => ({
      newPost: {
        ...prevState.newPost,
        tags: [...prevState.newPost.tags, suggestion],
      },
      currentTag: "",
      suggestedTags: [],
    }));
  };

  handleTagRemove = (tag) => {
    this.setState((prevState) => ({
      newPost: {
        ...prevState.newPost,
        tags: prevState.newPost.tags.filter((t) => t !== tag),
      },
    }));
  };

  handleSubmit = (event) => {
    event.preventDefault();

    const { title, summery, image, tags } = this.state.newPost;
    if (!title || !summery || !image) {
      alert("Please fill in all required fields.");
      return;
    }

    const newPostId = uuidv4();
    const formData = new FormData();
    formData.append("id", newPostId);
    formData.append("card_id", newPostId);
    formData.append("email", this.state.userEmail);
    formData.append("title", title);
    formData.append("summery", summery);
    formData.append("image", image);
    formData.append("tags", JSON.stringify(tags));

    axios
      .post("http://localhost:9001/posts/save", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((res) => {
        if (res.data.success) {
          this.setState({
            newPost: { id: "", title: "", summery: "", image: null, tags: [] },
            imagePreview: defaultImage,
          });
          this.retrievePosts();
          this.props.navigate(`/teacherweek/${newPostId}`);
        } else {
          this.setState({ errorMessage: res.data.error });
        }
      })
      .catch(() => {
        this.setState({ errorMessage: "Error adding post." });
      });
  };

  handleImageClick = () => {
    this.fileInputRef.current.click();
  };

  render() {
    return (
      <div className="create-card-container">
        <div className="form-container">
          <h2>Create New Post</h2>
          <form onSubmit={this.handleSubmit}>
            {this.state.errorMessage && (
              <div className="error-message">{this.state.errorMessage}</div>
            )}

            <div className="image-upload-section">
              <div className="image-preview" onClick={this.handleImageClick}>
                <img
                  src={this.state.imagePreview}
                  alt="Image Preview"
                  className="image-preview-img"
                />
                <span className="image-upload-text">Click to upload</span>
              </div>
              <input
                type="file"
                name="image"
                accept=".png, .jpg, .jpeg"
                onChange={this.handleImageChange}
                ref={this.fileInputRef}
                style={{ display: "none" }}
                required
              />
            </div>

            <div className="input-group">
              <input
                type="text"
                name="title"
                value={this.state.newPost.title}
                placeholder="Post Title"
                onChange={this.handleChange}
                required
              />
            </div>

            <div className="input-group">
              <textarea
                name="summery"
                value={this.state.newPost.summery}
                onChange={this.handleChange}
                placeholder="Post Summary"
                required
              />
            </div>

            <div className="tags-section">
              <input
                type="text"
                placeholder="Add a tag and press Enter"
                value={this.state.currentTag}
                onChange={this.handleTagInputChange}
                onKeyPress={(e) => e.key === "Enter" && this.handleTagAdd(e)}
              />
              <div className="suggested-tags">
                {this.state.suggestedTags.map((tag, index) => (
                  <div
                    key={index}
                    className="suggested-tag"
                    onClick={() => this.handleSuggestionClick(tag)}
                  >
                    {tag}
                  </div>
                ))}
              </div>
            </div>

            <div className="added-tags">
              {this.state.newPost.tags.map((tag, index) => (
                <span key={index} className="tag-chip">
                  {tag}
                  <span
                    className="remove-tag-chip"
                    onClick={() => this.handleTagRemove(tag)}
                  >
                    &times;
                  </span>
                </span>
              ))}
            </div>

            <button type="submit" className="submit-button">
              Create Post
            </button>
          </form>
        </div>
      </div>
    );
  }
}

export default withNavigation(CreateCard);
