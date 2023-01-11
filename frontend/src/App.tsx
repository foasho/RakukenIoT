import React from 'react';
import { Route, BrowserRouter, Routes } from "react-router-dom"
import logo from './logo.svg';
import styles from "./App.module.scss";
import { HeaderComponent } from './components/commons/Header';
import { HomeComponent } from './components/pages/Home';

/**
 * ページ一覧
 *  /:home
 *  /:docs
 *  /:github
 */

function App() {
  return (
    <div className={styles.appMain}>
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<HomeComponent/>}></Route>npm
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
