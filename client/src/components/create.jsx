import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom"; 
import axios from "axios";
import "../css/question.css";

// AddPage component for quiz_id
const AddPage = ({ setQuizId }) => {
  const { id, quizId } = useParams(); // Get both card_id (id) and quiz_id from URL

  useEffect(() => {
    if (setQuizId) {
      setQuizId(quizId);  // Set quizId using the prop passed from parent
    }
  }, [quizId, setQuizId]);
  const quiz_id=quizId;

  return (
    <div>
      <h1>Add Page</h1>
      <p>Your unique quiz ID is: {quizId}</p>  {/* Display the quizId */}
    </div>
  );
};

// Create a wrapper component for AddPage
const AddPageWrapper = ({ setQuizId }) => {
  return <AddPage setQuizId={setQuizId} />;
};

// Function to create a wrapper for the class component
const withNavigate = (WrappedComponent) => {
  return (props) => {
    const navigate = useNavigate();
    return <WrappedComponent {...props} navigate={navigate} />;
  };
};

class CreatePost extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      posts: [],
      newPost: {
        quiz_id: "",  // Changed card_id to quiz_id
        question: "",
        answer_1: "",
        answer_2: "",
        answer_3: "",
        answer_4: "",
        correct_answer: "",
      },
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleRadioChange = this.handleRadioChange.bind(this);
    this.setQuizId = this.setQuizId.bind(this);
    this.handleQuizButtonClick = this.handleQuizButtonClick.bind(this);
  }


  setQuizId(id) {
    this.setState((prevState) => ({
      newPost: {
        ...prevState.newPost,
        quiz_id: id,  // Set quiz_id instead of card_id
      },
    }));
  }

  handleChange(event) {
    const { name, value } = event.target;
    this.setState((prevState) => ({
      newPost: {
        ...prevState.newPost,
        [name]: value,
      },
    }));
  }

  handleRadioChange(event) {
    this.setState({
      newPost: {
        ...this.state.newPost,
        correct_answer: event.target.value,
      },
    });
  }

  handleSubmit(event) {
    event.preventDefault();
    axios
      .post("http://localhost:9001/question/save", this.state.newPost)
      .then((res) => {
        if (res.data.success) {
          console.log("Post added successfully");
          this.setState({
            newPost: {
              quiz_id: "",  // Reset quiz_id
              question: "",
              answer_1: "",
              answer_2: "",
              answer_3: "",
              answer_4: "",
              correct_answer: "",
            },
          });
          window.location.reload();
        } else {
          console.error("Error adding post:", res.data.error);
        }
      })
      .catch((error) => {
        console.error("Error adding post:", error);
      });
  }

  handleQuizButtonClick() {
    const { newPost } = this.state;
    if (newPost.quiz_id) {
      this.props.navigate(`/curds/${newPost.quiz_id}`);  // Navigate using quiz_id
    } else {
      console.error("Quiz ID is not defined.");
    }
  }

  render() {
    return (
      <div className="show">
        <center>
          <div className="container1">
            <div className="content">
              <AddPageWrapper setQuizId={this.setQuizId} />
              <form onSubmit={this.handleSubmit}>
                <div className="title">Add Question Details</div>
                <br />
                <label>
                  Question Text :
                  <textarea
                    type="text"
                    name="question"
                    value={this.state.newPost.question}
                    onChange={this.handleChange}
                  />
                </label>
                <br />
                <label>
                  Answer 1 :
                  <input
                    type="text"
                    name="answer_1"
                    value={this.state.newPost.answer_1}
                    onChange={this.handleChange}
                  />
                </label>
                <br />
                <label>
                  Answer 2 :
                  <input
                    type="text"
                    name="answer_2"
                    value={this.state.newPost.answer_2}
                    onChange={this.handleChange}
                  />
                </label>
                <br />
                <label>
                  Answer 3 :
                  <input
                    type="text"
                    name="answer_3"
                    value={this.state.newPost.answer_3}
                    onChange={this.handleChange}
                  />
                </label>
                <br />
                <label>
                  Answer 4 :
                  <input
                    type="text"
                    name="answer_4"
                    value={this.state.newPost.answer_4}
                    onChange={this.handleChange}
                  />
                </label>
                <br />
                <label>Select the Correct Answer:</label>
                <div>
                  <input
                    type="radio"
                    name="correct_answer"
                    value={this.state.newPost.answer_1}
                    checked={this.state.newPost.correct_answer === this.state.newPost.answer_1}
                    onChange={this.handleRadioChange}
                  />
                  {this.state.newPost.answer_1}
                </div>
                <div>
                  <input
                    type="radio"
                    name="correct_answer"
                    value={this.state.newPost.answer_2}
                    checked={this.state.newPost.correct_answer === this.state.newPost.answer_2}
                    onChange={this.handleRadioChange}
                  />
                  {this.state.newPost.answer_2}
                </div>
                <div>
                  <input
                    type="radio"
                    name="correct_answer"
                    value={this.state.newPost.answer_3}
                    checked={this.state.newPost.correct_answer === this.state.newPost.answer_3}
                    onChange={this.handleRadioChange}
                  />
                  {this.state.newPost.answer_3}
                </div>
                <div>
                  <input
                    type="radio"
                    name="correct_answer"
                    value={this.state.newPost.answer_4}
                    checked={this.state.newPost.correct_answer === this.state.newPost.answer_4}
                    onChange={this.handleRadioChange}
                  />
                  {this.state.newPost.answer_4}
                </div>
                <br />
                <button type="submit">Store in the system</button>
              </form>
            </div>
            <button className="quiz-button" onClick={this.handleQuizButtonClick}>
              Preview
            </button>
          </div>
        </center>
      </div>
    );
  }
}

// Wrap CreatePost with withNavigate to pass navigate as a prop
export default withNavigate(CreatePost);
