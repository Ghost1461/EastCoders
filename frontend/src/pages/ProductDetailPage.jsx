import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import api from '../api/client';

export const ProductDetailPage = () => {
    const { listingId } = useParams();
    const [productDetail, setProductDetail] = useState(null);
    const [reviews, setReviews] = useState([]);
    const [loading, setLoading] = useState(true);

    const [reviewSummary, setReviewSummary] = useState(null);
    const [ratingDistribution, setRatingDistribution] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                // Fetch product details
                const detailRes = await api.get(`/products_display/detail/${listingId}`);
                setProductDetail(detailRes.data);

                // Fetch product reviews
                let reviewsRes;
                if (detailRes.data && detailRes.data.external_product_id) {
                    reviewsRes = await api.get(`/review_display/product/${detailRes.data.external_product_id}`);
                } else {
                    reviewsRes = await api.get(`/review_display/listing/${listingId}`);
                }
                
                if (reviewsRes.data && reviewsRes.data.reviews) {
                    setReviews(reviewsRes.data.reviews);
                }

                // Fetch general store review summary
                const [sumRes, distRes] = await Promise.all([
                    api.get('/review_display/summary'),
                    api.get('/review_display/rating-distribution')
                ]);
                setReviewSummary(sumRes.data);
                setRatingDistribution(distRes.data);
            } catch (error) {
                console.error("Veriler çekilemedi:", error);
            } finally {
                setLoading(false);
            }
        };

        if (listingId) {
            fetchData();
        }
    }, [listingId]);

    if (loading) {
        return (
            <div className="dashboard-container">
                <Navbar />
                <main className="dashboard-main" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 'calc(100vh - 100px)' }}>
                    <p style={{ color: '#64748b' }}>Ürün bilgileri yükleniyor...</p>
                </main>
            </div>
        );
    }

    if (!productDetail || productDetail.message === "Ürün bulunamadı") {
        return (
            <div className="dashboard-container">
                <Navbar />
                <main className="dashboard-main" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', minHeight: 'calc(100vh - 100px)' }}>
                    <h2 style={{ color: '#0f172a', marginBottom: '16px' }}>Ürün Bulunamadı</h2>
                    <Link to="/products" style={{ color: '#3b82f6', textDecoration: 'none' }}>&larr; Ürünlerime Dön</Link>
                </main>
            </div>
        );
    }

    const { product, platform, price, stock, status, rating, review_count } = productDetail;

    return (
        <div className="dashboard-container" style={{ background: '#f0f4f8' }}>
            <Navbar />
            <main className="dashboard-main" style={{ padding: '40px', maxWidth: '1400px', margin: '0 auto' }}>
                <div style={{ marginBottom: '30px' }}>
                    <Link to="/products" style={{ color: '#475569', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '8px', fontSize: '16px', fontWeight: '500', transition: 'color 0.2s' }} onMouseEnter={e => e.target.style.color = '#0f172a'} onMouseLeave={e => e.target.style.color = '#475569'}>
                        &larr; Ürünlerime Dön
                    </Link>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '40px' }}>
                    {/* Left Column: Product Info */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                        <div style={{ background: '#fff', padding: '32px', borderRadius: '24px', boxShadow: '0 20px 40px rgba(0,0,0,0.04)', display: 'flex', flexDirection: 'column', alignItems: 'center', border: '1px solid rgba(226, 232, 240, 0.8)' }}>
                            <div style={{ padding: '20px', background: '#f8fafc', borderRadius: '16px', marginBottom: '24px', width: '100%', display: 'flex', justifyContent: 'center' }}>
                                <img 
                                    src={product?.image_url || 'https://via.placeholder.com/400x500'} 
                                    alt={product?.name} 
                                    style={{ width: '100%', maxWidth: '250px', objectFit: 'contain', mixBlendMode: 'multiply' }}
                                />
                            </div>
                            <div style={{ width: '100%' }}>
                                <span style={{ padding: '6px 12px', background: '#eff6ff', color: '#2563eb', borderRadius: '12px', fontSize: '12px', fontWeight: 'bold', textTransform: 'uppercase', letterSpacing: '1px' }}>
                                    {product?.brand}
                                </span>
                                <h2 style={{ margin: '16px 0 24px 0', color: '#0f172a', fontSize: '24px', lineHeight: '1.3' }}>{product?.name}</h2>
                                
                                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px', background: '#f8fafc', borderRadius: '12px' }}>
                                        <span style={{ color: '#64748b', fontWeight: '500' }}>Platform</span>
                                        <strong style={{ textTransform: 'capitalize', color: '#0f172a' }}>{platform}</strong>
                                    </div>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px', background: '#f8fafc', borderRadius: '12px' }}>
                                        <span style={{ color: '#64748b', fontWeight: '500' }}>Fiyat</span>
                                        <strong style={{ color: '#0f172a', fontSize: '18px' }}>₺{price}</strong>
                                    </div>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px', background: '#f8fafc', borderRadius: '12px' }}>
                                        <span style={{ color: '#64748b', fontWeight: '500' }}>Stok</span>
                                        <strong style={{ color: '#0f172a' }}>{stock} Adet</strong>
                                    </div>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px', background: '#f8fafc', borderRadius: '12px' }}>
                                        <span style={{ color: '#64748b', fontWeight: '500' }}>Durum</span>
                                        <span style={{ color: status === 'Active' || status === 'Aktif' ? '#10b981' : '#ef4444', fontWeight: 'bold', padding: '4px 12px', background: status === 'Active' || status === 'Aktif' ? '#d1fae5' : '#fee2e2', borderRadius: '8px' }}>
                                            {status}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Right Column: Reviews */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                        
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
                            {/* Product Specific Rating */}
                            <div style={{ background: '#fff', padding: '32px', borderRadius: '24px', boxShadow: '0 20px 40px rgba(0,0,0,0.04)', border: '1px solid rgba(226, 232, 240, 0.8)' }}>
                                <h3 style={{ margin: '0 0 24px 0', color: '#0f172a', fontSize: '18px' }}>Bu Ürünün Puanı</h3>
                                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
                                    <div style={{ fontSize: '64px', fontWeight: '800', color: '#f59e0b', lineHeight: '1' }}>
                                        {rating || 0}
                                    </div>
                                    <div style={{ color: '#f59e0b', fontSize: '28px', letterSpacing: '4px' }}>
                                        {'★'.repeat(Math.round(rating || 0))}{'☆'.repeat(5 - Math.round(rating || 0))}
                                    </div>
                                    <div style={{ color: '#64748b', fontSize: '15px', marginTop: '4px', fontWeight: '500' }}>
                                        {review_count || 0} Değerlendirme
                                    </div>
                                </div>
                            </div>

                            {/* Store General Rating */}
                            {reviewSummary && (
                                <div style={{ background: 'linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%)', padding: '32px', borderRadius: '24px', boxShadow: '0 20px 40px rgba(59, 130, 246, 0.2)', color: '#fff' }}>
                                    <h3 style={{ margin: '0 0 24px 0', fontSize: '18px', fontWeight: '600', opacity: 0.9 }}>Mağaza Genel Ortalaması</h3>
                                    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
                                        <div style={{ fontSize: '64px', fontWeight: '800', lineHeight: '1' }}>
                                            {reviewSummary.average_rating ? reviewSummary.average_rating.toFixed(1) : 0}
                                        </div>
                                        <div style={{ fontSize: '28px', letterSpacing: '4px', color: '#fbbf24' }}>
                                            {'★'.repeat(Math.round(reviewSummary.average_rating || 0))}{'☆'.repeat(5 - Math.round(reviewSummary.average_rating || 0))}
                                        </div>
                                        <div style={{ fontSize: '15px', marginTop: '4px', fontWeight: '500', opacity: 0.9 }}>
                                            Toplam {reviewSummary.total_reviews} Değerlendirme
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* Store Ratings Distribution & Product Reviews */}
                        <div style={{ background: '#fff', padding: '32px', borderRadius: '24px', boxShadow: '0 20px 40px rgba(0,0,0,0.04)', border: '1px solid rgba(226, 232, 240, 0.8)', flex: 1, display: 'flex', flexDirection: 'column' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                                <h3 style={{ margin: 0, color: '#0f172a', fontSize: '20px' }}>Ürün Yorumları ({reviews.length})</h3>
                                {reviewSummary && (
                                    <div style={{ display: 'flex', gap: '12px' }}>
                                        <span style={{ padding: '6px 12px', background: '#dcfce7', color: '#166534', borderRadius: '20px', fontSize: '13px', fontWeight: '600' }}>
                                            👍 {reviewSummary.positive_count} Olumlu (Mağazanız)
                                        </span>
                                        <span style={{ padding: '6px 12px', background: '#fee2e2', color: '#991b1b', borderRadius: '20px', fontSize: '13px', fontWeight: '600' }}>
                                            👎 {reviewSummary.negative_count} Olumsuz (Mağazanız)
                                        </span>
                                        <span style={{ padding: '6px 12px', background: '#fef3c7', color: '#b45309', borderRadius: '20px', fontSize: '13px', fontWeight: '600' }}>
                                            😐 {reviewSummary.mixed_count} Nötr/Karma (Mağazanız)
                                        </span>
                                    </div>
                                )}
                            </div>
                            
                            {reviews.length === 0 ? (
                                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '60px 0', flex: 1 }}>
                                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#cbd5e1" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" style={{ marginBottom: '16px' }}>
                                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                                    </svg>
                                    <p style={{ color: '#94a3b8', fontSize: '16px', margin: 0 }}>Bu ürün için henüz yorum bulunmuyor.</p>
                                </div>
                            ) : (
                                <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', maxHeight: '600px', overflowY: 'auto', paddingRight: '12px', flex: 1 }}>
                                    {reviews.map(review => (
                                        <div key={review.id} style={{ padding: '24px', border: '1px solid #f1f5f9', borderRadius: '16px', background: '#f8fafc', transition: 'transform 0.2s', cursor: 'default' }} onMouseEnter={e => e.currentTarget.style.transform = 'translateY(-2px)'} onMouseLeave={e => e.currentTarget.style.transform = 'translateY(0)'}>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
                                                <div>
                                                    <div style={{ color: '#f59e0b', fontSize: '18px', letterSpacing: '2px', marginBottom: '8px' }}>
                                                        {'★'.repeat(review.rating)}{'☆'.repeat(5 - review.rating)}
                                                    </div>
                                                    {review.sentiment && (
                                                        <span style={{ padding: '4px 10px', borderRadius: '12px', fontSize: '12px', fontWeight: '600', background: review.sentiment === 'positive' ? '#dcfce7' : review.sentiment === 'negative' ? '#fee2e2' : '#fef3c7', color: review.sentiment === 'positive' ? '#166534' : review.sentiment === 'negative' ? '#991b1b' : '#b45309', textTransform: 'capitalize' }}>
                                                            {review.sentiment === 'positive' ? 'Olumlu' : review.sentiment === 'negative' ? 'Olumsuz' : 'Nötr'}
                                                        </span>
                                                    )}
                                                </div>
                                                <div style={{ textAlign: 'right' }}>
                                                    <div style={{ color: '#64748b', fontSize: '13px', fontWeight: '500' }}>
                                                        {new Date(review.created_at).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' })}
                                                    </div>
                                                    {review.topic && (
                                                        <div style={{ color: '#94a3b8', fontSize: '12px', marginTop: '4px', textTransform: 'capitalize' }}>
                                                            Konu: {review.topic}
                                                        </div>
                                                    )}
                                                </div>
                                            </div>
                                            <p style={{ margin: 0, color: '#334155', fontSize: '15px', lineHeight: '1.6' }}>
                                                {review.comment}
                                            </p>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};
