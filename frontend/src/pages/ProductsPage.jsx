// Vite HMR trigger comment
import { useAuth } from '../context/AuthContext';
import { Link, useLocation } from 'react-router-dom';
import './ProductsPage.css';

export const ProductsPage = () => {
    const { user, logout } = useAuth();
    const location = useLocation();

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
                <div className="products-header-top">
                    <h1>Ürünlerim</h1>
                    <button className="add-product-btn">+ Yeni Ürün Ekle</button>
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
                            {mockProducts.map(product => (
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
                            ))}
                        </tbody>
                    </table>
                </div>
            </main>
        </div>
    );
};
