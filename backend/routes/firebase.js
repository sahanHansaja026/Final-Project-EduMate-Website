// config/firebaseAdmin.js
const admin = require("firebase-admin");
const serviceAccount = require("../serviceAccountKey.json");

if (!admin.apps.length) {
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    storageBucket: "scurd-e749c.appspot.com",
  });
}

const bucket = admin.storage().bucket();

module.exports = { admin, bucket };
