import React from 'react';
import config  from '../config.json';

export const LoginPage: React.FC = () => {
    window.location.href = config.OAUTH_URL;
    return <div ></div>;
}