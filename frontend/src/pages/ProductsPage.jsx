// Vite HMR trigger comment
import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useLocation } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import './ProductsPage.css';

export const ProductsPage = () => {
    const { user, logout } = useAuth();
    const location = useLocation();
    const [searchTerm, setSearchTerm] = useState('');

    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                setLoading(true);
                const token = localStorage.getItem('token');
                if (!token) return;

                const url = searchTerm.trim() === '' 
                    ? 'http://localhost:8000/products_display/all' 
                    : `http://localhost:8000/products_display/search/name?q=${encodeURIComponent(searchTerm)}`;

                const response = await fetch(url, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    
                    const groupedProducts = {};
                    
                    if (data && data.products) {
                        data.products.forEach(listing => {
                            const prod = listing.product;
                            if (!prod) return;
                            
                            if (!groupedProducts[prod.id]) {
                                groupedProducts[prod.id] = {
                                    id: prod.id,
                                    name: prod.name || "İsimsiz Ürün",
                                    category: prod.category || "Diğer",
                                    stock: listing.stock,
                                    status: listing.status === 'Active' || listing.status === 'Aktif' ? 'Aktif' : (listing.stock > 0 ? 'Aktif' : 'Tükendi'),
                                    image: prod.image_url || "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=150&q=80",
                                    platforms: []
                                };
                            } else {
                                groupedProducts[prod.id].stock += listing.stock;
                            }
                            
                            groupedProducts[prod.id].platforms.push({
                                name: listing.platform,
                                price: `₺${listing.price}`
                            });
                        });
                        
                        setProducts(Object.values(groupedProducts));
                    } else {
                        setProducts([]);
                    }
                }
            } catch (error) {
                console.error("Ürünler çekilirken hata oluştu:", error);
            } finally {
                setLoading(false);
            }
        };

        const delayDebounceFn = setTimeout(() => {
            fetchProducts();
        }, 500);

        return () => clearTimeout(delayDebounceFn);
    }, [searchTerm]);

    return (
        <div className="dashboard-container">
            <Navbar />

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
                            {loading ? (
                                <tr>
                                    <td colSpan="6" style={{ textAlign: 'center', padding: '40px', color: '#64748b' }}>
                                        Ürünler yükleniyor...
                                    </td>
                                </tr>
                            ) : products.length > 0 ? (
                                products.map(product => (
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
                                        Kayıtlı ürününüz bulunmamaktadır. Aktarma sayfasından ürün ekleyebilirsiniz.
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
