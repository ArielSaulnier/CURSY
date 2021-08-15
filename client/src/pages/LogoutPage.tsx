import React from 'react';

export const LogoutPage: React.FC = () => {
    localStorage.removeItem('access_token');
    window.location.href = "/";
    return <div ></div>;
}