import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';
import LoginPage from './LoginPage';
import SelectCalendarPage from './SelectCalendarPage';
import './App.scss';

const buttonStyle = {
  fontSize: 32,
  textAlign: 'center',
};

const headerStyle = {
  textAlign: 'center',
};

export function App() {
  const [userInfo, setUserInfo] = useState<string | any>(null);

  useEffect(() => {
    axios.get('/user').then((res) => {
      setUserInfo(res.data);
    });
  }, []);

  const isLoggedIn = userInfo && userInfo !== "Not logged in";

  return (
    <BrowserRouter>
      <div className="App">
        <Routes>
          <Route path="/" element={isLoggedIn ? <SelectCalendarPage isLoggedIn={isLoggedIn} userInfo={userInfo} /> : <LoginPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
