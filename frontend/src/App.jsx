import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage } from './pages/LoginPage';
import { SignupPage } from './pages/SignupPage';
import { OverviewPage } from './pages/OverviewPage';
import { ProductsPage } from './pages/ProductsPage';
import { IntegrationPage } from './pages/IntegrationPage';
import { ProfilePage } from './pages/ProfilePage';
import { NewsPage } from './pages/NewsPage';
import { TrendPage } from './pages/TrendPage';
import { ReportsPage } from './pages/ReportsPage';
import { useAuth } from './context/AuthContext';

function App() {
  const { user } = useAuth();

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={!user ? <LoginPage /> : <Navigate to="/dashboard" />} />
        <Route path="/signup" element={!user ? <SignupPage /> : <Navigate to="/dashboard" />} />
        
        {/* Korumalı Route: Giriş yapmayan dashboard'u göremez */}
        <Route path="/dashboard" element={user ? <OverviewPage /> : <Navigate to="/login" />} />
        <Route path="/products" element={user ? <ProductsPage /> : <Navigate to="/login" />} />
        <Route path="/integration" element={user ? <IntegrationPage /> : <Navigate to="/login" />} />
        <Route path="/haber" element={user ? <NewsPage /> : <Navigate to="/login" />} />
        <Route path="/reports" element={user ? <ReportsPage /> : <Navigate to="/login" />} />
        <Route path="/trend" element={user ? <TrendPage /> : <Navigate to="/login" />} />
        <Route path="/profile" element={user ? <ProfilePage /> : <Navigate to="/login" />} />
        
        <Route path="/" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;