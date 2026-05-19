import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useLocation } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer, Cell, PieChart, Pie } from 'recharts';
import api from '../api/client';
import { Navbar } from '../components/Navbar';
import { CustomPeriodPicker } from '../components/CustomPeriodPicker';
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

    const [aiReports, setAiReports] = useState({
        recommendations: { data: null, loading: false },
        stock: { data: null, loading: false },
        review: { data: null, loading: false }
    });
    const [activeReport, setActiveReport] = useState(null);

    const [periodSummary, setPeriodSummary] = useState({
        period: 'daily',
        value: '',
        data: null,
        loading: false,
        error: null
    });

    const fetchPeriodSummary = async () => {
        setPeriodSummary(prev => ({ ...prev, loading: true, error: null }));
        try {
            const token = localStorage.getItem('token');
            const res = await fetch(`http://localhost:8000/reports/ai/period-summary?period=${periodSummary.period}&value=${periodSummary.value}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                const data = await res.json();
                setPeriodSummary(prev => ({ ...prev, data, loading: false }));
            } else {
                const errorData = await res.json();
                let errMsg = 'Bu dönem için veri bulunamadı.';
                if (errorData && errorData.detail) {
                    if (typeof errorData.detail === 'string' && errorData.detail.includes('No data found')) {
                        errMsg = 'Seçilen dönem için henüz herhangi bir sipariş veya satış verisi bulunmuyor.';
                    } else {
                        errMsg = typeof errorData.detail === 'string' ? errorData.detail : errorData.detail.message || errMsg;
                    }
                }
                setPeriodSummary(prev => ({ ...prev, loading: false, error: errMsg }));
            }
        } catch (error) {
            console.error('Period summary error:', error);
            setPeriodSummary(prev => ({ ...prev, loading: false, error: 'Sunucuya bağlanılamadı.' }));
        }
    };

    const fetchAiReport = async (type, endpoint, title) => {
        setAiReports(prev => ({ ...prev, [type]: { ...prev[type], loading: true } }));
        try {
            const token = localStorage.getItem('token');
            const res = await fetch(`http://localhost:8000${endpoint}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                const data = await res.json();
                setAiReports(prev => ({ ...prev, [type]: { data, loading: false } }));
                setActiveReport({ title, data });
            } else {
                throw new Error("Failed to fetch");
            }
        } catch (error) {
            console.error(`${title} çekilirken hata oluştu:`, error);
            setAiReports(prev => ({ ...prev, [type]: { ...prev[type], loading: false } }));
        }
    };

    const formatMarkdownToJSX = (text) => {
        if (!text) return null;
        
        const lines = text.split('\n');
        let elements = [];
        let inList = false;
        let listItems = [];
        
        lines.forEach((line, index) => {
            line = line.trim();
            if (!line) {
                if (inList) {
                    elements.push(<ul key={`ul-${index}`} style={{ paddingLeft: '0', margin: '0 0 20px 0', display: 'flex', flexDirection: 'column', gap: '10px', listStyle: 'none' }}>{listItems}</ul>);
                    inList = false;
                    listItems = [];
                }
                return;
            }

            const formatBold = (str) => {
                const parts = str.split(/\*\*(.*?)\*\*/g);
                return parts.map((part, i) => i % 2 === 1 ? <strong key={i} style={{ color: '#0f172a', fontWeight: '700' }}>{part}</strong> : part);
            };

            const customHeaders = [
                "🔥 Öncelikli Aksiyonlar",
                "📈 Satış Artırma Önerileri",
                "⚠️ Riskli Alanlar",
                "🚀 Hızlı Kazanımlar",
                "🔥 En Kritik Problem",
                "😊 Pozitif İçgörüler",
                "⚠️ Riskli Konular",
                "💬 En Çok Geçen Konular",
                "🛠️ İyileştirme Önerileri"
            ];

            let isHeader = false;
            let headerText = line;

            if (line.startsWith('### ')) {
                isHeader = true;
                headerText = line.substring(4);
            } else if (line.startsWith('## ')) {
                isHeader = true;
                headerText = line.substring(3);
            } else if (customHeaders.some(header => line.startsWith(header))) {
                isHeader = true;
                headerText = line;
                if (headerText.endsWith(':')) headerText = headerText.slice(0, -1);
            }

            if (isHeader) {
                if (inList) {
                    elements.push(<ul key={`ul-${index}`} style={{ paddingLeft: '0', margin: '0 0 20px 0', display: 'flex', flexDirection: 'column', gap: '10px', listStyle: 'none' }}>{listItems}</ul>);
                    inList = false;
                    listItems = [];
                }
                elements.push(<h3 key={`h3-${index}`} style={{ color: '#1e293b', fontSize: '18px', marginTop: '28px', marginBottom: '16px', paddingBottom: '10px', borderBottom: '2px solid #f1f5f9' }}>{formatBold(headerText)}</h3>);
            } else if (line.startsWith('- ') || line.startsWith('* ')) {
                inList = true;
                listItems.push(
                    <li key={`li-${index}`} style={{ color: '#475569', fontSize: '15px', lineHeight: '1.7', display: 'flex', alignItems: 'flex-start' }}>
                        <span style={{ color: '#8b5cf6', marginRight: '12px', fontSize: '18px', lineHeight: '1.3' }}>•</span>
                        <span>{formatBold(line.substring(2))}</span>
                    </li>
                );
            } else if (line.match(/^\d+\.\s/)) {
                // Numbered list items support
                const numMatch = line.match(/^(\d+)\.\s/);
                inList = true;
                listItems.push(
                    <li key={`li-${index}`} style={{ color: '#475569', fontSize: '15px', lineHeight: '1.7', display: 'flex', alignItems: 'flex-start' }}>
                        <span style={{ color: '#8b5cf6', marginRight: '12px', fontWeight: 'bold' }}>{numMatch[1]}.</span>
                        <span>{formatBold(line.substring(numMatch[0].length))}</span>
                    </li>
                );
            } else {
                if (inList) {
                    elements.push(<ul key={`ul-${index}`} style={{ paddingLeft: '0', margin: '0 0 20px 0', display: 'flex', flexDirection: 'column', gap: '10px', listStyle: 'none' }}>{listItems}</ul>);
                    inList = false;
                    listItems = [];
                }
                elements.push(<p key={`p-${index}`} style={{ color: '#475569', fontSize: '15px', lineHeight: '1.7', margin: '0 0 16px 0' }}>{formatBold(line)}</p>);
            }
        });

        if (inList) {
            elements.push(<ul key={`ul-end`} style={{ paddingLeft: '0', margin: '0 0 20px 0', display: 'flex', flexDirection: 'column', gap: '10px', listStyle: 'none' }}>{listItems}</ul>);
        }

        return elements;
    };

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
            <Navbar />

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

                        <div className="ai-reports-section" style={{ marginTop: '48px', marginBottom: '48px' }}>
                            <h2 style={{ fontSize: '24px', color: '#0f172a', marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '10px', fontWeight: '700' }}>
                                <span style={{ fontSize: '28px' }}>🧠</span> Yapay Zeka Analizleri
                            </h2>
                            <div className="ai-cards-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '24px' }}>
                                {/* Recommendations Card */}
                                <div className="ai-card" style={{ background: 'linear-gradient(145deg, #ffffff, #f8fafc)', borderRadius: '20px', padding: '28px', border: '1px solid #e2e8f0', boxShadow: '0 10px 30px -10px rgba(0,0,0,0.05)', display: 'flex', flexDirection: 'column', transition: 'transform 0.3s, box-shadow 0.3s' }} onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-5px)'; e.currentTarget.style.boxShadow = '0 20px 40px -15px rgba(0,0,0,0.1)'; }} onMouseLeave={e => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = '0 10px 30px -10px rgba(0,0,0,0.05)'; }}>
                                    <div style={{ background: '#eff6ff', width: '56px', height: '56px', borderRadius: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '28px', marginBottom: '20px', boxShadow: '0 4px 12px rgba(59,130,246,0.15)' }}>💡</div>
                                    <h3 style={{ margin: '0 0 12px 0', color: '#1e293b', fontSize: '19px', fontWeight: '700' }}>Satış & Büyüme Önerileri</h3>
                                    <p style={{ color: '#64748b', fontSize: '15px', lineHeight: '1.6', flex: 1, margin: '0 0 24px 0' }}>Mağazanızın genel performansını artırmak için yapay zeka destekli stratejik aksiyon planları ve büyüme fırsatları.</p>
                                    <button 
                                        onClick={() => aiReports.recommendations.data ? setActiveReport({ title: 'Satış & Büyüme Önerileri', data: aiReports.recommendations.data }) : fetchAiReport('recommendations', '/reports/ai-recommendations', 'Satış & Büyüme Önerileri')}
                                        disabled={aiReports.recommendations.loading}
                                        style={{ width: '100%', padding: '14px', background: aiReports.recommendations.data ? '#f1f5f9' : '#3b82f6', color: aiReports.recommendations.data ? '#475569' : 'white', border: 'none', borderRadius: '12px', fontWeight: '600', fontSize: '15px', cursor: aiReports.recommendations.loading ? 'wait' : 'pointer', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '8px', transition: 'all 0.2s' }}
                                    >
                                        {aiReports.recommendations.loading ? <div style={{ width: '20px', height: '20px', border: '3px solid #ffffff', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 1s linear infinite' }}></div> : (aiReports.recommendations.data ? 'Raporu Görüntüle' : 'Analiz Et')}
                                    </button>
                                </div>

                                {/* Stock Analysis Card */}
                                <div className="ai-card" style={{ background: 'linear-gradient(145deg, #ffffff, #f8fafc)', borderRadius: '20px', padding: '28px', border: '1px solid #e2e8f0', boxShadow: '0 10px 30px -10px rgba(0,0,0,0.05)', display: 'flex', flexDirection: 'column', transition: 'transform 0.3s, box-shadow 0.3s' }} onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-5px)'; e.currentTarget.style.boxShadow = '0 20px 40px -15px rgba(0,0,0,0.1)'; }} onMouseLeave={e => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = '0 10px 30px -10px rgba(0,0,0,0.05)'; }}>
                                    <div style={{ background: '#fef3c7', width: '56px', height: '56px', borderRadius: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '28px', marginBottom: '20px', boxShadow: '0 4px 12px rgba(245,158,11,0.15)' }}>📦</div>
                                    <h3 style={{ margin: '0 0 12px 0', color: '#1e293b', fontSize: '19px', fontWeight: '700' }}>Akıllı Stok Analizi</h3>
                                    <p style={{ color: '#64748b', fontSize: '15px', lineHeight: '1.6', flex: 1, margin: '0 0 24px 0' }}>Hangi ürünlerin stoğunun kritik seviyede olduğunu ve hangi kategorilerde potansiyel kaybı yaşadığınızı tespit edin.</p>
                                    <button 
                                        onClick={() => aiReports.stock.data ? setActiveReport({ title: 'Akıllı Stok Analizi', data: aiReports.stock.data }) : fetchAiReport('stock', '/reports/ai-stock-analysis', 'Akıllı Stok Analizi')}
                                        disabled={aiReports.stock.loading}
                                        style={{ width: '100%', padding: '14px', background: aiReports.stock.data ? '#f1f5f9' : '#f59e0b', color: aiReports.stock.data ? '#475569' : 'white', border: 'none', borderRadius: '12px', fontWeight: '600', fontSize: '15px', cursor: aiReports.stock.loading ? 'wait' : 'pointer', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '8px', transition: 'all 0.2s' }}
                                    >
                                        {aiReports.stock.loading ? <div style={{ width: '20px', height: '20px', border: '3px solid #ffffff', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 1s linear infinite' }}></div> : (aiReports.stock.data ? 'Raporu Görüntüle' : 'Analiz Et')}
                                    </button>
                                </div>

                                {/* Review Analysis Card */}
                                <div className="ai-card" style={{ background: 'linear-gradient(145deg, #ffffff, #f8fafc)', borderRadius: '20px', padding: '28px', border: '1px solid #e2e8f0', boxShadow: '0 10px 30px -10px rgba(0,0,0,0.05)', display: 'flex', flexDirection: 'column', transition: 'transform 0.3s, box-shadow 0.3s' }} onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-5px)'; e.currentTarget.style.boxShadow = '0 20px 40px -15px rgba(0,0,0,0.1)'; }} onMouseLeave={e => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = '0 10px 30px -10px rgba(0,0,0,0.05)'; }}>
                                    <div style={{ background: '#fce7f3', width: '56px', height: '56px', borderRadius: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '28px', marginBottom: '20px', boxShadow: '0 4px 12px rgba(236,72,153,0.15)' }}>⭐</div>
                                    <h3 style={{ margin: '0 0 12px 0', color: '#1e293b', fontSize: '19px', fontWeight: '700' }}>Müşteri Geri Bildirim Analizi</h3>
                                    <p style={{ color: '#64748b', fontSize: '15px', lineHeight: '1.6', flex: 1, margin: '0 0 24px 0' }}>Müşteri yorumlarından elde edilen derin içgörülerle memnuniyeti artırma ve ürün geliştirme stratejileri oluşturun.</p>
                                    <button 
                                        onClick={() => aiReports.review.data ? setActiveReport({ title: 'Müşteri Geri Bildirim Analizi', data: aiReports.review.data }) : fetchAiReport('review', '/reports/ai-review-analysis', 'Müşteri Geri Bildirim Analizi')}
                                        disabled={aiReports.review.loading}
                                        style={{ width: '100%', padding: '14px', background: aiReports.review.data ? '#f1f5f9' : '#ec4899', color: aiReports.review.data ? '#475569' : 'white', border: 'none', borderRadius: '12px', fontWeight: '600', fontSize: '15px', cursor: aiReports.review.loading ? 'wait' : 'pointer', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '8px', transition: 'all 0.2s' }}
                                    >
                                        {aiReports.review.loading ? <div style={{ width: '20px', height: '20px', border: '3px solid #ffffff', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 1s linear infinite' }}></div> : (aiReports.review.data ? 'Raporu Görüntüle' : 'Analiz Et')}
                                    </button>
                                </div>
                            </div>
                        </div>

                        {/* Dönemsel Analiz Bölümü */}
                        <div className="period-summary-section" style={{ marginTop: '48px', marginBottom: '48px', background: '#ffffff', borderRadius: '24px', padding: '36px', boxShadow: '0 15px 40px -10px rgba(0,0,0,0.08)', border: '1px solid #e2e8f0' }}>
                            <h2 style={{ fontSize: '24px', color: '#0f172a', marginBottom: '32px', display: 'flex', alignItems: 'center', gap: '12px', fontWeight: '800' }}>
                                <span style={{ fontSize: '28px', background: '#f5f3ff', padding: '8px', borderRadius: '12px', color: '#8b5cf6' }}>📅</span> 
                                Dönemsel Yapay Zeka Özeti
                            </h2>
                            <div style={{ display: 'flex', gap: '48px', flexWrap: 'wrap' }}>
                                {/* Sol: Dönem Tipi */}
                                <div style={{ flex: '1', minWidth: '250px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
                                    <h3 style={{ fontSize: '15px', color: '#64748b', margin: '0', textTransform: 'uppercase', letterSpacing: '1px', fontWeight: '700' }}>Dönem Tipi</h3>
                                    {['daily', 'weekly', 'monthly'].map(p => (
                                        <button 
                                            key={p}
                                            onClick={() => setPeriodSummary(prev => ({ ...prev, period: p, value: '', data: null, error: null }))}
                                            style={{ 
                                                padding: '16px 24px', 
                                                background: periodSummary.period === p ? '#eff6ff' : '#f8fafc', 
                                                border: `2px solid ${periodSummary.period === p ? '#3b82f6' : '#e2e8f0'}`,
                                                borderRadius: '16px',
                                                color: periodSummary.period === p ? '#1d4ed8' : '#475569',
                                                fontWeight: periodSummary.period === p ? '700' : '600',
                                                fontSize: '16px',
                                                textAlign: 'left',
                                                cursor: 'pointer',
                                                transition: 'all 0.2s',
                                                display: 'flex',
                                                justifyContent: 'space-between',
                                                alignItems: 'center',
                                                boxShadow: periodSummary.period === p ? '0 4px 12px rgba(59,130,246,0.1)' : 'none'
                                            }}
                                        >
                                            {p === 'daily' ? 'Günlük Analiz' : p === 'weekly' ? 'Haftalık Analiz' : 'Aylık Analiz'}
                                            {periodSummary.period === p && <span style={{ color: '#3b82f6', fontSize: '20px' }}>✓</span>}
                                        </button>
                                    ))}
                                </div>

                                {/* Sağ: Tarih ve Sonuç */}
                                <div style={{ flex: '2', minWidth: '350px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
                                    <h3 style={{ fontSize: '15px', color: '#64748b', margin: '0', textTransform: 'uppercase', letterSpacing: '1px', fontWeight: '700' }}>Tarih Seçin</h3>
                                    <div style={{ display: 'flex', gap: '16px', alignItems: 'center', flexWrap: 'wrap' }}>
                                        <CustomPeriodPicker 
                                            period={periodSummary.period} 
                                            value={periodSummary.value} 
                                            onChange={(val) => setPeriodSummary(prev => ({ ...prev, value: val, error: null }))} 
                                        />
                                        <button 
                                            onClick={fetchPeriodSummary}
                                            disabled={!periodSummary.value || periodSummary.loading}
                                            style={{ 
                                                padding: '16px 32px', 
                                                background: (!periodSummary.value || periodSummary.loading) ? '#cbd5e1' : '#8b5cf6', 
                                                color: 'white', 
                                                border: 'none', 
                                                borderRadius: '16px', 
                                                fontWeight: '700',
                                                fontSize: '16px',
                                                cursor: (!periodSummary.value || periodSummary.loading) ? 'not-allowed' : 'pointer',
                                                transition: 'all 0.2s',
                                                display: 'flex',
                                                alignItems: 'center',
                                                gap: '10px',
                                                boxShadow: (!periodSummary.value || periodSummary.loading) ? 'none' : '0 4px 15px rgba(139,92,246,0.3)'
                                            }}
                                        >
                                            {periodSummary.loading ? <div style={{ width: '22px', height: '22px', border: '3px solid rgba(255,255,255,0.3)', borderTopColor: 'white', borderRadius: '50%', animation: 'spin 1s linear infinite' }}></div> : '🚀 Özeti Çıkar'}
                                        </button>
                                    </div>

                                    {periodSummary.error && (
                                        <div style={{ marginTop: '16px', color: '#b91c1c', fontSize: '15px', background: '#fef2f2', padding: '16px 20px', borderRadius: '12px', border: '1px solid #fecaca', display: 'flex', alignItems: 'center', gap: '12px' }}>
                                            <span style={{ fontSize: '20px' }}>⚠️</span>
                                            {periodSummary.error}
                                        </div>
                                    )}

                                    {periodSummary.data && !periodSummary.loading && (
                                        <div style={{ marginTop: '24px', padding: '32px', background: '#f8fafc', borderRadius: '20px', border: '1px solid #e2e8f0', maxHeight: '500px', overflowY: 'auto' }}>
                                            {formatMarkdownToJSX(periodSummary.data.ai)}
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>


                    </>
                )}
            </main>
            
            {activeReport && (
                <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', background: 'rgba(15, 23, 42, 0.6)', zIndex: 1000, display: 'flex', justifyContent: 'center', alignItems: 'center', backdropFilter: 'blur(8px)', padding: '20px' }}>
                    <div style={{ background: '#ffffff', borderRadius: '24px', width: '100%', maxWidth: '800px', maxHeight: '90vh', overflow: 'hidden', boxShadow: '0 25px 50px -12px rgba(0,0,0,0.4)', display: 'flex', flexDirection: 'column', animation: 'modalSlideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1)' }}>
                        
                        {/* Header Gradient */}
                        <div style={{ background: 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)', padding: '24px 32px', borderBottom: '1px solid #e2e8f0', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                                <div style={{ background: 'white', padding: '12px', borderRadius: '16px', boxShadow: '0 4px 12px rgba(0,0,0,0.05)', fontSize: '24px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>✨</div>
                                <div>
                                    <h2 style={{ margin: 0, color: '#0f172a', fontSize: '22px', fontWeight: '800' }}>{activeReport.title}</h2>
                                    <p style={{ margin: '4px 0 0 0', color: '#64748b', fontSize: '13px', fontWeight: '500' }}>Yapay Zeka Destekli İçgörü</p>
                                </div>
                            </div>
                            <button onClick={() => setActiveReport(null)} style={{ background: 'white', border: '1px solid #e2e8f0', width: '40px', height: '40px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', color: '#64748b', transition: 'all 0.2s', boxShadow: '0 2px 5px rgba(0,0,0,0.02)' }} onMouseEnter={e => { e.currentTarget.style.background = '#f8fafc'; e.currentTarget.style.color = '#0f172a'; }} onMouseLeave={e => { e.currentTarget.style.background = 'white'; e.currentTarget.style.color = '#64748b'; }}>
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                            </button>
                        </div>
                        
                        {/* Content Area */}
                        <div style={{ padding: '32px', overflowY: 'auto', background: '#ffffff' }}>
                            {activeReport.data?.ai ? (
                                <div style={{ background: '#f8fafc', padding: '24px', borderRadius: '16px', border: '1px solid #f1f5f9' }}>
                                    {formatMarkdownToJSX(activeReport.data.ai)}
                                </div>
                            ) : (
                                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '60px 0', color: '#ef4444' }}>
                                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginBottom: '16px' }}><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                                    <h3 style={{ margin: '0 0 8px 0' }}>Rapor Yüklenemedi</h3>
                                    <p style={{ margin: 0, color: '#64748b' }}>Sistemle iletişim kurulurken bir sorun oluştu.</p>
                                </div>
                            )}
                        </div>
                        
                        {/* Footer Action (Optional) */}
                        <div style={{ padding: '20px 32px', background: '#ffffff', borderTop: '1px solid #f1f5f9', display: 'flex', justifyContent: 'flex-end' }}>
                            <button onClick={() => setActiveReport(null)} style={{ background: '#3b82f6', color: 'white', border: 'none', padding: '12px 28px', borderRadius: '10px', fontWeight: '600', fontSize: '14px', cursor: 'pointer', transition: 'background 0.2s', boxShadow: '0 4px 12px rgba(59,130,246,0.3)' }} onMouseEnter={e => e.currentTarget.style.background = '#2563eb'} onMouseLeave={e => e.currentTarget.style.background = '#3b82f6'}>
                                Kapat
                            </button>
                        </div>
                        
                        <style>{`
                            @keyframes modalSlideUp { 0% { opacity: 0; transform: translateY(20px) scale(0.98); } 100% { opacity: 1; transform: translateY(0) scale(1); } }
                            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
                        `}</style>
                    </div>
                </div>
            )}
        </div>
    );
};
