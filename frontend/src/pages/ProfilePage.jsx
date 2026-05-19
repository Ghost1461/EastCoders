import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import api from '../api/client';
import './ProfilePage.css';

export const ProfilePage = () => {
    const { user, setUser } = useAuth();
    
    // Profile Update State
    const [isEditing, setIsEditing] = useState(false);
    const [formData, setFormData] = useState({
        full_name: user?.full_name || '',
        phone_number: user?.phone_number || '',
        email: user?.email || '',
    });
    const [updateStatus, setUpdateStatus] = useState({ loading: false, error: null, success: false });

    // Password Update State
    const [showPasswordModal, setShowPasswordModal] = useState(false);
    const [passwordData, setPasswordData] = useState({
        current_password: '',
        new_password: '',
        new_password_confirm: ''
    });
    const [passwordStatus, setPasswordStatus] = useState({ loading: false, error: null, success: false });

    const handleProfileChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleProfileSubmit = async () => {
        setUpdateStatus({ loading: true, error: null, success: false });
        try {
            const res = await api.put('/profile/update', formData);
            // Update auth context user and local storage
            const updatedUser = { ...user, ...res.data };
            setUser(updatedUser);
            localStorage.setItem('user', JSON.stringify(updatedUser));
            
            setUpdateStatus({ loading: false, error: null, success: true });
            setIsEditing(false);
            
            setTimeout(() => setUpdateStatus(prev => ({ ...prev, success: false })), 3000);
        } catch (err) {
            setUpdateStatus({ loading: false, error: err.response?.data?.detail || "Profil güncellenirken hata oluştu.", success: false });
        }
    };

    const handlePasswordChange = (e) => {
        setPasswordData({ ...passwordData, [e.target.name]: e.target.value });
    };

    const handlePasswordSubmit = async (e) => {
        e.preventDefault();
        setPasswordStatus({ loading: true, error: null, success: false });
        try {
            await api.put('/profile/change-password', passwordData);
            setPasswordStatus({ loading: false, error: null, success: true });
            setTimeout(() => {
                setShowPasswordModal(false);
                setPasswordStatus({ loading: false, error: null, success: false });
                setPasswordData({ current_password: '', new_password: '', new_password_confirm: '' });
            }, 2000);
        } catch (err) {
            setPasswordStatus({ loading: false, error: err.response?.data?.detail || "Şifre değiştirilirken hata oluştu.", success: false });
        }
    };

    return (
        <div className="dashboard-container">
            <Navbar />

            <main className="dashboard-main profile-main">
                <div className="profile-header">
                    <h1>Profilim</h1>
                    <p>Kişisel bilgilerinizi ve güvenlik ayarlarınızı buradan görüntüleyebilirsiniz.</p>
                </div>

                <div className="profile-content">
                    <div className="profile-card">
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                            <h2 style={{ margin: 0 }}>Kişisel Bilgiler</h2>
                            {!isEditing ? (
                                <button className="edit-btn" onClick={() => setIsEditing(true)}>Düzenle</button>
                            ) : (
                                <div style={{ display: 'flex', gap: '8px' }}>
                                    <button className="cancel-btn" onClick={() => {
                                        setIsEditing(false);
                                        setFormData({
                                            full_name: user?.full_name || '',
                                            phone_number: user?.phone_number || '',
                                            email: user?.email || '',
                                        });
                                        setUpdateStatus({ loading: false, error: null, success: false });
                                    }}>İptal</button>
                                    <button className="save-btn" onClick={handleProfileSubmit} disabled={updateStatus.loading}>
                                        {updateStatus.loading ? 'Kaydediliyor...' : 'Kaydet'}
                                    </button>
                                </div>
                            )}
                        </div>

                        {updateStatus.error && <p className="error-message">{updateStatus.error}</p>}
                        {updateStatus.success && <p className="success-message">Profil başarıyla güncellendi!</p>}

                        <div className="profile-form">
                            <div className="form-group">
                                <label>Ad Soyad</label>
                                <input 
                                    type="text" 
                                    name="full_name"
                                    value={isEditing ? formData.full_name : (user?.full_name || '')} 
                                    onChange={handleProfileChange}
                                    readOnly={!isEditing} 
                                    className={isEditing ? 'editable-input' : 'read-only-input'} 
                                />
                            </div>
                            
                            <div className="form-group">
                                <label>E-posta Adresi</label>
                                <input 
                                    type="email" 
                                    name="email"
                                    value={isEditing ? formData.email : (user?.email || '')} 
                                    onChange={handleProfileChange}
                                    readOnly={!isEditing} 
                                    className={isEditing ? 'editable-input' : 'read-only-input'} 
                                />
                            </div>

                            <div className="form-group">
                                <label>Telefon Numarası</label>
                                <input 
                                    type="text" 
                                    name="phone_number"
                                    value={isEditing ? formData.phone_number : (user?.phone_number || '')} 
                                    onChange={handleProfileChange}
                                    readOnly={!isEditing} 
                                    className={isEditing ? 'editable-input' : 'read-only-input'} 
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
                                <div className="password-group">
                                    <input type="password" value="********" readOnly className="read-only-input" />
                                    <button className="change-pwd-btn" onClick={() => setShowPasswordModal(true)}>Değiştir</button>
                                </div>
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

                {/* Password Modal */}
                {showPasswordModal && (
                    <div className="modal-overlay" onClick={() => !passwordStatus.loading && setShowPasswordModal(false)}>
                        <div className="modal-content" onClick={e => e.stopPropagation()}>
                            <div className="modal-header">
                                <h2>Şifre Değiştir</h2>
                                <button className="modal-close" onClick={() => setShowPasswordModal(false)}>✕</button>
                            </div>
                            <form onSubmit={handlePasswordSubmit} className="modal-body">
                                {passwordStatus.error && <p className="error-message">{passwordStatus.error}</p>}
                                {passwordStatus.success && <p className="success-message">Şifre başarıyla değiştirildi!</p>}
                                
                                <div className="form-group">
                                    <label>Mevcut Şifre</label>
                                    <input 
                                        type="password" 
                                        name="current_password"
                                        value={passwordData.current_password} 
                                        onChange={handlePasswordChange}
                                        required 
                                        className="editable-input" 
                                    />
                                </div>
                                <div className="form-group">
                                    <label>Yeni Şifre</label>
                                    <input 
                                        type="password" 
                                        name="new_password"
                                        value={passwordData.new_password} 
                                        onChange={handlePasswordChange}
                                        required 
                                        className="editable-input" 
                                        placeholder="En az 6 karakter, 1 büyük, 1 küçük harf, 1 rakam"
                                    />
                                </div>
                                <div className="form-group">
                                    <label>Yeni Şifre (Tekrar)</label>
                                    <input 
                                        type="password" 
                                        name="new_password_confirm"
                                        value={passwordData.new_password_confirm} 
                                        onChange={handlePasswordChange}
                                        required 
                                        className="editable-input" 
                                    />
                                </div>
                                <div className="modal-actions">
                                    <button type="button" className="cancel-btn" onClick={() => setShowPasswordModal(false)}>İptal</button>
                                    <button type="submit" className="save-btn" disabled={passwordStatus.loading}>
                                        {passwordStatus.loading ? 'Değiştiriliyor...' : 'Şifreyi Değiştir'}
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
};
