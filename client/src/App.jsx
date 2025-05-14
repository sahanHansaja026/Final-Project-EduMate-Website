import React from "react";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";

import Landing_Page from "./pages/landing_page";
import NavBar from "./components/navbar";
import Login from "./pages/login_page";
import Regestar from "./pages/register_page";
import Profile from "./pages/profile";
import Home from "./pages/home_page";
import Upgrade from "./pages/upgrade";
import Dashboard from "./pages/dashboard_page";
import Teacherweek from "./components/teacherweek";
import AddPage from "./components/Add";
import Assingment from "./components/assingment";
import Note from "./components/note";
import Video from "./components/video";
import Search from "./components/search";
import CreateQuiz from "./components/create_quiz";
import Create from "./components/create";
import Quiz from "./components/quiz";
import Score from "./components/score";
import EnrolleStudent from "./pages/enrolle";
import CMS from "./components/add_cms";
import WriteCms from "./components/CMS";
import Footer from "./components/footer";
import About from "./pages/about";
import SearchComponent from "./components/searchcomponent";
import Message from "./components/message";
import Notewritter from "./components/notewritting";
import VedioEdit from "./components/Editting/vedio";
import AssignmentEdit from "./components/Editting/assignments";
import ArticleEdit from "./components/articaledit";
import QuizEditCurd from "./components/Editting/quixedit";
import QuestionDeatils from "./components/questiondetails";
import QuestionEdit from "./components/Editting/questionedit";
import SettingsPage from "./components/settings";
import QuizGradeShow from "./components/grading/quizgrade";
import ChatBot from "./components/chatbot";
import CMSGrage from "./components/grading/CMSgrage";
import CMSShow from "./components/grading/CMSshow";
import AllStudents from "./components/grading/allstudent";
import MyGrades from "./components/grading/mygrade";

//for chenals
import ChenaHome from "./chanel/chenal_home";
import MOduleOwner from "./chanel/moduleowner";
import ChenalEnrollment from "./chanel/chenalenrollement";
import CheanelHome from "./chanel/chenal_home";
import Addstudents_and_teachers from "./chanel/addstudents_and_teachers";

const App = () => {
  const location = useLocation();

  const noNavBarPaths = ["/", "/login", "/registar", "/dashboard"];
  const noFooterPaths = ["/login", "/registar", "/dashboard"];

  const shouldShowFooter = !noFooterPaths.some((path) =>
    location.pathname.startsWith(path)
  );

  return (
    <div className="container">
      {!noNavBarPaths.includes(location.pathname) && <NavBar />}
      <Routes>
        <Route exact path="/" element={<Landing_Page />} />
        <Route exact path="/login" element={<Login />} />
        <Route path="/dashboard/*" element={<Dashboard />} />
        <Route exact path="/registar" element={<Regestar />} />
        <Route exact path="/profile" element={<Profile />} />
        <Route exact path="/home" element={<Home />} />
        <Route exact path="/search" element={<Search />} />
        <Route exact path="/searchcomponent" element={<SearchComponent />} />
        <Route exact path="/about" element={<About />} />
        <Route exact path="/teacherweek/:id" element={<Teacherweek />} />
        <Route exact path="/add/:id" element={<AddPage />} />
        <Route exact path="/add_assingment/:id" element={<Assingment />} />
        <Route exact path="/add_note/:id" element={<Note />} />
        <Route exact path="/add_vedio/:id" element={<Video />} />
        <Route exact path="/notewritting/:id" element={<Notewritter />} />
        <Route exact path="/add_quiz/:id" element={<CreateQuiz />} />
        <Route exact path="/add_cms/:id" element={<CMS />} />
        <Route exact path="/enrollestudent/:id" element={<EnrolleStudent />} />
        <Route exact path="/create/:quizId" element={<Create />} />
        <Route exact path="/quiz/:quizId" element={<Quiz />} />
        <Route exact path="/WriteCMS/:CMS_id" element={<WriteCms />} />
        <Route exact path="/score/:quizId" element={<Score />} />
        <Route exact path="/message/:id" element={<Message />} />
        <Route exact path="/upgrade" element={<Upgrade />} />
        <Route exact path="/vdiosedit/:video_id" element={<VedioEdit />} />
        <Route exact path="/quizedit/:quiz_id" element={<QuizEditCurd />} />
        <Route exact path="/getquestion/:_id" element={<QuestionDeatils />} />
        <Route exact path="/qedit/:_id" element={<QuestionEdit />} />
        <Route exact path="/settings/:card_id" element={<SettingsPage />} />
        <Route exact path="/chatbot" element={<ChatBot />} />
        <Route exact path="/corsegrade/:card_id" element={<AllStudents />} />
        <Route exact path="/mygrade/:card_id" element={<MyGrades />} />
        <Route
          exact
          path="/quizgradeview/:quiz_id"
          element={<QuizGradeShow />}
        />
        <Route exact path="/CMSgradeadd/:id" element={<CMSGrage />} />
        <Route exact path="/CMSgradeview/:CMS_id" element={<CMSShow />} />
        <Route
          exact
          path="/articaledit/:article_id"
          element={<ArticleEdit />}
        />
        <Route
          exact
          path="/assgnmentedit/:assignment_id"
          element={<AssignmentEdit />}
        />
        {/* for chenal */}
        <Route exact path="/chenalhome/:id" element={<ChenaHome />} />
        <Route exact path="/moduleowner/:id" element={<MOduleOwner />} />
        <Route
          exact
          path="/addstudent/:chenalId"
          element={<Addstudents_and_teachers />}
        />
        <Route
          exact
          path="/chenalenrollement/:id"
          element={<ChenalEnrollment />}
        />
        <Route exact path="/chenalhome/:id" element={<CheanelHome />} />
        <Route exact path="/vdiosedit/:video_id" element={<VedioEdit />} />
      </Routes>
      {shouldShowFooter && <Footer />}
    </div>
  );
};

// eslint-disable-next-line react-refresh/only-export-components
export default () => (
  <BrowserRouter>
    <App />
  </BrowserRouter>
);
