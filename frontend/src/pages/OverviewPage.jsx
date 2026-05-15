import { useAuth } from '../context/AuthContext';
import { Link, useLocation } from 'react-router-dom';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { useState, useEffect } from 'react';
import './OverviewPage.css';

export const OverviewPage = () => {
    const { user, logout } = useAuth();
    const location = useLocation();

    // Mock veriler, ileride endpoint'ler bağlandığında bunlar stateden gelecek
    const metrics = {
        totalProducts: 142,
        totalSales: 1284,
        pendingOrders: 23,
        averageRating: 4.8
    };

    const [categoryData, setCategoryData] = useState([]);

    useEffect(() => {
        const fetchCategories = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) return;

                const response = await fetch('http://localhost:8000/products_display/options/categories', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    if (data && data.categories) {
                        setCategoryData(data.categories);
                    }
                }
            } catch (error) {
                console.error("Kategoriler çekilirken hata oluştu:", error);
            }
        };

        fetchCategories();
    }, []);
    
    const COLORS = ['#2563eb', '#7c3aed', '#ec4899', '#f59e0b', '#10b981', '#3b82f6'];

    return (
        <div className="dashboard-container">
            <nav className="dashboard-nav">
                <Link to="/dashboard" className="nav-brand">EastCoders</Link>
                <div className="nav-links">
                    <Link to="/dashboard" className={`nav-link ${location.pathname === '/dashboard' ? 'active' : ''}`}>Özet</Link>
                    <Link to="/products" className={`nav-link ${location.pathname === '/products' ? 'active' : ''}`}>Ürünlerim</Link>
                    <Link to="/integration" className={`nav-link ${location.pathname === '/integration' ? 'active' : ''}`}>Aktarma</Link>
                </div>
                <div className="nav-user">
                    <span>Hoş geldin, {user?.full_name || 'Kullanıcı'}</span>
                    <button onClick={logout} className="logout-btn">Çıkış Yap</button>
                </div>
            </nav>

            <main className="dashboard-main">
                <div className="dashboard-header">
                    <h1>Mağaza Özeti</h1>
                    <p>Satış ve mağaza performansınızın genel görünümü.</p>
                </div>

                <div className="overview-content">
                    <div className="metrics-column">
                        <div className="metric-card">
                            <div className="metric-icon">📦</div>
                            <div className="metric-info">
                                <h3>Toplam Ürün Sayısı</h3>
                                <p className="metric-value">{metrics.totalProducts}</p>
                            </div>
                        </div>

                        <div className="metric-card">
                            <div className="metric-icon">💰</div>
                            <div className="metric-info">
                                <h3>Toplam Satış Sayısı</h3>
                                <p className="metric-value">{metrics.totalSales}</p>
                            </div>
                        </div>

                        <div className="metric-card">
                            <div className="metric-icon">⏳</div>
                            <div className="metric-info">
                                <h3>Bekleyen Siparişler</h3>
                                <p className="metric-value">{metrics.pendingOrders}</p>
                            </div>
                        </div>

                        <div className="metric-card">
                            <div className="metric-icon">⭐</div>
                            <div className="metric-info">
                                <h3>Ortalama Mağaza Puanı</h3>
                                <p className="metric-value">{metrics.averageRating} <span style={{fontSize: "16px", color: "#94a3b8"}}>/ 5.0</span></p>
                            </div>
                        </div>
                    </div>

                    <div className="chart-column">
                        <div className="chart-card">
                            <h2>Ürün Dağılımı</h2>
                            <div className="chart-container">
                                <ResponsiveContainer width="100%" height={300}>
                                    <PieChart>
                                        <Pie
                                            data={categoryData}
                                            cx="50%"
                                            cy="50%"
                                            innerRadius={60}
                                            outerRadius={100}
                                            fill="#8884d8"
                                            paddingAngle={5}
                                            dataKey="value"
                                        >
                                            {categoryData.map((entry, index) => (
                                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                            ))}
                                        </Pie>
                                        <Tooltip 
                                            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}
                                            formatter={(value, name) => [`${value} Ürün`, name]}
                                        />
                                        <Legend verticalAlign="bottom" height={36} iconType="circle" />
                                    </PieChart>
                                </ResponsiveContainer>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};
