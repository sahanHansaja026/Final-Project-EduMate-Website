import React, { Component } from "react";
import axios from "axios";
import { withNavigation } from "../utils/withNavigation";
import authService from "../services/authService";
import { v4 as uuidv4 } from "uuid";
import "../css/chenalinput.css";
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
        chenal_id: "",
        image: null,
      },
      userEmail: "",
      errorMessage: "",
      imagePreview: defaultImage,
    };
    this.fileInputRef = React.createRef();
    this.textareaRef = React.createRef(); // Reference for textarea
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
      .get("http://localhost:9001/ch")
      .then((res) => {
        if (res.data.success) {
          this.setState({ posts: res.data.existingPosts });
        } else {
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

    if (file) {
      const maxSizeInMB = 2;
      const maxFileSize = maxSizeInMB * 1024 * 1024;

      if (file.size > maxFileSize) {
        this.setState({
          errorMessage: `File size should be less than ${maxSizeInMB} MB.`,
        });
        return;
      }

      this.setState({
        newPost: {
          ...this.state.newPost,
          image: file,
        },
        imagePreview: URL.createObjectURL(file),
        errorMessage: "",
      });
    }
  };

  handleSubmit = (event) => {
    event.preventDefault();

    const { title, summery, image } = this.state.newPost;
    if (!title || !summery || !image) {
      this.setState({ errorMessage: "Please fill in all required fields." });
      return;
    }

    const newPostId = uuidv4();
    const formData = new FormData();
    formData.append("id", newPostId);
    formData.append("chenal_id", newPostId);
    formData.append("email", this.state.userEmail);
    formData.append("title", title);
    formData.append("summery", summery);
    formData.append("image", image);

    axios
      .post("http://localhost:9001/chanel/save", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((res) => {
        if (res.data.success) {
          this.setState({
            newPost: { id: "", title: "", summery: "", image: null },
            imagePreview: defaultImage,
          });
          this.retrievePosts();
          this.props.navigate(`/dashboard/mychenal`);
        } else {
          this.setState({ errorMessage: res.data.error });
        }
      })
      .catch((error) => {
        console.error("Error adding post:", error);
        this.setState({ errorMessage: "Error adding post." });
      });
  };

  handleImageClick = () => {
    this.fileInputRef.current.click();
  };

  // Function to auto-adjust textarea height
  handleTextareaChange = () => {
    const textarea = this.textareaRef.current;
    textarea.style.height = "auto"; // Reset the height
    textarea.style.height = `${textarea.scrollHeight}px`; // Adjust the height
  };

  render() {
    return (
      <div>
        <h1>Create Your Own Channel</h1>
        <center>
          <div className="input_sub1">
            <div className="container">
              <form onSubmit={this.handleSubmit}>
                {this.state.errorMessage && (
                  <div className="error-message">{this.state.errorMessage}</div>
                )}
                <div className="cardshowimage" onClick={this.handleImageClick}>
                  <img src={this.state.imagePreview} alt="Image Preview" />
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
                <div className="box">
                  <label>
                    <input
                      type="text"
                      name="title"
                      value={this.state.newPost.title}
                      placeholder="Title"
                      onChange={this.handleChange}
                      required
                    />
                  </label>
                </div>
                <label>
                  <textarea
                    name="summery"
                    value={this.state.newPost.summery}
                    onChange={(event) => {
                      this.handleChange(event);
                      this.handleTextareaChange(); // Resize textarea
                    }}
                    placeholder="Add Summary about your channel"
                    ref={this.textareaRef}
                    required
                  />
                </label>
                <button type="submit">Create Channel</button>
              </form>
            </div>
          </div>
        </center>
      </div>
    );
  }
}

// eslint-disable-next-line react-refresh/only-export-components
export default withNavigation(CreateCard);
