import { useAuth } from '../context/AuthContext';
import { Link, useLocation } from 'react-router-dom';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { useState, useEffect } from 'react';
import { Navbar } from '../components/Navbar';
import './OverviewPage.css';

export const OverviewPage = () => {
    const { user, logout } = useAuth();
    const location = useLocation();

    // Mock veriler, ileride endpoint'ler bağlandığında bunlar stateden gelecek
    const [metrics, setMetrics] = useState({
        totalProducts: 0, // Bu değer backend'den (Pie Chart verisinden) beslenecek
        totalSales: 1284,
        pendingOrders: 23,
        averageRating: 4.8
    });

    const [categoryData, setCategoryData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) return;

                const response = await fetch('http://localhost:8000/products_display/analytics/category-counts', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    if (data && data.categories) {
                    const formattedData = data.categories
                        .filter(item => item.category !== null) // null değerleri temizle
                        .map(item => ({
                            name: item.category,
                            value: Number(item.count) // Sayı olduğundan emin ol
                        }));  
                    
                    console.log("Pie Chart Verisi:", formattedData); // Tarayıcı konsolundan kontrol et
                    setCategoryData(formattedData);

                    // Toplam ürün sayısını hesaplamak için tüm ürünleri çek ve grupla (Ürünlerim sayfasıyla aynı mantık)
                    try {
                        const allProductsRes = await fetch('http://localhost:8000/products_display/all', {
                            headers: { 'Authorization': `Bearer ${token}` }
                        });
                        
                        if (allProductsRes.ok) {
                            const allData = await allProductsRes.json();
                            const uniqueProducts = new Set();
                            
                            if (allData && allData.products) {
                                allData.products.forEach(listing => {
                                    if (listing.product && listing.product.id) {
                                        uniqueProducts.add(listing.product.id);
                                    }
                                });
                            }
                            
                            setMetrics(prev => ({ ...prev, totalProducts: uniqueProducts.size }));
                        }
                    } catch (err) {
                        console.error("Toplam ürün sayısı çekilirken hata:", err);
                    }
                    }
                }
                
                // Sipariş Özetini Çek (Toplam Satış ve Bekleyen Siparişler)
                try {
                    const ordersRes = await fetch('http://localhost:8000/orders/get/summary', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (ordersRes.ok) {
                        const orderData = await ordersRes.json();
                        setMetrics(prev => ({ 
                            ...prev, 
                            totalSales: orderData.total_orders || 0,
                            pendingOrders: orderData.shipped_orders || 0
                        }));
                    }
                } catch (err) {
                    console.error("Sipariş özeti çekilirken hata:", err);
                }

                // Yorum Özetini Çek (Ortalama Mağaza Puanı)
                try {
                    const reviewsRes = await fetch('http://localhost:8000/review_display/summary', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (reviewsRes.ok) {
                        const reviewData = await reviewsRes.json();
                        setMetrics(prev => ({ 
                            ...prev, 
                            averageRating: reviewData.average_rating || 0
                        }));
                    }
                } catch (err) {
                    console.error("Yorum özeti çekilirken hata:", err);
                }

            } catch (error) {
                console.error("Veriler çekilirken hata oluştu:", error);
            }
        };

        fetchData();
    }, []);
    
    const COLORS = ['#2563eb', '#7c3aed', '#ec4899', '#f59e0b', '#10b981', '#3b82f6'];

    return (
        <div className="dashboard-container">
            <Navbar />

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
                                <h3>Toplam Ürün Çeşidi</h3>
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
                                {categoryData.length > 0 ? (
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
                                                nameKey="name"
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
                                ) : (
                                    <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '100%', color: '#94a3b8' }}>
                                        <div style={{ fontSize: '48px', marginBottom: '16px' }}>📊</div>
                                        <p>Henüz ürün verisi bulunmuyor.</p>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};
