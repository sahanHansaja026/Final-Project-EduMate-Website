import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import authService from "../../services/authService";
import "../../css/curd.css";

const ShowQuizScore = () => {
    const { card_id } = useParams();
    const [email, setEmail] = useState("");
    const [scores, setScores] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const userData = await authService.getUserData();
                setEmail(userData.email);
            } catch (err) {
                console.error("Failed to fetch user data", err);
            }
        };

        fetchUserData();
    }, []);

    useEffect(() => {
        const fetchScores = async () => {
            try {
                const response = await axios.get(`http://localhost:9001/activities/${card_id}`);
                const { posts } = response.data;
                const activities = Array.isArray(posts) ? posts : [];

                const updatedScores = await Promise.all(
                    activities.map(async (item) => {
                        let type = "";
                        let name = "";
                        let id = "";
                        let score = "NA";

                        try {
                            if (item.quiz_name) {
                                type = "Quiz";
                                name = item.quiz_name;
                                id = item.quiz_id;
                                const quizId = id;
                                const res = await axios.get(`http://localhost:9001/getquizscore/${quizId}/${email}`);
                                const rawScore = res.data?.score;
                                score = !isNaN(rawScore) ? Number(rawScore) : "Not grated";
                            } else if (item.CMS_name) {
                                type = "CMS";
                                name = item.CMS_name;
                                id = item.CMS_id;
                                const CMS_id = id;
                                const res = await axios.get(`http://localhost:9001/getscore/${CMS_id}/${email}`);
                                const rawScore = res.data?.score;
                                score = !isNaN(rawScore) ? Number(rawScore) : "Not grated";
                            } else if (item.assignment_name) {
                                type = "Assignment";
                                name = item.assignment_name;
                                id = item.assignment_id;
                                score = "Not grated";
                            } else {
                                return null;
                            }
                        } catch (err) {
                            console.error("Score fetch error:", err);
                            score = "Error";
                        }

                        return {
                            _id: item._id,
                            type,
                            name,
                            id,
                            score,
                        };
                    })
                );

                setScores(updatedScores.filter((s) => s !== null));
            } catch (err) {
                console.error("Main fetch error:", err);
                setError("Failed to fetch scores");
            } finally {
                setLoading(false);
            }
        };

        if (email) {
            fetchScores();
        }
    }, [card_id, email]);

    const totalScore = scores.reduce((acc, curr) => {
        return acc + (typeof curr.score === "number" ? curr.score : 0);
    }, 0);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <div className="curd">
            <center>
                <h1>Quiz Score Board</h1>
                <p>{email}</p>
                <h3>Quiz ID: {card_id}</h3>
            </center>

            {scores.length === 0 ? (
                <p>No scores found for this quiz.</p>
            ) : (
                <center>
                    <table>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Type</th>
                                <th>Title</th>
                                <th>ID</th>
                                <th>Score</th>
                            </tr>
                        </thead>
                        <tbody>
                            {scores.map((scoreObj, index) => (
                                <tr key={scoreObj._id}>
                                    <td>{index + 1}</td>
                                    <td>{scoreObj.type}</td>
                                    <td>{scoreObj.name}</td>
                                    <td>{scoreObj.id}</td>
                                    <td>{scoreObj.score}</td>
                                </tr>
                            ))}
                            {/* Total Row */}
                            <tr style={{ fontWeight: "bold" }}>
                                <td colSpan="4" style={{ textAlign: "right" }}>∑ Course total</td>
                                <td>{totalScore}</td>
                            </tr>
                        </tbody>
                    </table>
                </center>
            )}
        </div>
    );
};

export default ShowQuizScore;
