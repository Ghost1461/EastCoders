import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import { LoginPage } from './pages/LoginPage';
import { SignupPage } from './pages/SignupPage';
import { OverviewPage } from './pages/OverviewPage';
import { ProductsPage } from './pages/ProductsPage';
import { IntegrationPage } from './pages/IntegrationPage';
import { ProfilePage } from './pages/ProfilePage';
import { NewsPage } from './pages/NewsPage';
import { TrendPage } from './pages/TrendPage';
import { AdminPage } from './pages/AdminPage';
import { useAuth } from './context/AuthContext';

function App() {
  const { user } = useAuth();

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={!user ? <LoginPage /> : <Navigate to={user.role === 'admin' ? "/admin" : "/dashboard"} />} />
        <Route path="/signup" element={!user ? <SignupPage /> : <Navigate to={user.role === 'admin' ? "/admin" : "/dashboard"} />} />
        
        {/* Korumalı Route: Admin normal sayfalara, normal kullanıcı admin sayfasına giremez */}
        <Route path="/dashboard" element={user ? (user.role === 'admin' ? <Navigate to="/admin" /> : <OverviewPage />) : <Navigate to="/login" />} />
        <Route path="/products" element={user ? (user.role === 'admin' ? <Navigate to="/admin" /> : <ProductsPage />) : <Navigate to="/login" />} />
        <Route path="/integration" element={user ? (user.role === 'admin' ? <Navigate to="/admin" /> : <IntegrationPage />) : <Navigate to="/login" />} />
        <Route path="/haber" element={user ? (user.role === 'admin' ? <Navigate to="/admin" /> : <NewsPage />) : <Navigate to="/login" />} />
        <Route path="/trend" element={user ? (user.role === 'admin' ? <Navigate to="/admin" /> : <TrendPage />) : <Navigate to="/login" />} />
        <Route path="/profile" element={user ? (user.role === 'admin' ? <Navigate to="/admin" /> : <ProfilePage />) : <Navigate to="/login" />} />
        
        {/* Admin Route */}
        <Route path="/admin" element={user ? (user.role === 'admin' ? <AdminPage /> : <Navigate to="/dashboard" />) : <Navigate to="/login" />} />
        
        <Route path="/" element={!user ? <LandingPage /> : <Navigate to={user.role === 'admin' ? "/admin" : "/dashboard"} />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;