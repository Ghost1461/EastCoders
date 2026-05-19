import { useState, useEffect } from 'react';
import api from '../api/client';
import { AdminNavbar } from '../components/AdminNavbar';
import './AdminPage.css';

export const AdminPage = () => {
    const [summary, setSummary] = useState(null);
    const [users, setUsers] = useState([]);
    const [accounts, setAccounts] = useState([]);
    const [caches, setCaches] = useState([]);
    const [listings, setListings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchAdminData();
    }, []);

    const fetchAdminData = async () => {
        setLoading(true);
        try {
            const [summaryRes, usersRes, accountsRes, cachesRes, listingsRes] = await Promise.all([
                api.get('/admin/summary'),
                api.get('/admin/users'),
                api.get('/admin/connected-accounts'),
                api.get('/admin/ai-cache'),
                api.get('/admin/listings')
            ]);
            setSummary(summaryRes.data);
            setUsers(usersRes.data.users || []);
            setAccounts(accountsRes.data.accounts || []);
            setCaches(cachesRes.data.records || []);
            setListings(listingsRes.data.listings || []);
        } catch (err) {
            console.error("Admin data fetch error:", err);
            setError('Veriler yüklenirken bir hata oluştu. Lütfen yetkinizi kontrol edin.');
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="admin-layout">
                <AdminNavbar />
                <div className="admin-loading">
                    <div className="admin-spinner"></div>
                    <p>Yönetim paneli yükleniyor...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="admin-layout">
            <AdminNavbar />
            
            <main className="admin-main">
                <header className="admin-page-header">
                    <h1>Sistem Özeti</h1>
                    <button className="admin-refresh-btn" onClick={fetchAdminData}>
                        🔄 Yenile
                    </button>
                </header>

                {error && <div className="admin-error-box">{error}</div>}

                {/* Summary Cards */}
                <div className="admin-summary-grid">
                    <div className="admin-stat-card">
                        <div className="stat-icon users-icon">👥</div>
                        <div className="stat-content">
                            <h3>Toplam Kullanıcı</h3>
                            <span className="stat-value">{summary?.total_users || 0}</span>
                        </div>
                    </div>
                    <div className="admin-stat-card">
                        <div className="stat-icon accounts-icon">🔗</div>
                        <div className="stat-content">
                            <h3>Bağlı Hesaplar</h3>
                            <span className="stat-value">{summary?.total_connected_accounts || 0}</span>
                        </div>
                    </div>
                    <div className="admin-stat-card">
                        <div className="stat-icon cache-icon">🧠</div>
                        <div className="stat-content">
                            <h3>AI Önbellek Kayıtları</h3>
                            <span className="stat-value">{summary?.total_ai_cache_records || 0}</span>
                        </div>
                    </div>
                </div>

                {/* Users Table */}
                <section className="admin-section">
                    <h2>Kullanıcı Listesi</h2>
                    <div className="admin-table-container">
                        <table className="admin-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Ad Soyad</th>
                                    <th>E-posta</th>
                                    <th>Rol</th>
                                    <th>Kayıt Tarihi</th>
                                </tr>
                            </thead>
                            <tbody>
                                {users.map(user => (
                                    <tr key={user.id}>
                                        <td>#{user.id}</td>
                                        <td>{user.full_name}</td>
                                        <td>{user.email}</td>
                                        <td>
                                            <span className={`role-badge ${user.role === 'admin' ? 'role-admin' : 'role-seller'}`}>
                                                {user.role}
                                            </span>
                                        </td>
                                        <td>{new Date(user.created_at).toLocaleDateString('tr-TR')}</td>
                                    </tr>
                                ))}
                                {users.length === 0 && (
                                    <tr>
                                        <td colSpan="5" className="text-center">Kullanıcı bulunamadı.</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </section>

                {/* Connected Accounts Table */}
                <section className="admin-section" style={{marginTop: '32px'}}>
                    <h2>Bağlı Hesaplar</h2>
                    <div className="admin-table-container">
                        <table className="admin-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Kullanıcı ID</th>
                                    <th>Platform</th>
                                    <th>Mağaza Adı</th>
                                    <th>Bağlantı Tarihi</th>
                                </tr>
                            </thead>
                            <tbody>
                                {accounts.map(acc => (
                                    <tr key={acc.id}>
                                        <td>#{acc.id}</td>
                                        <td>#{acc.user_id}</td>
                                        <td><span className={`role-badge ${acc.platform === 'trendyol' ? 'role-admin' : 'role-seller'}`}>{acc.platform}</span></td>
                                        <td>{acc.store_name || '-'}</td>
                                        <td>{new Date(acc.connected_at).toLocaleDateString('tr-TR')}</td>
                                    </tr>
                                ))}
                                {accounts.length === 0 && (
                                    <tr>
                                        <td colSpan="5" className="text-center">Bağlı hesap bulunamadı.</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </section>

                {/* AI Cache Table */}
                <section className="admin-section" style={{marginTop: '32px'}}>
                    <h2>AI Önbellek Kayıtları</h2>
                    <div className="admin-table-container">
                        <table className="admin-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Kullanıcı ID</th>
                                    <th>Endpoint</th>
                                    <th>Oluşturulma Tarihi</th>
                                </tr>
                            </thead>
                            <tbody>
                                {caches.map(c => (
                                    <tr key={c.id}>
                                        <td>#{c.id}</td>
                                        <td>#{c.user_id}</td>
                                        <td>{c.report_type}</td>
                                        <td>{new Date(c.created_at).toLocaleString('tr-TR')}</td>
                                    </tr>
                                ))}
                                {caches.length === 0 && (
                                    <tr>
                                        <td colSpan="4" className="text-center">AI önbellek kaydı bulunamadı.</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </section>

                {/* Product Listings Table */}
                <section className="admin-section" style={{marginTop: '32px'}}>
                    <h2>Ürün Listelemeleri</h2>
                    <div className="admin-table-container">
                        <table className="admin-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Kullanıcı ID</th>
                                    <th>Platform</th>
                                    <th>Platform Ürün ID</th>
                                    <th>Stok</th>
                                </tr>
                            </thead>
                            <tbody>
                                {listings.map(l => (
                                    <tr key={l.listing_id}>
                                        <td>#{l.listing_id}</td>
                                        <td>#{l.user_id}</td>
                                        <td>{l.platform}</td>
                                        <td>{l.external_product_id}</td>
                                        <td>{l.stock}</td>
                                    </tr>
                                ))}
                                {listings.length === 0 && (
                                    <tr>
                                        <td colSpan="5" className="text-center">Ürün listelemesi bulunamadı.</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </section>
            </main>
        </div>
    );
};
