import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useLocation } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer, Cell, PieChart, Pie } from 'recharts';
import api from '../api/client';
import './ReportsPage.css';

export const ReportsPage = () => {
    const { user, logout } = useAuth();
    const location = useLocation();

    const [monthlyData, setMonthlyData] = useState([]);
    const [platformData, setPlatformData] = useState([]);
    const [summaryMetrics, setSummaryMetrics] = useState({
        totalRevenue: 0,
        totalOrders: 0,
        averageOrderValue: 0
    });
    const [isLoading, setIsLoading] = useState(true);

    const COLORS = ['#f27a1a', '#ff6000', '#232f3e', '#10b981', '#3b82f6'];

    useEffect(() => {
        const fetchReportsData = async () => {
            try {
                // 1. Aylık Analiz
                const monthlyRes = await api.get('/orders/analysis/monthly');
                if (monthlyRes.data && monthlyRes.data.data) {
                    const formattedMonthly = monthlyRes.data.data.map(item => ({
                        name: item.period,
                        Gelir: item.total_revenue,
                        Sipariş: item.total_orders
                    }));
                    setMonthlyData(formattedMonthly);
                }

                // 2. Platform Analizi
                const platformRes = await api.get('/orders/analysis/platform');
                if (platformRes.data && platformRes.data.platforms) {
                    const formattedPlatform = platformRes.data.platforms.map(item => ({
                        name: item.platform.charAt(0).toUpperCase() + item.platform.slice(1),
                        value: item.total_revenue,
                        orders: item.total_orders
                    }));
                    setPlatformData(formattedPlatform);
                }

                // 3. Genel Özet
                const summaryRes = await api.get('/orders/get/summary');
                if (summaryRes.data) {
                    setSummaryMetrics({
                        totalRevenue: summaryRes.data.total_revenue || 0,
                        totalOrders: summaryRes.data.total_orders || 0,
                        averageOrderValue: summaryRes.data.average_order_value || 0
                    });
                }

            } catch (error) {
                console.error("Rapor verileri çekilirken hata oluştu:", error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchReportsData();
    }, []);

    const formatCurrency = (value) => {
        return new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'TRY' }).format(value);
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

            <main className="dashboard-main reports-main">
                <div className="reports-header">
                    <h1>Satış Raporları ve Analizler</h1>
                    <p>Satış trendlerinizi ve platform performansınızı detaylı olarak inceleyin.</p>
                </div>

                {isLoading ? (
                    <div style={{ textAlign: 'center', padding: '50px', color: '#64748b' }}>Yükleniyor...</div>
                ) : (
                    <>
                        <div className="metrics-summary-grid">
                            <div className="summary-card">
                                <div className="summary-icon" style={{ backgroundColor: '#eff6ff', color: '#3b82f6' }}>💰</div>
                                <div className="summary-info">
                                    <h4>Toplam Gelir</h4>
                                    <p className="summary-value">{formatCurrency(summaryMetrics.totalRevenue)}</p>
                                </div>
                            </div>
                            <div className="summary-card">
                                <div className="summary-icon" style={{ backgroundColor: '#f0fdf4', color: '#22c55e' }}>📦</div>
                                <div className="summary-info">
                                    <h4>Toplam Sipariş</h4>
                                    <p className="summary-value">{summaryMetrics.totalOrders}</p>
                                </div>
                            </div>
                            <div className="summary-card">
                                <div className="summary-icon" style={{ backgroundColor: '#fdf2f8', color: '#ec4899' }}>🛒</div>
                                <div className="summary-info">
                                    <h4>Ortalama Sepet Tutarı</h4>
                                    <p className="summary-value">{formatCurrency(summaryMetrics.averageOrderValue)}</p>
                                </div>
                            </div>
                        </div>

                        <div className="charts-grid">
                            <div className="chart-card">
                                <h2>Aylık Satış Trendi (Gelir)</h2>
                                <div className="chart-container">
                                    {monthlyData.length > 0 ? (
                                        <ResponsiveContainer width="100%" height="100%">
                                            <LineChart data={monthlyData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                                                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#64748b' }} dy={10} />
                                                <YAxis axisLine={false} tickLine={false} tick={{ fill: '#64748b' }} tickFormatter={(value) => `₺${value}`} dx={-10} />
                                                <RechartsTooltip 
                                                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}
                                                    formatter={(value) => formatCurrency(value)}
                                                />
                                                <Legend verticalAlign="top" height={36} />
                                                <Line type="monotone" dataKey="Gelir" stroke="#3b82f6" strokeWidth={3} dot={{ r: 4, fill: '#3b82f6', strokeWidth: 2, stroke: '#fff' }} activeDot={{ r: 6 }} />
                                            </LineChart>
                                        </ResponsiveContainer>
                                    ) : (
                                        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%', color: '#94a3b8' }}>Veri bulunamadı.</div>
                                    )}
                                </div>
                            </div>

                            <div className="chart-card">
                                <h2>Platform Dağılımı (Gelir)</h2>
                                <div className="chart-container">
                                    {platformData.length > 0 ? (
                                        <ResponsiveContainer width="100%" height="100%">
                                            <PieChart>
                                                <Pie
                                                    data={platformData}
                                                    cx="50%"
                                                    cy="50%"
                                                    innerRadius={60}
                                                    outerRadius={100}
                                                    paddingAngle={5}
                                                    dataKey="value"
                                                    nameKey="name"
                                                >
                                                    {platformData.map((entry, index) => (
                                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                                    ))}
                                                </Pie>
                                                <RechartsTooltip 
                                                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}
                                                    formatter={(value) => formatCurrency(value)}
                                                />
                                                <Legend verticalAlign="bottom" height={36} iconType="circle" />
                                            </PieChart>
                                        </ResponsiveContainer>
                                    ) : (
                                        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%', color: '#94a3b8' }}>Veri bulunamadı.</div>
                                    )}
                                </div>
                            </div>
                        </div>
                    </>
                )}
            </main>
        </div>
    );
};
