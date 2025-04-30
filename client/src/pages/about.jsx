import React, { Component } from "react";
import "../css/about.css";
import wellcome from "../images/Welcome.png";
import Goal from "../images/goal.png";
import Movies from "../images/movie.png";
import Community from "../images/community.png";
import Vison from "../images/vison.png";
import Mark from "../images/mark.png";
import heroimage from "../images/test.png";

export default class About extends Component {
  render() {
    return (
      <div className="abouts">
        <div className="hero">
          <div className="herotext">
            <h1>Welcome</h1>
            <h2>ModuleMate</h2>
            <h4>
              "Reflects the idea of a global education space where everyone can
              learn."
            </h4>
          </div>
          <div className="heroimage">
            <img src={heroimage} alt="Example" />
          </div>
        </div>
        <div className="box2">
          <div className="subbox1">
            <h2>Welcome to ModuleMate!</h2>
            <p>
              ModuleMate is your ultimate platform for learning and growth.
              Whether you're here to create engaging courses, explore new
              subjects, or participate in interactive activities, this is the
              perfect place for you. Get ready to expand your knowledge and
              enjoy a seamless educational experience!
            </p>
          </div>
          <div className="subbox2">
            <img src={wellcome} alt="Background" />
          </div>
        </div>
        <br />
        <div className="box3">
          <div className="subbox2">
            <img src={Goal} alt="Background" />
          </div>
          <div className="subbox1">
            <h2>Our Mission</h2>
            <p>
              At ModuleMate, our mission is to empower learners and educators by
              providing an engaging platform for creating and exploring courses.
              We aim to foster a love for learning by offering interactive
              activities, quizzes, and resources. Whether you're here to teach
              or to learn, our goal is to make the educational journey
              enjoyable, accessible, and rewarding for everyone.
            </p>
          </div>
        </div>
        <br />
        <div className="box3">
          <div className="subbox1">
            <h2>What We Offer</h2>
            <ul class="a">
              <li>
                <b>Interactive Courses:-</b>
                <i>
                  We offer a variety of courses with engaging content, including
                  videos, assignments, and quizzes, designed to make learning
                  interactive and enjoyable.
                </i>
              </li>
              <br />
              <li>
                <b>Collaborative Learning:-</b>
                Join a global community of learners and educators, collaborate
                on activities, share insights, and grow together in a supportive
                learning environment.
              </li>
              <br />
              <li>
                <b>Custom Modules:-</b>
                Create your own learning modules, tailor them to your interests
                or needs, and share them with others for a personalized
                educational experience.
              </li>
            </ul>
          </div>
          <div className="subbox3">
            <img src={Movies} alt="Background" />
          </div>
        </div>
        <br />
        <center>
          <div className="add_sence">Google Ads</div>
        </center>
        <br />
        <div className="box2">
          <div className="subbox1">
            <h2>Join Our Community</h2>
            <p>
              Become a part of the ModuleMate community and connect with
              passionate learners and educators! By joining, you'll gain access
              to engaging courses, interactive activities, and collaborative
              learning opportunities. Share your progress, collaborate with
              peers, and be a part of a growing global network of knowledge
              seekers. Sign up today and transform your learning experience with
              ModuleMate!
            </p>
          </div>
          <div className="subbox2">
            <img src={Community} alt="Background" />
          </div>
        </div>
        <br />
        <div className="box3">
          <div className="subbox4">
            <img src={Vison} alt="Background" />
          </div>
          <div className="subbox1">
            <h2>Our Vision</h2>
            <p>
              At ModuleMate, our vision is to become the premier platform for
              interactive learning and knowledge-sharing. We aspire to inspire a
              global community of curious learners and dedicated educators,
              fostering a passion for education through engaging courses and
              collaborative activities. We envision a world where learning is
              accessible, enjoyable, and empowering for everyone, everywhere.
            </p>
          </div>
        </div>
        <br />
        <center>
          <div className="mark">
            <img src={Mark} alt="Background" />
          </div>
          <div className="mark">
            <p>
              ModuleMate is proudly powered by MARK Technologies, delivering a
              seamless and reliable educational experience for all our users.
            </p>
          </div>
        </center>
        <center>
          <div className="add_sence">Google Ads</div>
        </center>
        <br />
      </div>
    );
  }
}
