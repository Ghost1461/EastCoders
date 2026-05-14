import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage } from './pages/LoginPage';
import { SignupPage } from './pages/SignupPage';
import { useAuth } from './context/AuthContext';

function App() {
  const { user } = useAuth();

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={!user ? <LoginPage /> : <Navigate to="/dashboard" />} />
        <Route path="/signup" element={!user ? <SignupPage /> : <Navigate to="/dashboard" />} />
        
        {/* Korumalı Route: Giriş yapmayan dashboard'u göremez */}
        <Route path="/dashboard" element={user ? <div>Hoş geldin, {user.full_name}</div> : <Navigate to="/login" />} />
        
        <Route path="/" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;