import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useLocation } from 'react-router-dom';
import api from '../api/client';
import './ProfilePage.css';

export const ProfilePage = () => {
    const { user, logout } = useAuth();
    const location = useLocation();

    const [formData, setFormData] = useState({
        full_name: user?.full_name || '',
        email: user?.email || '',
        phone_number: user?.phone_number || ''
    });
    const [isSaving, setIsSaving] = useState(false);

    useEffect(() => {
        if (user) {
            setFormData({
                full_name: user.full_name || '',
                email: user.email || '',
                phone_number: user.phone_number || ''
            });
        }
    }, [user]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleUpdateProfile = async () => {
        const payload = {};
        if (formData.full_name !== user?.full_name) payload.full_name = formData.full_name;
        if (formData.email !== user?.email) payload.email = formData.email;
        if (formData.phone_number !== user?.phone_number) payload.phone_number = formData.phone_number;

        if (Object.keys(payload).length === 0) {
            alert("Değişen bir bilgi yok.");
            return;
        }

        setIsSaving(true);
        try {
            await api.put('/profile/update', payload);
            alert("Profil başarıyla güncellendi!");
        } catch (error) {
            console.error("Profil güncelleme hatası:", error);
            alert(`Güncelleme başarısız: ${error.response?.data?.detail || error.message}`);
        } finally {
            setIsSaving(false);
        }
    };

    const [isPasswordFormVisible, setIsPasswordFormVisible] = useState(false);
    const [passwordData, setPasswordData] = useState({
        current_password: '',
        new_password: '',
        new_password_confirm: ''
    });
    const [isChangingPassword, setIsChangingPassword] = useState(false);

    const handlePasswordInputChange = (e) => {
        const { name, value } = e.target;
        setPasswordData(prev => ({ ...prev, [name]: value }));
    };

    const handleUpdatePassword = async () => {
        if (passwordData.new_password !== passwordData.new_password_confirm) {
            alert("Yeni şifreler birbiriyle eşleşmiyor!");
            return;
        }
        setIsChangingPassword(true);
        try {
            await api.put('/profile/change-password', passwordData);
            alert("Şifreniz başarıyla güncellendi!");
            setIsPasswordFormVisible(false);
            setPasswordData({ current_password: '', new_password: '', new_password_confirm: '' });
        } catch (error) {
            console.error("Şifre güncelleme hatası:", error);
            alert(`Güncelleme başarısız: ${error.response?.data?.detail || error.message}`);
        } finally {
            setIsChangingPassword(false);
        }
    };

    return (
        <div className="dashboard-container">
            <nav className="dashboard-nav">
                <div className="nav-left" style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                    <Link to="/dashboard" className="nav-brand">EastCoders</Link>
                </div>
                <div className="nav-links">
                    <Link to="/dashboard" className={`nav-link ${location.pathname === '/dashboard' ? 'active' : ''}`}>Özet</Link>
                    <Link to="/products" className={`nav-link ${location.pathname === '/products' ? 'active' : ''}`}>Ürünlerim</Link>
                    <Link to="/integration" className={`nav-link ${location.pathname === '/integration' ? 'active' : ''}`}>Aktarma</Link>
                    <Link to="/haber" className={`nav-link ${location.pathname === '/haber' ? 'active' : ''}`}>Haber</Link>
                    <Link to="/reports" className={`nav-link ${location.pathname === '/reports' ? 'active' : ''}`}>Raporlar</Link>
                    <Link to="/trend" className={`nav-link ${location.pathname === '/trend' ? 'active' : ''}`}>Trend</Link>
                    <Link to="/profile" className={`nav-link ${location.pathname === '/profile' ? 'active' : ''}`}>Profil</Link>
                </div>
                <div className="nav-user" style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                    <div className="notification-bell" style={{ position: 'relative', cursor: 'pointer', display: 'flex', alignItems: 'center', transition: 'transform 0.2s' }} onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.1)'} onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}>
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#475569" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="feather feather-bell">
                            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                            <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                        </svg>
                        <span className="notification-dot" style={{ position: 'absolute', top: '0', right: '2px', width: '8px', height: '8px', backgroundColor: '#ef4444', borderRadius: '50%', border: '2px solid #fff' }}></span>
                    </div>
                    <span>Hoş geldin, {user?.full_name || 'Kullanıcı'}</span>
                    <button onClick={logout} className="logout-btn">Çıkış Yap</button>
                </div>
            </nav>

            <main className="dashboard-main profile-main">
                <div className="profile-header">
                    <h1>Profilim</h1>
                    <p>Kişisel bilgilerinizi ve güvenlik ayarlarınızı buradan görüntüleyebilirsiniz.</p>
                </div>

                <div className="profile-content">
                    <div className="profile-card">
                        <h2>Kişisel Bilgiler</h2>
                        <div className="profile-form">
                            <div className="form-group">
                                <label>Ad Soyad</label>
                                <input 
                                    type="text" 
                                    name="full_name"
                                    value={formData.full_name} 
                                    onChange={handleInputChange} 
                                    className="profile-input" 
                                />
                            </div>
                            
                            <div className="form-group">
                                <label>E-posta Adresi</label>
                                <input 
                                    type="email" 
                                    name="email"
                                    value={formData.email} 
                                    onChange={handleInputChange} 
                                    className="profile-input" 
                                />
                            </div>

                            <div className="form-group">
                                <label>Telefon Numarası</label>
                                <input 
                                    type="text" 
                                    name="phone_number"
                                    value={formData.phone_number} 
                                    onChange={handleInputChange} 
                                    className="profile-input" 
                                />
                            </div>

                            <div className="form-group">
                                <label>Kullanıcı Rolü</label>
                                <input type="text" value={user?.role === 'seller' ? 'Satıcı' : (user?.role || '')} readOnly className="read-only-input role-input" />
                            </div>

                            <button 
                                onClick={handleUpdateProfile} 
                                disabled={isSaving} 
                                className="change-pwd-btn" 
                                style={{ marginTop: '10px', width: '100%', padding: '10px' }}
                            >
                                {isSaving ? 'Kaydediliyor...' : 'Değişiklikleri Kaydet'}
                            </button>
                        </div>
                    </div>

                    <div className="profile-card">
                        <h2>Güvenlik ve API</h2>
                        <div className="profile-form">
                            <div className="form-group">
                                <label>Şifre</label>
                                {!isPasswordFormVisible ? (
                                    <div className="password-group">
                                        <input type="password" value="********" readOnly className="read-only-input" />
                                        <button className="change-pwd-btn" onClick={() => setIsPasswordFormVisible(true)}>Değiştir</button>
                                    </div>
                                ) : (
                                    <div className="password-change-form" style={{ marginTop: '10px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
                                        <input 
                                            type="password" 
                                            name="current_password"
                                            placeholder="Mevcut Şifreniz" 
                                            value={passwordData.current_password}
                                            onChange={handlePasswordInputChange}
                                            className="profile-input" 
                                        />
                                        <input 
                                            type="password" 
                                            name="new_password"
                                            placeholder="Yeni Şifre" 
                                            value={passwordData.new_password}
                                            onChange={handlePasswordInputChange}
                                            className="profile-input" 
                                        />
                                        <input 
                                            type="password" 
                                            name="new_password_confirm"
                                            placeholder="Yeni Şifre (Tekrar)" 
                                            value={passwordData.new_password_confirm}
                                            onChange={handlePasswordInputChange}
                                            className="profile-input" 
                                        />
                                        <div style={{ display: 'flex', gap: '10px' }}>
                                            <button 
                                                onClick={handleUpdatePassword} 
                                                disabled={isChangingPassword} 
                                                className="change-pwd-btn"
                                                style={{ flex: 1, padding: '10px' }}
                                            >
                                                {isChangingPassword ? 'Güncelleniyor...' : 'Şifreyi Güncelle'}
                                            </button>
                                            <button 
                                                onClick={() => {
                                                    setIsPasswordFormVisible(false);
                                                    setPasswordData({ current_password: '', new_password: '', new_password_confirm: '' });
                                                }} 
                                                style={{ flex: 1, padding: '10px', border: '1px solid #e2e8f0', borderRadius: '8px', background: '#f8fafc', color: '#64748b', cursor: 'pointer', fontWeight: '500' }}
                                            >
                                                İptal
                                            </button>
                                        </div>
                                    </div>
                                )}
                            </div>
                            
                            <div className="form-group api-section">
                                <label>Bağlı API Key'ler (Aktarma)</label>
                                <div className="api-list">
                                    <div className="api-item empty">
                                        <div className="api-info">
                                            <span className="api-icon">🔗</span>
                                            <span>API bağlantılarınızı <Link to="/integration" className="api-link">Aktarma</Link> sayfasından yönetebilirsiniz.</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};
