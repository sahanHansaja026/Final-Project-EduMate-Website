import React, { useEffect } from "react";
import { useParams } from "react-router-dom"; 

const AddPage = ({ setCardId }) => {
  const { id } = useParams(); 
  useEffect(() => {
    if (setCardId) {
      setCardId(id); 
    }
  }, [id, setCardId]);

  return (
    <div>
      <h1>Add Page</h1>
      <p>Your unique post ID is: {id}</p> 
    </div>
  );
};

export default AddPage;
