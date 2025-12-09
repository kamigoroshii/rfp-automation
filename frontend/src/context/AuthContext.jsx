import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Check local storage for persisted login
        const storedUser = localStorage.getItem('rfp_user');
        if (storedUser) {
            setUser(JSON.parse(storedUser));
        }
        setLoading(false);
    }, []);

    const login = (username, password) => {
        // Static credentials
        if (username === 'admin' && password === 'admin123') {
            const userData = { username: 'admin', role: 'admin' };
            setUser(userData);
            localStorage.setItem('rfp_user', JSON.stringify(userData));
            return true;
        }
        if (username === 'team' && password === 'team123') {
            const userData = { username: 'team', role: 'team' };
            setUser(userData);
            localStorage.setItem('rfp_user', JSON.stringify(userData));
            return true;
        }
        return false;
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem('rfp_user');
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
