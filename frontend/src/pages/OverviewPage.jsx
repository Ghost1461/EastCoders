import { useAuth } from '../context/AuthContext';
import { Link, useLocation } from 'react-router-dom';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend, BarChart, Bar, XAxis, YAxis, CartesianGrid, AreaChart, Area, ComposedChart, Line } from 'recharts';
import { useState, useEffect } from 'react';
import { Navbar } from '../components/Navbar';
import './OverviewPage.css';

export const OverviewPage = () => {
    const { user, logout } = useAuth();
    const location = useLocation();

    // Mock veriler, ileride endpoint'ler bağlandığında bunlar stateden gelecek
    const [metrics, setMetrics] = useState({
        totalProducts: 0, // Bu değer backend'den (Pie Chart verisinden) beslenecek
        totalSales: 0,
        pendingOrders: 0,
        averageRating: 0,
        totalRevenue: 0,
        averageOrderValue: 0
    });

    const [categoryData, setCategoryData] = useState([]);
    const [ratingData, setRatingData] = useState([]);
    const [topicData, setTopicData] = useState([]);
    const [timePeriod, setTimePeriod] = useState('daily');
    const [timeData, setTimeData] = useState([]);
    const [platformData, setPlatformData] = useState([]);

    useEffect(() => {
        const fetchTimeData = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) return;
                
                const response = await fetch(`http://localhost:8000/orders/analysis/${timePeriod}`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });

                if (response.ok) {
                    const data = await response.json();
                    if (data && data.data) {
                        const formatted = data.data.map(d => {
                            let displayPeriod = d.period;
                            if (timePeriod === 'daily') {
                                const dateObj = new Date(d.period);
                                displayPeriod = dateObj.toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' });
                            } else if (timePeriod === 'monthly') {
                                const dateObj = new Date(d.period + '-01');
                                displayPeriod = dateObj.toLocaleDateString('tr-TR', { month: 'long', year: 'numeric' });
                            }
                            return { ...d, displayPeriod };
                        });
                        setTimeData(formatted);
                    }
                }
            } catch (err) {
                console.error("Zaman analizi çekilirken hata:", err);
            }
        };

        fetchTimeData();
    }, [timePeriod]);

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
                            pendingOrders: orderData.shipped_orders || 0,
                            totalRevenue: orderData.total_revenue || 0,
                            averageOrderValue: orderData.average_order_value || 0
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

                // Puan Dağılımı Çek
                try {
                    const ratingRes = await fetch('http://localhost:8000/review_display/rating-distribution', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (ratingRes.ok) {
                        const ratingJson = await ratingRes.json();
                        if (ratingJson.rating_distribution) {
                            const formattedRating = ratingJson.rating_distribution.map(item => ({
                                rating: `${item.rating}★`,
                                count: item.count
                            }));
                            setRatingData(formattedRating);
                        }
                    }
                } catch (err) {
                    console.error("Puan dağılımı çekilirken hata:", err);
                }

                // Konu Özeti Çek
                try {
                    const topicRes = await fetch('http://localhost:8000/review_display/topic-summary', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (topicRes.ok) {
                        const topicJson = await topicRes.json();
                        if (topicJson.topics) {
                            setTopicData(topicJson.topics.slice(0, 6)); // İlk 6
                        }
                    }
                } catch (err) {
                    console.error("Konu özeti çekilirken hata:", err);
                }

                // Platform Analizi Çek
                try {
                    const platformRes = await fetch('http://localhost:8000/orders/analysis/platform', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (platformRes.ok) {
                        const platformJson = await platformRes.json();
                        if (platformJson.platforms) {
                            setPlatformData(platformJson.platforms);
                        }
                    }
                } catch (err) {
                    console.error("Platform analizi çekilirken hata:", err);
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
                    <div className="metrics-column" style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '20px' }}>
                        <div className="metric-card">
                            <div className="metric-icon">💵</div>
                            <div className="metric-info">
                                <h3>Toplam Ciro</h3>
                                <p className="metric-value">₺{metrics.totalRevenue.toLocaleString('tr-TR')}</p>
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
                            <div className="metric-icon">📈</div>
                            <div className="metric-info">
                                <h3>Ortalama Sipariş Tutarı</h3>
                                <p className="metric-value">₺{metrics.averageOrderValue.toLocaleString('tr-TR')}</p>
                            </div>
                        </div>

                        <div className="metric-card">
                            <div className="metric-icon">📦</div>
                            <div className="metric-info">
                                <h3>Toplam Ürün Çeşidi</h3>
                                <p className="metric-value">{metrics.totalProducts}</p>
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

                <div className="overview-content" style={{ marginTop: '32px', gap: '32px', flexWrap: 'wrap' }}>
                    <div className="chart-card" style={{ flex: 1, minWidth: '400px' }}>
                        <h2>Puan Dağılımı</h2>
                        <div className="chart-container">
                            {ratingData.length > 0 ? (
                                <ResponsiveContainer width="100%" height={300}>
                                    <BarChart data={ratingData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                                        <XAxis dataKey="rating" tick={{fill: '#64748b', fontSize: 13}} axisLine={false} tickLine={false} />
                                        <YAxis tick={{fill: '#64748b', fontSize: 13}} axisLine={false} tickLine={false} />
                                        <Tooltip cursor={{fill: '#f1f5f9'}} contentStyle={{ borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 10px 25px -5px rgba(0,0,0,0.1)' }} />
                                        <Bar dataKey="count" name="Yorum Sayısı" fill="#fbbf24" radius={[6, 6, 0, 0]} />
                                    </BarChart>
                                </ResponsiveContainer>
                            ) : (
                                <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '100%', color: '#94a3b8' }}>
                                    <div style={{ fontSize: '48px', marginBottom: '16px' }}>📉</div>
                                    <p>Veri bulunmuyor.</p>
                                </div>
                            )}
                        </div>
                    </div>

                    <div className="chart-card" style={{ flex: 1, minWidth: '400px' }}>
                        <h2>En Çok Yorumlanan Konular</h2>
                        <div className="chart-container">
                            {topicData.length > 0 ? (
                                <ResponsiveContainer width="100%" height={300}>
                                    <BarChart data={topicData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }} layout="vertical">
                                        <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" />
                                        <XAxis type="number" tick={{fill: '#64748b', fontSize: 13}} axisLine={false} tickLine={false} />
                                        <YAxis type="category" dataKey="topic" tick={{fill: '#64748b', fontSize: 13, textTransform: 'capitalize'}} axisLine={false} tickLine={false} width={80} />
                                        <Tooltip cursor={{fill: '#f1f5f9'}} contentStyle={{ borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 10px 25px -5px rgba(0,0,0,0.1)' }} />
                                        <Bar dataKey="review_count" name="Yorum Sayısı" fill="#3b82f6" radius={[0, 6, 6, 0]} />
                                    </BarChart>
                                </ResponsiveContainer>
                            ) : (
                                <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '100%', color: '#94a3b8' }}>
                                    <div style={{ fontSize: '48px', marginBottom: '16px' }}>📊</div>
                                    <p>Konu verisi bulunmuyor.</p>
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                <div className="overview-content" style={{ marginTop: '32px', gap: '32px', flexWrap: 'wrap' }}>
                    <div className="chart-card" style={{ flex: 2, minWidth: '600px' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                            <h2 style={{ margin: 0 }}>Sipariş Trendi (Zaman Bazlı)</h2>
                            <div style={{ display: 'flex', gap: '8px', background: '#f1f5f9', padding: '4px', borderRadius: '8px' }}>
                                <button 
                                    onClick={() => setTimePeriod('daily')} 
                                    style={{ padding: '6px 12px', border: 'none', background: timePeriod === 'daily' ? '#fff' : 'transparent', borderRadius: '6px', fontWeight: '600', color: timePeriod === 'daily' ? '#2563eb' : '#64748b', cursor: 'pointer', boxShadow: timePeriod === 'daily' ? '0 1px 3px rgba(0,0,0,0.1)' : 'none', transition: 'all 0.2s' }}
                                >Günlük</button>
                                <button 
                                    onClick={() => setTimePeriod('weekly')}
                                    style={{ padding: '6px 12px', border: 'none', background: timePeriod === 'weekly' ? '#fff' : 'transparent', borderRadius: '6px', fontWeight: '600', color: timePeriod === 'weekly' ? '#2563eb' : '#64748b', cursor: 'pointer', boxShadow: timePeriod === 'weekly' ? '0 1px 3px rgba(0,0,0,0.1)' : 'none', transition: 'all 0.2s' }}
                                >Haftalık</button>
                                <button 
                                    onClick={() => setTimePeriod('monthly')}
                                    style={{ padding: '6px 12px', border: 'none', background: timePeriod === 'monthly' ? '#fff' : 'transparent', borderRadius: '6px', fontWeight: '600', color: timePeriod === 'monthly' ? '#2563eb' : '#64748b', cursor: 'pointer', boxShadow: timePeriod === 'monthly' ? '0 1px 3px rgba(0,0,0,0.1)' : 'none', transition: 'all 0.2s' }}
                                >Aylık</button>
                            </div>
                        </div>
                        <div className="chart-container">
                            {timeData.length > 0 ? (
                                <ResponsiveContainer width="100%" height={300}>
                                    <ComposedChart data={timeData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                                        <defs>
                                            <linearGradient id="colorOrders" x1="0" y1="0" x2="0" y2="1">
                                                <stop offset="5%" stopColor="#2563eb" stopOpacity={0.3}/>
                                                <stop offset="95%" stopColor="#2563eb" stopOpacity={0}/>
                                            </linearGradient>
                                            <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                                                <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                                                <stop offset="95%" stopColor="#10b981" stopOpacity={0.2}/>
                                            </linearGradient>
                                        </defs>
                                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                                        <XAxis dataKey="displayPeriod" tick={{fill: '#64748b', fontSize: 13}} axisLine={false} tickLine={false} />
                                        <YAxis yAxisId="left" tick={{fill: '#64748b', fontSize: 13}} axisLine={false} tickLine={false} />
                                        <YAxis yAxisId="right" orientation="right" tick={{fill: '#10b981', fontSize: 13}} axisLine={false} tickLine={false} tickFormatter={(value) => `₺${value > 1000 ? (value/1000).toFixed(1) + 'k' : value}`} />
                                        <Tooltip contentStyle={{ borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 10px 25px -5px rgba(0,0,0,0.1)' }} />
                                        <Legend wrapperStyle={{ paddingTop: '10px' }} iconType="circle" />
                                        <Bar yAxisId="right" dataKey="total_revenue" name="Ciro (₺)" fill="url(#colorRevenue)" radius={[6, 6, 0, 0]} maxBarSize={40} />
                                        <Line yAxisId="left" type="monotone" dataKey="total_orders" name="Sipariş Sayısı" stroke="#2563eb" strokeWidth={3} dot={{r: 4, fill: '#2563eb', strokeWidth: 2, stroke: '#fff'}} activeDot={{r: 6}} />
                                    </ComposedChart>
                                </ResponsiveContainer>
                            ) : (
                                <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '100%', color: '#94a3b8' }}>
                                    <div style={{ fontSize: '48px', marginBottom: '16px' }}>📅</div>
                                    <p>Sipariş verisi bulunmuyor.</p>
                                </div>
                            )}
                        </div>
                    </div>

                    <div className="chart-card" style={{ flex: 1, minWidth: '400px' }}>
                        <h2>Platformlara Göre Satış</h2>
                        <div className="chart-container">
                            {platformData.length > 0 ? (
                                <ResponsiveContainer width="100%" height={300}>
                                    <BarChart data={platformData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                                        <XAxis dataKey="platform" tick={{fill: '#64748b', fontSize: 13, textTransform: 'capitalize'}} axisLine={false} tickLine={false} />
                                        <YAxis tick={{fill: '#64748b', fontSize: 13}} axisLine={false} tickLine={false} />
                                        <Tooltip cursor={{fill: '#f1f5f9'}} contentStyle={{ borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 10px 25px -5px rgba(0,0,0,0.1)' }} />
                                        <Bar dataKey="total_revenue" name="Toplam Ciro (₺)" fill="#10b981" radius={[6, 6, 0, 0]} />
                                    </BarChart>
                                </ResponsiveContainer>
                            ) : (
                                <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '100%', color: '#94a3b8' }}>
                                    <div style={{ fontSize: '48px', marginBottom: '16px' }}>🏬</div>
                                    <p>Platform verisi bulunmuyor.</p>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};
