// config/firebase.js
const admin = require("firebase-admin");
const serviceAccount = require("../backend/serviceAccountKey.json");

// Initialize Firebase Admin SDK with the service account key
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  storageBucket: "scurd-e749c.appspot.com", // Replace with your Firebase project ID
});

// Export Firebase Storage bucket reference
const bucket = admin.storage().bucket();

module.exports = { bucket };
