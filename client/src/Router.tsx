import React from 'react';
import { BrowserRouter, Switch, Route, Link } from 'react-router-dom';
import { CallbackHandler } from './pages/CallbackHandler';
import { LandingPage } from './pages/LandingPage';
import { LoginPage } from './pages/LoginPage';
import { LogoutPage } from './pages/LogoutPage';
import { GuildsPage } from './pages/GuildsPage';
export const Router: React.FC = () => {
    return (
        <BrowserRouter>
            <Switch>
                <Route exact path='/' component={LandingPage}/>
                <Route exact path='/callback' component={CallbackHandler}/>
                <Route exact path='/login' component={LoginPage}/>
                <Route exact path='/logout' component={LogoutPage}/>
                <Route exact path='/guilds' component={GuildsPage}/>
            </Switch>
        </BrowserRouter>
    )
}