import React, { createContext, useState, useContext, useRef } from 'react';
import { Alert } from 'react-bootstrap';

const NotificationContext = createContext();

export const useNotification = () => useContext(NotificationContext);

export const NotificationProvider = ({ children }) => {
    const [notification, setNotification] = useState(null);
    const [animationClass, setAnimationClass] = useState('');
    const timeoutRef = useRef(null);

    const showNotification = (message, variant = 'info') => {
        if (timeoutRef.current) {
            clearTimeout(timeoutRef.current);
        }

        setNotification({ message, variant });
        setAnimationClass('notification-enter');

        timeoutRef.current = setTimeout(() => {
            setAnimationClass('notification-exit');
            setTimeout(() => {
                setNotification(null);
                setAnimationClass('');
            }, 500); // Duration of slideUp animation
        }, 2500);
    };

    const handleDismiss = () => {
        if (timeoutRef.current) {
            clearTimeout(timeoutRef.current);
        }
        setAnimationClass('notification-exit');
        setTimeout(() => {
            setNotification(null);
            setAnimationClass('');
        }, 500);
    };

    return (
        <NotificationContext.Provider value={showNotification}>
            {children}
            {notification && (
                <Alert
                    className={`notification ${animationClass}`}
                    variant={notification.variant}
                    dismissible
                    onClose={handleDismiss}
                >
                    {notification.message}
                </Alert>
            )}
        </NotificationContext.Provider>
    );
};
