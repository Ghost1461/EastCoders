// Vite HMR trigger comment
import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useLocation } from 'react-router-dom';
import './ProductsPage.css';

export const ProductsPage = () => {
    const { user, logout } = useAuth();
    const location = useLocation();
    const [searchTerm, setSearchTerm] = useState('');

    const mockProducts = [
        { 
            id: 1, 
            name: "Kablosuz Kulaklık Pro", 
            category: "Elektronik", 
            stock: 45, 
            status: "Aktif",
            image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=150&q=80",
            platforms: [{ name: "Trendyol", price: "₺1,299" }, { name: "Hepsiburada", price: "₺1,350" }]
        },
        { 
            id: 2, 
            name: "Akıllı Saat Series 5", 
            category: "Giyilebilir", 
            stock: 12, 
            status: "Aktif",
            image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=150&q=80",
            platforms: [{ name: "Amazon", price: "₺2,499" }, { name: "Kendi Sitemiz", price: "₺2,300" }]
        },
        { 
            id: 3, 
            name: "Ergonomik Ofis Koltuğu", 
            category: "Mobilya", 
            stock: 0, 
            status: "Tükendi",
            image: "https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?w=150&q=80",
            platforms: [{ name: "Trendyol", price: "₺3,850" }]
        },
        { 
            id: 4, 
            name: "Mekanik Oyuncu Klavyesi", 
            category: "Elektronik", 
            stock: 28, 
            status: "Aktif",
            image: "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=150&q=80",
            platforms: [{ name: "Hepsiburada", price: "₺899" }]
        },
        { 
            id: 5, 
            name: "4K Ultra HD Monitör", 
            category: "Elektronik", 
            stock: 5, 
            status: "Düşük Stok",
            image: "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=150&q=80",
            platforms: [{ name: "Amazon", price: "₺6,499" }, { name: "Trendyol", price: "₺6,700" }, { name: "Kendi Sitemiz", price: "₺6,200" }]
        },
    ];

    const filteredProducts = mockProducts.filter(product => 
        product.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
        product.category.toLowerCase().includes(searchTerm.toLowerCase())
    );

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

            <main className="dashboard-main">
                <div className="products-header-top">
                    <h1>Ürünlerim</h1>
                    <button className="add-product-btn">+ Yeni Ürün Ekle</button>
                </div>

                <div className="products-controls">
                    <div className="search-bar">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="search-icon">
                            <circle cx="11" cy="11" r="8"></circle>
                            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                        </svg>
                        <input 
                            type="text" 
                            placeholder="Ürün adı veya kategori ara..." 
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                </div>

                <div className="products-table-container">
                    <table className="products-table">
                        <thead>
                            <tr>
                                <th>Ürün Görseli</th>
                                <th>Ürün Adı & Kategori</th>
                                <th>Satış Platformları</th>
                                <th>Fiyatlar</th>
                                <th>Stok Durumu</th>
                                <th>İşlemler</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredProducts.length > 0 ? (
                                filteredProducts.map(product => (
                                    <tr key={product.id}>
                                        <td>
                                            <img src={product.image} alt={product.name} className="product-thumbnail" />
                                        </td>
                                        <td>
                                            <div className="product-name-col">
                                                <span className="product-title">{product.name}</span>
                                                <span className="product-category">{product.category}</span>
                                            </div>
                                        </td>
                                        <td>
                                            <div className="platform-list">
                                                {product.platforms.map((p, i) => (
                                                    <div key={i} className="platform-row">
                                                        <span className="platform-tag">{p.name}</span>
                                                    </div>
                                                ))}
                                            </div>
                                        </td>
                                        <td>
                                            <div className="price-list">
                                                {product.platforms.map((p, i) => (
                                                    <div key={i} className="price-row">
                                                        <span className="product-price">{p.price}</span>
                                                    </div>
                                                ))}
                                            </div>
                                        </td>
                                        <td>
                                            <div className="stock-info">
                                                <span className={`status-badge status-${product.status === 'Aktif' ? 'active' : product.status === 'Tükendi' ? 'out' : 'low'}`}>
                                                    {product.status}
                                                </span>
                                                <span className="stock-count">{product.stock} adet</span>
                                            </div>
                                        </td>
                                        <td>
                                            <button className="action-btn edit-btn">Düzenle</button>
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="6" style={{ textAlign: 'center', padding: '40px', color: '#64748b' }}>
                                        Aramanızla eşleşen ürün bulunamadı.
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </main>
        </div>
    );
};
