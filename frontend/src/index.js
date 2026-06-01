/*!
=========================================================
* Argon Design System React - v1.1.2
=========================================================
*/

import React from "react";
import ReactDOM from "react-dom/client";
import {
  BrowserRouter,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";

import "assets/vendor/nucleo/css/nucleo.css";
import "assets/vendor/font-awesome/css/font-awesome.min.css";
import "assets/scss/argon-design-system-react.scss";

import Landing from "views/examples/Landing.js";
import Login from "views/examples/Login.js";
import Register from "views/examples/Register.js";
import Commute from "views/examples/Commute.js";
import Logs from "views/Logs.js";
import Badge from "views/examples/Badge.js";
import ThemeShop from "views/examples/ThemeShop.js";


// 로그인하지 않은 사용자를 /login으로 보냄
function PrivateRoute({ children }) {
  const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";

  if (!isLoggedIn) {
    return <Navigate to="/login" replace />;
  }

  return children;
}


const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <BrowserRouter>
    <Routes>
      <Route
        path="/"
        element={<Landing />}
      />

      <Route
        path="/login"
        element={<Login />}
      />

      <Route
        path="/register"
        element={<Register />}
      />

      <Route
        path="/commute"
        element={
          <PrivateRoute>
            <Commute />
          </PrivateRoute>
        }
      />

      <Route
        path="/logs"
        element={
          <PrivateRoute>
            <Logs />
          </PrivateRoute>
        }
      />

      <Route
        path="/badge"
        element={
          <PrivateRoute>
            <Badge />
          </PrivateRoute>
        }
      />

      <Route
        path="/theme-shop"
        element={
          <PrivateRoute>
            <ThemeShop />
          </PrivateRoute>
        }
      />

      <Route
        path="*"
        element={<Navigate to="/" replace />}
      />
    </Routes>
  </BrowserRouter>
);