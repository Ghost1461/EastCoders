import React, { useState, useEffect, useRef } from 'react';

export const CustomPeriodPicker = ({ period, value, onChange }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [currentDate, setCurrentDate] = useState(new Date());
    const dropdownRef = useRef(null);

    // Close when clicking outside
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const getDaysInMonth = (year, month) => new Date(year, month + 1, 0).getDate();
    // JS getDay() is 0 for Sunday. We want Monday=0, Sunday=6
    const getFirstDayOfMonth = (year, month) => {
        const day = new Date(year, month, 1).getDay();
        return day === 0 ? 6 : day - 1;
    };

    const renderDailyPicker = () => {
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();
        const daysInMonth = getDaysInMonth(year, month);
        const firstDay = getFirstDayOfMonth(year, month);
        const days = [];
        
        const today = new Date();
        const todayStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;

        for (let i = 0; i < firstDay; i++) {
            days.push(<div key={`empty-${i}`} className="calendar-day empty"></div>);
        }
        
        for (let i = 1; i <= daysInMonth; i++) {
            const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
            const isSelected = value === dateStr;
            const isFuture = dateStr > todayStr;
            
            days.push(
                <button 
                    key={i} 
                    className={`calendar-day ${isSelected ? 'selected' : ''} ${isFuture ? 'disabled' : ''}`}
                    disabled={isFuture}
                    onClick={() => {
                        if (!isFuture) {
                            onChange(dateStr);
                            setIsOpen(false);
                        }
                    }}
                >
                    {i}
                </button>
            );
        }

        const monthNames = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"];

        return (
            <div className="custom-calendar">
                <div className="calendar-header">
                    <button onClick={() => setCurrentDate(new Date(year, month - 1, 1))}>&lt;</button>
                    <span style={{ fontWeight: 'bold' }}>{monthNames[month]} {year}</span>
                    <button onClick={() => setCurrentDate(new Date(year, month + 1, 1))}>&gt;</button>
                </div>
                <div className="calendar-grid">
                    <div className="day-name">Pzt</div><div className="day-name">Sal</div><div className="day-name">Çar</div>
                    <div className="day-name">Per</div><div className="day-name">Cum</div><div className="day-name">Cmt</div><div className="day-name">Paz</div>
                    {days}
                </div>
            </div>
        );
    };

    const renderMonthlyPicker = () => {
        const year = currentDate.getFullYear();
        const monthNames = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"];
        
        const today = new Date();
        const currentYear = today.getFullYear();
        const currentMonth = today.getMonth();

        return (
            <div className="custom-calendar">
                <div className="calendar-header">
                    <button onClick={() => setCurrentDate(new Date(year - 1, 0, 1))}>&lt;</button>
                    <span style={{ fontWeight: 'bold' }}>{year}</span>
                    <button onClick={() => setCurrentDate(new Date(year + 1, 0, 1))}>&gt;</button>
                </div>
                <div className="months-grid">
                    {monthNames.map((m, idx) => {
                        const valStr = `${year}-${String(idx + 1).padStart(2, '0')}`;
                        const isSelected = value === valStr;
                        const isFuture = year > currentYear || (year === currentYear && idx > currentMonth);
                        
                        return (
                            <button 
                                key={m}
                                className={`month-btn ${isSelected ? 'selected' : ''} ${isFuture ? 'disabled' : ''}`}
                                disabled={isFuture}
                                onClick={() => { if (!isFuture) { onChange(valStr); setIsOpen(false); } }}
                            >
                                {m}
                            </button>
                        );
                    })}
                </div>
            </div>
        );
    };

    const getWeekNumber = (d) => {
        const date = new Date(d.getTime());
        date.setHours(0, 0, 0, 0);
        date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
        const week1 = new Date(date.getFullYear(), 0, 4);
        return 1 + Math.round(((date.getTime() - week1.getTime()) / 86400000 - 3 + (week1.getDay() + 6) % 7) / 7);
    };

    const renderWeeklyPicker = () => {
        const year = currentDate.getFullYear();
        const today = new Date();
        const currentYear = today.getFullYear();
        const currentWeek = getWeekNumber(today);
        
        const weeks = [];
        for(let i=1; i<=52; i++) {
            const valStr = `${year}-W${i}`;
            const isSelected = value === valStr;
            const isFuture = year > currentYear || (year === currentYear && i > currentWeek);
            
            weeks.push(
                <button 
                    key={i}
                    className={`week-btn ${isSelected ? 'selected' : ''} ${isFuture ? 'disabled' : ''}`}
                    disabled={isFuture}
                    onClick={() => { if (!isFuture) { onChange(valStr); setIsOpen(false); } }}
                >
                    {i}. Hafta
                </button>
            );
        }

        return (
            <div className="custom-calendar">
                <div className="calendar-header">
                    <button onClick={() => setCurrentDate(new Date(year - 1, 0, 1))}>&lt;</button>
                    <span style={{ fontWeight: 'bold' }}>{year}</span>
                    <button onClick={() => setCurrentDate(new Date(year + 1, 0, 1))}>&gt;</button>
                </div>
                <div className="weeks-grid" style={{ maxHeight: '220px', overflowY: 'auto' }}>
                    {weeks}
                </div>
            </div>
        );
    };

    return (
        <div className="custom-period-picker-container" ref={dropdownRef} style={{ position: 'relative', flex: 1, minWidth: '220px' }}>
            <div 
                className="picker-input"
                onClick={() => setIsOpen(!isOpen)}
                style={{
                    padding: '16px 20px', borderRadius: '16px', border: `2px solid ${isOpen ? '#3b82f6' : '#e2e8f0'}`, 
                    fontSize: '16px', color: value ? '#1e293b' : '#94a3b8', background: '#f8fafc', fontWeight: '600', 
                    cursor: 'pointer', display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                    transition: 'border-color 0.2s', boxShadow: isOpen ? '0 0 0 4px rgba(59,130,246,0.1)' : 'none'
                }}
            >
                <span>{value || (period === 'daily' ? 'Gün Seçiniz' : period === 'weekly' ? 'Hafta Seçiniz' : 'Ay Seçiniz')}</span>
                <span style={{ color: '#8b5cf6', fontSize: '20px' }}>📅</span>
            </div>
            
            {isOpen && (
                <div className="picker-dropdown" style={{
                    position: 'absolute', top: 'calc(100% + 12px)', left: 0, background: 'white', 
                    boxShadow: '0 20px 40px -10px rgba(0,0,0,0.2)', borderRadius: '20px', border: '1px solid #e2e8f0',
                    zIndex: 50, width: '100%', minWidth: '320px', padding: '24px', animation: 'fadeInDown 0.2s cubic-bezier(0.16, 1, 0.3, 1)'
                }}>
                    {period === 'daily' && renderDailyPicker()}
                    {period === 'monthly' && renderMonthlyPicker()}
                    {period === 'weekly' && renderWeeklyPicker()}
                </div>
            )}
            
            <style>{`
                @keyframes fadeInDown {
                    from { opacity: 0; transform: translateY(-10px) scale(0.98); }
                    to { opacity: 1; transform: translateY(0) scale(1); }
                }
                .custom-calendar .calendar-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; color: #0f172a; }
                .custom-calendar .calendar-header button { background: #f1f5f9; border: none; width: 36px; height: 36px; border-radius: 10px; cursor: pointer; color: #475569; font-weight: bold; transition: all 0.2s; font-size: 16px; display: flex; align-items: center; justify-content: center; }
                .custom-calendar .calendar-header button:hover { background: #e2e8f0; color: #0f172a; transform: scale(1.05); }
                
                .calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px; text-align: center; }
                .day-name { font-size: 13px; color: #94a3b8; font-weight: 700; padding-bottom: 12px; }
                .calendar-day { padding: 10px 0; border: none; background: white; border-radius: 12px; cursor: pointer; font-size: 15px; color: #334155; font-weight: 600; transition: all 0.2s; }
                .calendar-day:hover:not(.empty):not(.disabled) { background: #eff6ff; color: #3b82f6; }
                .calendar-day.selected { background: #3b82f6; color: white; box-shadow: 0 4px 12px rgba(59,130,246,0.35); }
                .calendar-day.disabled { color: #cbd5e1; cursor: not-allowed; background: transparent; }
                
                .months-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
                .month-btn { padding: 16px 8px; border: none; background: #f8fafc; border-radius: 16px; cursor: pointer; font-size: 15px; font-weight: 600; color: #475569; transition: all 0.2s; border: 1px solid transparent; }
                .month-btn:hover:not(.disabled) { background: #eff6ff; color: #3b82f6; border-color: #bfdbfe; }
                .month-btn.selected { background: #8b5cf6; color: white; box-shadow: 0 4px 15px rgba(139,92,246,0.35); }
                .month-btn.disabled { color: #cbd5e1; cursor: not-allowed; background: #f8fafc; opacity: 0.6; }
                
                .weeks-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; padding-right: 8px; }
                .weeks-grid::-webkit-scrollbar { width: 6px; }
                .weeks-grid::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
                .week-btn { padding: 12px; border: none; background: #f8fafc; border-radius: 12px; cursor: pointer; font-size: 14px; font-weight: 600; color: #475569; transition: all 0.2s; border: 1px solid transparent; }
                .week-btn:hover:not(.disabled) { background: #eff6ff; color: #3b82f6; border-color: #bfdbfe; }
                .week-btn.selected { background: #10b981; color: white; box-shadow: 0 4px 15px rgba(16,185,129,0.35); }
                .week-btn.disabled { color: #cbd5e1; cursor: not-allowed; background: #f8fafc; opacity: 0.6; }
            `}</style>
        </div>
    );
};
