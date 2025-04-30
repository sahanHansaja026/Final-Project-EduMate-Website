import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "../css/item.css";

// Importing images if they are in src folder
import AssignmentImage from "../images/Task.gif";
import CMSImage from "../images/Editing body text.gif";
import QuizImage from "../images/Online test.gif";
import VideoImage from "../images/Online learning.gif";
import NoteImage from "../images/Writer's block.gif";

const AddPage = ({ setCardId }) => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [selectedAction, setSelectedAction] = useState("add_assignment");

  useEffect(() => {
    if (setCardId) {
      setCardId(id);
    }
  }, [id, setCardId]);

  // Navigation handlers
  const handleCreateActivity1 = () => {
    navigate(`/add_assingment/${id}`);
  };
  const handleCreateActivity2 = () => {
    navigate(`/add_quiz/${id}`);
  };
  const handleCreateActivity3 = () => {
    navigate(`/add_vedio/${id}`);
  };
  const handleCreateActivity4 = () => {
    navigate(`/add_note/${id}`);
  };
  const handleCreateActivity5 = () => {
    navigate(`/add_cms/${id}`);
  };
  const handleCreateActivity6 = () => {
    navigate(`/notewritting/${id}`)
  }

  // Function to render content based on selected action
  const renderContent = () => {
    switch (selectedAction) {
      case "add_assignment":
        return (
          <div className="additmebox">
            <img
              src={AssignmentImage}
              alt="Assignment"
              className="action-image"
            />
            <div className="addbuttonbox">
              <p>
                An Assignment is a task designed to assess understanding of a
                topic or concept. It can take the form of essays, problem sets,
                projects, or other creative tasks. Assignments are valuable
                tools for evaluating the application of learned material and for
                guiding the learning process. They can be set with deadlines,
                instructions, and grading criteria, providing structure and
                clarity to the task at hand..
              </p>
              <br />

              <button
                className="btn btn-succes"
                onClick={handleCreateActivity1}
              >
                <i className="fa fa-plus"></i>&nbsp;Create
              </button>
            </div>
          </div>
        );
      case "add_cms":
        return (
          <div className="additmebox">
            <img src={CMSImage} alt="CMS" className="action-image" />
            <div className="addbuttonbox">
              <p>
                A Content Management System (CMS) is a platform that allows for
                easy organization, uploading, and sharing of materials like
                assignments, readings, and videos. With a CMS, there is no need
                for technical skills to manage content. The system makes it
                simple to create, modify, and distribute content, ensuring it is
                accessible at any time. It streamlines communication and keeps
                materials organized in one place, making it easier to manage and
                access important resources.
              </p>
              <br />
              <button
                className="btn btn-succes"
                onClick={handleCreateActivity5}
              >
                <i className="fa fa-plus"></i>&nbsp;Create
              </button>
            </div>
          </div>
        );
      case "add_quiz":
        return (
          <div className="additmebox">
            <img src={QuizImage} alt="Quiz" className="action-image" />
            <div className="addbuttonbox">
              <p>
                A Quiz is a tool used to assess understanding of the material.
                By creating quizzes, it's easy to evaluate how well the key
                concepts are grasped and identify areas that need further
                attention. Quizzes can include various question types, such as
                multiple-choice, true/false, or short-answer questions,
                providing a diverse approach to testing knowledge. They are
                ideal for both formative assessments and final evaluations,
                helping to reinforce learning and improve retention.
              </p>
              <br />
              <button
                className="btn btn-succes"
                onClick={handleCreateActivity2}
              >
                <i className="fa fa-plus"></i>&nbsp;Create
              </button>
            </div>
          </div>
        );
      case "add_video":
        return (
          <div className="additmebox">
            <img src={VideoImage} alt="Video" className="action-image" />
            <div className="addbuttonbox">
              <p>
                Educational Videos are a great way to explain complex concepts
                visually and audibly. They can supplement lessons, making them
                more engaging and easier to understand. Videos are particularly
                useful for demonstrating practical applications, showing
                experiments, or simplifying abstract ideas. This medium enhances
                the learning experience by catering to different learning styles
                and offering a flexible way to present information.
              </p>
              <br />
              <button
                className="btn btn-succes"
                onClick={handleCreateActivity3}
              >
                <i className="fa fa-plus"></i>&nbsp;Create
              </button>
            </div>
          </div>
        );
      case "add_note":
        return (
          <div className="additmebox">
            <img src={NoteImage} alt="Lecture Note" className="action-image" />
            <div className="addbuttonbox">
              <p>
                Lecture Notes are summaries of key concepts discussed during a
                lesson. These notes help organize and record important
                information, making it easier to review and study. They can
                include bullet points, diagrams, or additional resources to
                support understanding. Lecture notes serve as an efficient
                reference tool, ensuring that nothing important is missed and
                making study sessions more productive.
              </p>
              <br />
              <button
                className="btn btn-succes"
                onClick={handleCreateActivity4}
              >
                <i className="fa fa-plus"></i>&nbsp;Create
              </button>
            </div>
          </div>
        );
      case "notewritting":
        return (
          <div className="additmebox">
            <img src={NoteImage} alt="Lecture Note" className="action-image" />
            <div className="addbuttonbox">
              <p>
                Lecture Notes are summaries of key concepts discussed during a
                lesson. These notes help organize and record important
                information, making it easier to review and study. They can
                include bullet points, diagrams, or additional resources to
                support understanding. Lecture notes serve as an efficient
                reference tool, ensuring that nothing important is missed and
                making study sessions more productive.
              </p>
              <br />
              <button
                className="btn btn-succes"
                onClick={handleCreateActivity6}
              >
                <i className="fa fa-plus"></i>&nbsp;Create
              </button>
            </div>
          </div>
        );
      default:
        return <p>Please select an action from the sidebar.</p>;
    }
  };

  return (
    <div className="addingpage">
      {/* Sidebar */}
      <div className="addsidebar">
        <ul>
          <li>
            <button
              className={`sidebar-link ${
                selectedAction === "add_assignment" ? "active" : ""
              }`}
              onClick={() => setSelectedAction("add_assignment")}
            >
              Add Assignment
            </button>
          </li>
          <li>
            <button
              className={`sidebar-link ${
                selectedAction === "add_cms" ? "active" : ""
              }`}
              onClick={() => setSelectedAction("add_cms")}
            >
              Add CMS
            </button>
          </li>
          <li>
            <button
              className={`sidebar-link ${
                selectedAction === "add_quiz" ? "active" : ""
              }`}
              onClick={() => setSelectedAction("add_quiz")}
            >
              Add Quiz
            </button>
          </li>
          <li>
            <button
              className={`sidebar-link ${
                selectedAction === "add_video" ? "active" : ""
              }`}
              onClick={() => setSelectedAction("add_video")}
            >
              Add Video
            </button>
          </li>
          <li>
            <button
              className={`sidebar-link ${
                selectedAction === "add_note" ? "active" : ""
              }`}
              onClick={() => setSelectedAction("add_note")}
            >
              Add Lecture Note
            </button>
          </li>
          <li>
            <button
              className={`sidebar-link ${
                selectedAction === "notewritting" ? "active" : ""
              }`}
              onClick={() => setSelectedAction("notewritting")}
            >
              notewritting
            </button>
          </li>
        </ul>
      </div>

      {/* Main Content */}
      <div className="item">{renderContent()}</div>
    </div>
  );
};

export default AddPage;
