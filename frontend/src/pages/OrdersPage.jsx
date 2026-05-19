import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Navbar } from '../components/Navbar';

export const OrdersPage = () => {
    const { user } = useAuth();
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);

    const [searchTerm, setSearchTerm] = useState('');
    const [platform, setPlatform] = useState('');
    const [summary, setSummary] = useState(null);

    const fetchOrders = async () => {
        try {
            setLoading(true);
            const token = localStorage.getItem('token');
            if (!token) return;

            let url = 'http://localhost:8000/orders/';
            if (searchTerm.trim() !== '') {
                url = `http://localhost:8000/orders/search?q=${encodeURIComponent(searchTerm)}`;
            } else if (platform) {
                url = `http://localhost:8000/orders/platform/${platform}`;
            }

            const response = await fetch(url, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                if (data && data.orders) {
                    setOrders(data.orders);
                } else {
                    setOrders([]);
                }
            }
        } catch (error) {
            console.error("Siparişler çekilirken hata oluştu:", error);
        } finally {
            setLoading(false);
        }
    };

    const fetchSummary = async () => {
        try {
            const token = localStorage.getItem('token');
            if (!token) return;
            const res = await fetch('http://localhost:8000/orders/get/summary', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                const data = await res.json();
                setSummary(data);
            }
        } catch (error) {
            console.error("Özet çekilirken hata oluştu:", error);
        }
    };

    useEffect(() => {
        fetchSummary();
    }, []);

    useEffect(() => {
        const delayDebounceFn = setTimeout(() => {
            fetchOrders();
        }, 500);
        return () => clearTimeout(delayDebounceFn);
    }, [searchTerm, platform]);

    const getStatusStyle = (status) => {
        const lower = (status || '').toLowerCase();
        if (lower.includes('deliver') || lower.includes('teslim')) return { color: '#10b981', background: '#d1fae5' };
        if (lower.includes('cancel') || lower.includes('iptal')) return { color: '#ef4444', background: '#fee2e2' };
        if (lower.includes('return') || lower.includes('iade')) return { color: '#f59e0b', background: '#fef3c7' };
        if (lower.includes('ship') || lower.includes('kargo')) return { color: '#3b82f6', background: '#dbeafe' };
        return { color: '#64748b', background: '#f1f5f9' };
    };

    return (
        <div className="dashboard-container">
            <Navbar />

            <main className="dashboard-main">
                <div style={{ marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <h1 style={{ margin: 0, color: '#0f172a' }}>Siparişlerim</h1>
                    
                    <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
                        <div style={{ display: 'flex', alignItems: 'center', background: '#fff', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '10px 16px', minWidth: '300px' }}>
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: '8px' }}>
                                <circle cx="11" cy="11" r="8"></circle>
                                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                            </svg>
                            <input
                                type="text"
                                placeholder="Sipariş No veya Müşteri Ara..."
                                value={searchTerm}
                                onChange={(e) => {
                                    setSearchTerm(e.target.value);
                                    setPlatform(''); // Reset platform when searching
                                }}
                                style={{ border: 'none', outline: 'none', width: '100%', background: 'transparent' }}
                            />
                        </div>

                        <select 
                            value={platform} 
                            onChange={(e) => {
                                setPlatform(e.target.value);
                                setSearchTerm(''); // Reset search when platform changed
                            }} 
                            style={{ padding: '10px 16px', borderRadius: '8px', border: '1px solid #e2e8f0', background: '#fff', color: '#475569', outline: 'none', cursor: 'pointer' }}
                        >
                            <option value="">Tüm Platformlar</option>
                            <option value="trendyol">Trendyol</option>
                            <option value="hepsiburada">Hepsiburada</option>
                            <option value="amazon">Amazon</option>
                        </select>
                    </div>
                </div>

                {summary && (
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px', marginBottom: '24px' }}>
                        <div style={{ background: '#fff', padding: '20px', borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px rgba(0,0,0,0.02)' }}>
                            <div style={{ color: '#64748b', fontSize: '14px', fontWeight: '500', marginBottom: '8px' }}>Toplam Ciro</div>
                            <div style={{ color: '#0f172a', fontSize: '24px', fontWeight: '700' }}>₺{summary.total_revenue?.toLocaleString()}</div>
                        </div>
                        <div style={{ background: '#fff', padding: '20px', borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px rgba(0,0,0,0.02)' }}>
                            <div style={{ color: '#64748b', fontSize: '14px', fontWeight: '500', marginBottom: '8px' }}>Toplam Sipariş</div>
                            <div style={{ color: '#0f172a', fontSize: '24px', fontWeight: '700' }}>{summary.total_orders}</div>
                        </div>
                        <div style={{ background: '#fff', padding: '20px', borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px rgba(0,0,0,0.02)' }}>
                            <div style={{ color: '#64748b', fontSize: '14px', fontWeight: '500', marginBottom: '8px' }}>Ortalama Sipariş Tutarı</div>
                            <div style={{ color: '#0f172a', fontSize: '24px', fontWeight: '700' }}>₺{summary.average_order_value?.toLocaleString(undefined, {maximumFractionDigits:2})}</div>
                        </div>
                        <div style={{ background: '#fff', padding: '20px', borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px rgba(0,0,0,0.02)' }}>
                            <div style={{ color: '#64748b', fontSize: '14px', fontWeight: '500', marginBottom: '8px' }}>Teslim Edilenler</div>
                            <div style={{ color: '#10b981', fontSize: '24px', fontWeight: '700' }}>{summary.delivered_orders}</div>
                        </div>
                    </div>
                )}

                <div className="products-table-container" style={{ background: '#fff', borderRadius: '12px', border: '1px solid #e2e8f0', overflow: 'hidden' }}>
                    <table className="products-table" style={{ width: '100%', borderCollapse: 'collapse' }}>
                        <thead>
                            <tr style={{ background: '#f8fafc', borderBottom: '1px solid #e2e8f0', textAlign: 'left' }}>
                                <th style={{ padding: '16px', color: '#64748b', fontWeight: '600' }}>Sipariş No</th>
                                <th style={{ padding: '16px', color: '#64748b', fontWeight: '600' }}>Platform</th>
                                <th style={{ padding: '16px', color: '#64748b', fontWeight: '600' }}>Müşteri</th>
                                <th style={{ padding: '16px', color: '#64748b', fontWeight: '600' }}>Tarih</th>
                                <th style={{ padding: '16px', color: '#64748b', fontWeight: '600' }}>Tutar</th>
                                <th style={{ padding: '16px', color: '#64748b', fontWeight: '600' }}>Durum</th>
                            </tr>
                        </thead>
                        <tbody>
                            {loading ? (
                                <tr>
                                    <td colSpan="6" style={{ textAlign: 'center', padding: '20px' }}>Yükleniyor...</td>
                                </tr>
                            ) : orders.length > 0 ? (
                                orders.map((order) => (
                                    <tr key={order.id} style={{ borderBottom: '1px solid #e2e8f0' }}>
                                        <td style={{ padding: '16px' }}>{order.external_order_id}</td>
                                        <td style={{ padding: '16px', textTransform: 'capitalize' }}>{order.platform}</td>
                                        <td style={{ padding: '16px' }}>{order.customer_name || 'Gizli Müşteri'}</td>
                                        <td style={{ padding: '16px' }}>{new Date(order.order_date).toLocaleDateString('tr-TR')}</td>
                                        <td style={{ padding: '16px', fontWeight: 'bold' }}>₺{order.total_amount}</td>
                                        <td style={{ padding: '16px' }}>
                                            <span style={{ 
                                                padding: '4px 8px', 
                                                borderRadius: '12px', 
                                                fontSize: '12px', 
                                                fontWeight: '600',
                                                ...getStatusStyle(order.status) 
                                            }}>
                                                {order.status}
                                            </span>
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="6" style={{ textAlign: 'center', padding: '40px', color: '#64748b' }}>Sipariş bulunamadı.</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </main>
        </div>
    );
};
