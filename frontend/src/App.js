import React from "react";
import { FaHome } from "react-icons/fa";
import * as style from "./style/layout.module.scss";
import Main from "./main/main";

const App = () => {
  return (
    <div className={style.showcase}>
      <header className={style.header}>
        <div className={style.title}>
          <h3>Showcase</h3>
          <a href="https://hyuto.github.io/" className={style.home}>
            <FaHome size={30} />
          </a>
        </div>
      </header>
      <main>
        <Main />
      </main>
      <footer className={style.footer}>
        <strong>© wahyu setianto {new Date().getFullYear()}</strong>, Built with
        {` `}
        React and {"\u2764"}
      </footer>
    </div>
  );
};

export default App;
