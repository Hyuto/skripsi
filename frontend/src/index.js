import React from "react";
import ReactDOM from "react-dom";
import "@fontsource/montserrat";
import "@fontsource/merriweather";
import "./style/normalize.css";
import "./style/style.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById("root")
);

reportWebVitals();
