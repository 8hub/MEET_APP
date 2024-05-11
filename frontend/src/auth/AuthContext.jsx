import React, { createContext, useReducer, useEffect } from 'react';
import { authReducer, initialState } from './authReducer';
import { refreshAccessToken } from './authActions';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [state, dispatch] = useReducer(authReducer, initialState);

    useEffect(() => {
        refreshAccessToken(dispatch);
    }, []);
    
    return (
        <AuthContext.Provider value={{ state, dispatch }}>
            {children}
        </AuthContext.Provider>
    );
};

export default AuthContext;