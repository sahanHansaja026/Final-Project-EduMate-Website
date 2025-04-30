import React from "react";
import "../css/footer.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faFacebookF,
  faTwitter,
  faInstagram,
  faLinkedinIn,
} from "@fortawesome/free-brands-svg-icons";
import {
  faLaptopCode,
  faMobileAlt,
  faCloud,
  faHeadset,
  faMapMarkerAlt,
  faPhoneAlt,
  faEnvelope,
} from "@fortawesome/free-solid-svg-icons";

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-section about">
          <h2>About Us</h2>
          <p>
            At ModuleMate, we’re dedicated to making education accessible and
            engaging for everyone. Our platform allows learners and educators to
            create, share, and explore knowledge through interactive courses and
            activities. Join us in transforming education into a collaborative
            and exciting journey!
          </p>
          <div className="social-icons">
            <a href="#">
              <FontAwesomeIcon icon={faFacebookF} />
            </a>
            <a href="#">
              <FontAwesomeIcon icon={faTwitter} />
            </a>
            <a href="#">
              <FontAwesomeIcon icon={faInstagram} />
            </a>
            <a href="#">
              <FontAwesomeIcon icon={faLinkedinIn} />
            </a>
          </div>
        </div>

        <div className="footer-section services">
          <h2>Services</h2>
          <ul>
            <li>
              <FontAwesomeIcon icon={faLaptopCode} />{" "}
              <a href="#">Web Development</a>
            </li>
            <li>
              <FontAwesomeIcon icon={faMobileAlt} /> <a href="">Mobile Apps</a>
            </li>
            <li>
              <FontAwesomeIcon icon={faCloud} /> <a href="#">Cloud Services</a>
            </li>
            <li>
              <FontAwesomeIcon icon={faHeadset} /> <a href="#">IT Consulting</a>
            </li>
          </ul>
        </div>

        <div className="footer-section contact">
          <h2>Contact Us</h2>
          <ul>
            <li>
              <FontAwesomeIcon icon={faMapMarkerAlt} /> Mathugama, Sri Lanka,
              Country
            </li>
            <li>
              <FontAwesomeIcon icon={faPhoneAlt} /> +94 71 77 35 442
            </li>
            <li>
              <FontAwesomeIcon icon={faEnvelope} /> hansajasahan50@gmail.com
            </li>
          </ul>
        </div>

        <div className="footer-section newsletter">
          <h2>Newsletter</h2>
          <p>Subscribe to our newsletter for the latest updates and offers.</p>
        </div>
      </div>

      <div className="bottom-bar">
        <a href="https://sahan026.github.io/portfolio/">
          &copy; 2024 MARK Techenologies |
        </a>{" "}
        <a href="#">Privacy Policy</a> | <a href="#">Terms of Service</a>
      </div>
    </footer>
  );
};

export default Footer;
