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
    const [categories, setCategories] = useState([]);
    const [brands, setBrands] = useState([]);
    const [colors, setColors] = useState([]);
    const [genders, setGenders] = useState([]);

    const [selectedCategory, setSelectedCategory] = useState(null);
    const [filters, setFilters] = useState({
        platform: '',
        brand: '',
        color: '',
        gender: '',
        size: '',
        status: ''
    });

    const [activeRanking, setActiveRanking] = useState(null);
    const RANKING_FILTERS = [
        { label: 'Tümü', endpoint: null },
        { label: 'En Çok Yorum Alanlar', endpoint: '/products_display/ranking/most-reviewed' },
        { label: 'En Yüksek Puanlılar', endpoint: '/products_display/ranking/top-rated' },
        { label: 'En Düşük Puanlılar', endpoint: '/products_display/ranking/lowest-rated' },
        { label: 'En Az Yorum Alanlar', endpoint: '/products_display/ranking/least-reviewed' },
        { label: 'Stoku Azalanlar', endpoint: '/products_display/stock/low' }
    ];

    const handleRankingClick = (endpoint) => {
        setActiveRanking(endpoint);
        if (endpoint) {
            setSearchTerm('');
            setSelectedCategory(null);
            setFilters({ platform: '', brand: '', color: '', gender: '', size: '', status: '' });
        }
    };

    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchOptions = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) return;
                
                const fetchOpts = async (path) => {
                    const res = await fetch(`http://localhost:8000/products_display/options/${path}`, {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (res.ok) {
                        const data = await res.json();
                        return data[path];
                    }
                    return [];
                };

                const [cats, brnds, clrs, gndrs] = await Promise.all([
                    fetchOpts('categories'),
                    fetchOpts('brands'),
                    fetchOpts('colors'),
                    fetchOpts('genders')
                ]);

                const ALL_CATEGORIES = ["Kapüşonlu", "T-Shirt", "Pantolon", "Şapka", "Elbise", "Ceket", "Çorap"];
                setCategories(ALL_CATEGORIES);
                setBrands(brnds || []);
                setColors(clrs || []);
                setGenders(gndrs || []);
            } catch (e) { console.error(e); }
        };
        fetchOptions();
    }, []);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                setLoading(true);
                const token = localStorage.getItem('token');
                if (!token) return;

                let url = 'http://localhost:8000/products_display/all';
                
                const hasFilters = selectedCategory || Object.values(filters).some(v => v !== '');

                if (activeRanking) {
                    url = `http://localhost:8000${activeRanking}`;
                } else if (searchTerm.trim() !== '') {
                    url = `http://localhost:8000/products_display/search/name?q=${encodeURIComponent(searchTerm)}`;
                } else if (hasFilters) {
                    const params = new URLSearchParams();
                    if (selectedCategory) params.append('category', selectedCategory);
                    if (filters.platform) params.append('platform', filters.platform);
                    if (filters.brand) params.append('brand', filters.brand);
                    if (filters.color) params.append('color', filters.color);
                    if (filters.gender) params.append('gender', filters.gender);
                    if (filters.size) params.append('size', filters.size);
                    if (filters.status) params.append('status', filters.status);
                    
                    url = `http://localhost:8000/products_display/filter?${params.toString()}`;
                }

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
                                    listing_id: listing.listing_id,
                                    name: prod.name || "İsimsiz Ürün",
                                    category: prod.category || "Diğer",
                                    stock: listing.stock,
                                    status: listing.status === 'Active' || listing.status === 'Aktif' ? 'Aktif' : (listing.stock > 0 ? 'Aktif' : 'Tükendi'),
                                    image: prod.image_url 
                                        ? (prod.image_url.startsWith('/') ? `http://localhost:8000${prod.image_url}` : prod.image_url)
                                        : "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=150&q=80",
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
    }, [searchTerm, selectedCategory, filters, activeRanking]);

    return (
        <div className="dashboard-container">
            <Navbar />

            <main className="dashboard-main">
                <div className="products-header-top" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '24px', flex: 1 }}>
                        <h1 style={{ margin: 0 }}>Ürünlerim</h1>
                        <div className="search-bar" style={{ flex: 1, maxWidth: '600px', display: 'flex', alignItems: 'center', background: '#fff', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '10px 16px' }}>
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: '8px' }}>
                                <circle cx="11" cy="11" r="8"></circle>
                                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                            </svg>
                            <input
                                type="text"
                                placeholder="Ürün adı veya kategori ara..."
                                value={searchTerm}
                                onChange={(e) => {
                                    setSearchTerm(e.target.value);
                                    setActiveRanking(null);
                                }}
                                style={{ border: 'none', outline: 'none', width: '100%', background: 'transparent' }}
                            />
                        </div>
                    </div>
                </div>

                <div className="advanced-filters" style={{ display: 'flex', gap: '15px', flexWrap: 'wrap', marginBottom: '10px' }}>
                    <select value={activeRanking || ''} onChange={e => handleRankingClick(e.target.value || null)} style={{ padding: '8px 12px', borderRadius: '8px', border: '1px solid #e2e8f0', background: '#fff', color: '#475569', outline: 'none', cursor: 'pointer', fontWeight: 'bold' }}>
                        <option value="">Sıralama Seçin</option>
                        {RANKING_FILTERS.filter(rf => rf.endpoint !== null).map(rf => (
                            <option key={rf.label} value={rf.endpoint}>{rf.label}</option>
                        ))}
                    </select>

                    <select value={filters.platform} onChange={e => setFilters({...filters, platform: e.target.value})} style={{ padding: '8px 12px', borderRadius: '8px', border: '1px solid #e2e8f0', background: '#fff', color: '#475569', outline: 'none', cursor: 'pointer' }}>
                        <option value="">Tüm Platformlar</option>
                        <option value="trendyol">Trendyol</option>
                        <option value="hepsiburada">Hepsiburada</option>
                        <option value="amazon">Amazon</option>
                    </select>

                    <select value={filters.brand} onChange={e => setFilters({...filters, brand: e.target.value})} style={{ padding: '8px 12px', borderRadius: '8px', border: '1px solid #e2e8f0', background: '#fff', color: '#475569', outline: 'none', cursor: 'pointer' }}>
                        <option value="">Tüm Markalar</option>
                        {brands.map(b => <option key={b} value={b}>{b}</option>)}
                    </select>

                    <select value={filters.color} onChange={e => setFilters({...filters, color: e.target.value})} style={{ padding: '8px 12px', borderRadius: '8px', border: '1px solid #e2e8f0', background: '#fff', color: '#475569', outline: 'none', cursor: 'pointer' }}>
                        <option value="">Tüm Renkler</option>
                        {colors.map(c => <option key={c} value={c}>{c}</option>)}
                    </select>

                    <select value={filters.gender} onChange={e => setFilters({...filters, gender: e.target.value})} style={{ padding: '8px 12px', borderRadius: '8px', border: '1px solid #e2e8f0', background: '#fff', color: '#475569', outline: 'none', cursor: 'pointer' }}>
                        <option value="">Tüm Cinsiyetler</option>
                        {genders.map(g => <option key={g} value={g}>{g}</option>)}
                    </select>

                    <select value={filters.size} onChange={e => setFilters({...filters, size: e.target.value})} style={{ padding: '8px 12px', borderRadius: '8px', border: '1px solid #e2e8f0', background: '#fff', color: '#475569', outline: 'none', cursor: 'pointer' }}>
                        <option value="">Tüm Bedenler</option>
                        {['S', 'M', 'L', 'XL', 'XXL'].map(s => <option key={s} value={s}>{s}</option>)}
                    </select>
                    
                    <select value={filters.status} onChange={e => setFilters({...filters, status: e.target.value})} style={{ padding: '8px 12px', borderRadius: '8px', border: '1px solid #e2e8f0', background: '#fff', color: '#475569', outline: 'none', cursor: 'pointer' }}>
                        <option value="">Tüm Durumlar</option>
                        <option value="Aktif">Aktif</option>
                        <option value="Stokta Yok">Stokta Yok</option>
                    </select>
                </div>

                <div className="category-filter-bar" style={{ display: 'flex', gap: '20px', padding: '10px 0 15px', overflowX: 'auto', borderBottom: '1px solid #e2e8f0', marginBottom: '20px', whiteSpace: 'nowrap' }}>
                    <button
                        onClick={() => setSelectedCategory(null)}
                        style={{ background: 'none', border: 'none', padding: '0 0 8px 0', borderBottom: selectedCategory === null ? '2px solid #f27a1a' : '2px solid transparent', color: selectedCategory === null ? '#f27a1a' : '#64748b', fontWeight: selectedCategory === null ? '600' : '500', cursor: 'pointer', transition: 'all 0.2s' }}
                    >
                        Tümü
                    </button>
                    {categories.map(cat => (
                        <button
                            key={cat}
                            onClick={() => setSelectedCategory(cat)}
                            style={{ background: 'none', border: 'none', padding: '0 0 8px 0', borderBottom: selectedCategory === cat ? '2px solid #f27a1a' : '2px solid transparent', color: selectedCategory === cat ? '#f27a1a' : '#64748b', fontWeight: selectedCategory === cat ? '600' : '500', cursor: 'pointer', transition: 'all 0.2s' }}
                        >
                            {cat}
                        </button>
                    ))}
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
                                            <Link to={`/product/${product.listing_id}`} className="action-btn edit-btn" style={{ textDecoration: 'none', display: 'inline-block', textAlign: 'center' }}>
                                                İncele
                                            </Link>
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
