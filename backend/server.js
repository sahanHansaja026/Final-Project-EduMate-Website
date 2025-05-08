const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const bodyParser = require("body-parser");
const path = require("path");

//import router files
const authRouter = require("./routes/student");
const ProfileRouter = require("./routes/profile");
const CardRouter = require("./routes/card");
const AssignmentRouter = require("./routes/assignment");
const VideoRouter = require("./routes/fireassignment");
const GetmoduledeatailsRouter = require("./routes/getassigments");
const SerachRouter = require("./routes/search");
const NoteRouter = require("./routes/notes");
const Createquiz = require("./routes/create_quiz");
const SaveQuestionRouter = require("./routes/question");
const ScoreRoute = require("./routes/score");
const EnrolleStudents = require("./routes/enrolle");
const cmsRoute = require("./routes/CMS");
const CMSSaveRoute = require("./routes/savecms");
const UserCountRoute = require("./routes/usercount");
const PogressRoute = require("./routes/progress");
const ChenalCreateRoute = require("./routes/create_chanel");
const ChenalModule = require("./routes/chanelmodule");
const Analytics = require("./routes/dashboard");
const TagSearch = require("./routes/tagsearch");
const Subscribers = require("./routes/subscriber");
const Subscripion = require("./routes/subscription");
const Message = require("./routes/message");
const FireVideo = require("./routes/firevedio");
const Articals_d = require("./routes/artical");
const CMSGet = require("./routes/getCMS");
const GradeCMS = require("./routes/grageCMS");

const app = express();
const PORT = process.env.PORT || 9001;

//middleware

app.use(cors());
app.use(bodyParser.json());

// route middleware
app.use(ProfileRouter);
app.use(CardRouter);
app.use(AssignmentRouter);
app.use(VideoRouter);
app.use(GetmoduledeatailsRouter);
app.use(SerachRouter);
app.use(NoteRouter);
app.use(Createquiz);
app.use(SaveQuestionRouter);
app.use(ScoreRoute);
app.use(EnrolleStudents);
app.use(cmsRoute);
app.use(CMSSaveRoute);
app.use(UserCountRoute);
app.use(PogressRoute);
app.use(Analytics);
app.use(TagSearch);
app.use(Subscribers);
app.use(Message);
app.use(FireVideo);
app.use(Articals_d);
app.use(CMSGet);
app.use(GradeCMS);

//for chanel
app.use(ChenalCreateRoute);
app.use(ChenalModule);
app.use(Subscripion);

// server.js or the relevant file
app.use("/Uploads", express.static(path.join(__dirname, "Uploads")));
app.use("/Profileimge", express.static(path.join(__dirname, "Profile")));
app.use("/Assignmentfile", express.static(path.join(__dirname, "Assignments")));
app.use("/VideoFile", express.static(path.join(__dirname, "Vedios")));
app.use("/NotesFile", express.static(path.join(__dirname, "Notes")));
app.use("/ChenalsFile", express.static(path.join(__dirname, "chenals")));
mongoose
  .connect(
    "mongodb+srv://sahanhansaja026:GskrGiGY06A71N7Y@cluster0.y3y7q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    }
  )
  .then(() => {
    console.log("connected to mongodb successfully");

    app.listen(PORT, () => {
      console.log(`server is running on port ${PORT}`);
    });
  })
  .catch((err) => console.error("Failed to connect to MongoDB", err));
app.use("/api/auth", authRouter);
