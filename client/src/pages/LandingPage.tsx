import React, {useState} from 'react';
import { useEffect } from 'react';
import {User} from '../types';
import axios from 'axios';
import config from '../config.json';

export const LandingPage: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const access_token = localStorage.getItem('access_token');
    if(access_token){
      axios.get(`${config.API_URL}/users/me`,{
        headers:{
          access_token: access_token
        }
      }).then(resp => {
        const user: User = resp.data;
        setUser(user);
        setLoading(false);
      }).catch(e => {
        setLoading(false);
    });
    }else{
      setLoading(false);
    }
  },[]);
  
  if(loading){
    return (<div className='container mx-auto md:container md:mx-auto text-center h-screen'>
      <div className="flex h-full justify-center items-center">
      <button type="button" className="inline-flex items-center px-4 py-2 border border-transparent text-base leading-6 font-medium rounded-md text-white bg-rose-600 hover:bg-rose-500 focus:border-rose-700 active:bg-rose-700 transition ease-in-out duration-150 cursor-not-allowed" disabled>
        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Loading
      </button></div>
    
    </div>)
  }

  return (
    <div className='container mx-auto md:container md:mx-auto text-center h-screen'>
      <div className="flex h-full justify-center items-center">
        <div className="container mx-auto">
          <img src={!user ? "https://cdn.discordapp.com/avatars/780755594617421874/f4424fe27faf4ae0db7e00e2884940f1.png?size=256" : user.avatar_url} className="inline mb-5 rounded-full border-8 border-white" alt="" />
          <h1 className='text-white text-5xl mb-5'>Welcome to Cursy</h1>
          {!user ? (
            <button 
            className="bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 border-b-4 border-blue-700 hover:border-blue-500 rounded"
            onClick={() =>{
              window.location.href = "/login"
            }}>
              Log In with Discord
            </button>) : 
            <div>
              <h1 className="text-white text-xl mb-2">Logged In as:<span className="font-semibold"> {user.username}#{user.discriminator}</span></h1>
              <button 
            className="bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 border-b-4 border-blue-700 hover:border-blue-500 rounded "
            onClick={() =>{
              window.location.href = '/logout'
            }}>
              Logout
            </button>
            </div>}
        </div>
      </div>
    </div>
  );
}