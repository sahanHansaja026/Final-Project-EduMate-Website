// src/components/GiftCard.js
import React from "react";
import "../css/subcripionplane.css";

const Subscriptionplane = ({ closeModal }) => {
  return (
    <div className="subcribeplane-card-modal">
      <div className="subcribeplane-card-content">
        <h1>Upgrade Your Plan</h1>
        <div className="planemainbox">
          <button>Yearly (save 20%)</button>
          <div className="planeboxes">
            <div className="planebox">
              <div className="title">
                <h1>Free</h1>
                <p>Access basic features with limited usage</p>
              </div>
              <div className="pricebox">
                <h1>0$</h1>
                <p>lifelime subcribe</p>
              </div>
              <center>
                <button className="dissable">Current Plan</button>
              </center>
              <li>Access to any modules</li>
              <li>Enroll up to 25 students per channel</li>
              <li>Create 1 channel only</li>
              <li>Create up to 5 modules</li>
            </div>

            <div className="planebox">
              <div className="title">
                <h1>Pro</h1>
                <p>Unlock advance tools for enhancded productivity</p>
              </div>
              <div className="pricebox">
                <h1>10$</h1>
                <p>per yerly billed yearly</p>
              </div>
              <center>
                <button className="subcribe">Choose Pro</button>
              </center>
              <li>Access to all modules</li>
              <li>Enroll up to 100 students per channel</li>
              <li>Create up to 5 channels</li>
              <li>Unlimited modules</li>
              <li>Priority Email Support</li>
            </div>

            <div className="planebox">
              <div className="title">
                <h1>Premium</h1>
                <p>Get full access to all features for maximum flexibility</p>
              </div>
              <div className="pricebox">
                <h1>20$</h1>
                <p>per yerly billed yearly</p>
              </div>
              <center>
                <button className="choose">Choose Premium</button>
              </center>
              <li>Access to all modules</li>
              <li>Enroll unlimited students per channel</li>
              <li>Create unlimited channels</li>
              <li>Unlimited modules</li>
              <li>Priority Email Support</li>
              <li>One-on-One Mentorship</li>
            </div>
          </div>
        </div>

        <button onClick={closeModal}>Close</button>
      </div>
    </div>
  );
};

export default Subscriptionplane;
