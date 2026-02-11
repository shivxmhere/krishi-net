import React, { createContext, useState, useContext, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import api from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [isLoading, setIsLoading] = useState(true);
    const [userToken, setUserToken] = useState(null);
    const [user, setUser] = useState(null);

    useEffect(() => {
        // Check for stored token on app load
        loadStoredData();
    }, []);

    const loadStoredData = async () => {
        try {
            const token = await AsyncStorage.getItem('userToken');
            const userData = await AsyncStorage.getItem('userData');
            if (token) {
                setUserToken(token);
                setUser(JSON.parse(userData));
            }
        } catch (e) {
            console.error('Failed to load storage', e);
        } finally {
            setIsLoading(false);
        }
    };

    const login = async (email, password) => {
        try {
            const response = await api.post('/api/auth/login', { email, password });
            const { access_token } = response.data;

            await AsyncStorage.setItem('userToken', access_token);
            await AsyncStorage.setItem('userData', JSON.stringify({ email }));

            setUserToken(access_token);
            setUser({ email });
            return { success: true };
        } catch (error) {
            return {
                success: false,
                message: error.response?.data?.detail || 'Invalid email or password'
            };
        }
    };

    const register = async (email, password) => {
        try {
            await api.post('/api/auth/register', { email, password });
            return await login(email, password);
        } catch (error) {
            return {
                success: false,
                message: error.response?.data?.detail || 'Registration failed'
            };
        }
    };

    const logout = async () => {
        await AsyncStorage.removeItem('userToken');
        await AsyncStorage.removeItem('userData');
        setUserToken(null);
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ login, logout, register, isLoading, userToken, user }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
