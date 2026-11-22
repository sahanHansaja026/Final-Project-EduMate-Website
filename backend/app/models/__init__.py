"""EduMate database models package.

Importing the models here ensures every declarative model is registered on the
centralized SQLAlchemy metadata before any mapper or engine is used.
"""

from app.models.assignment import Assignment
from app.models.assignment_edit_access import AssignmentEditAccess
from app.models.assignment_grade_access import AssignmentGradeAccess
from app.models.assignment_grading import AssignmentGrading
from app.models.assignment_module_grade import AssignmentModuleGrade
from app.models.assignment_submission import AssignmentSubmission
from app.models.assignment_view_access import AssignmentViewAccess
from app.models.authorized_student import AuthorizedStudent
from app.models.channel import Channel, ChannelVisibilityEnum
from app.models.channel_analytics import ChannelAnalytics
from app.models.channel_content_access_controller import ChannelContentAccessController
from app.models.channel_module_access_controller import ChannelModuleAccessController
from app.models.channel_modules import ChannelModule, VisibilityEnum
from app.models.content import Content
from app.models.enrollment import Enrollment
from app.models.enrollment_analytics import EnrollmentAnalytics
from app.models.grade import Grade
from app.models.manual_grading import ManualGrading
from app.models.meeting import Meeting
from app.models.meeting_message import Message
from app.models.module import Module, VisibilityEnum
from app.models.module_quiz_access_controller import ModuleQuizAccessController
from app.models.module_quota import ModuleQuota
from app.models.profile import Profile, PushNotificationEnum
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.quiz import Quiz
from app.models.quiz_attempt_controller import QuizAttemptController
from app.models.quiz_score import QuizScore
from app.models.score_management import ScoreManagement
from app.models.sentiment import SentimentAnalysis
from app.models.student_answer import StudentAnswer
from app.models.subscription import PlanEnum, Subscription
from app.models.subscription_payment import PlanEnum, SubscriptionPayment
from app.models.user import User
from app.models.user_comments import UserComment
from app.models.video import Video
from app.models.video_access_control import VideoAccessControl
from app.models.video_quota import VideoQuota
