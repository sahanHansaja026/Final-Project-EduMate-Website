"use client";

import { useEffect, useState } from "react";
import { getUser } from "../../services/authService";

const HomePage = () => {
  const [user, setUser] = useState<{ id: number; email: string } | null>(null);

  useEffect(() => {
    const currentUser = getUser();
    setUser(currentUser);
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Home</h1>

      {user ? (
        <>
          <p>User ID: {user.id}</p>
          <p>Email: {user.email}</p>
        </>
      ) : (
        <p>No user logged in</p>
      )}
    </div>
  );
};

export default HomePage;
