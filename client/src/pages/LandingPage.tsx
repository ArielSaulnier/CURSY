import React, {useState} from 'react';
import { useEffect } from 'react';
import {Status, User} from '../types';
import axios from 'axios';
import config from '../config.json';

export const LandingPage: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [status, setStatus] = useState<Status | null>(null);

  useEffect(() => {
    axios.get(`${config.BOT_API_URL}/status`)
    .then((resp) => {
      setStatus(resp.data)
    });

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
    <div>
    <div className='container mx-auto md:container md:mx-auto text-center h-screen'>
      <div className="flex h-full justify-center items-center">
        <div className="container mx-auto">
          <img src={!user ? "https://cdn.discordapp.com/avatars/780755594617421874/f4424fe27faf4ae0db7e00e2884940f1.png?size=256" : user.avatar_url} className="inline mb-5 rounded-full border-8 border-white" alt="" />
          <h1 className='text-white text-5xl mb-5 text-semibold'>Welcome to Cursy</h1>
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
    <div>
      <div className="container mx-auto w-1/4 ">
        <h1 className="text-white font-semibold text-4xl  text-center mb-7">Infos</h1>
        <div className="flex items.center justify-between">
        <div><h1 className="text-white font-medium text-xl  text-center mb-3">Ping</h1>
        <h3 className="text-center text-white font-bold text-xl">
        {status ? status.ping : '...'}
        </h3></div>
          <div><h1 className="text-white font-medium text-xl  text-center mb-3">Status</h1>
        <span className={`bg-${status ? 'green' : 'red'}-500 text-white font-bold py-2 px-4 rounded`}>
          {status ? '✓Online' : 'Offline'}
        </span></div>
        
        <div><h1 className="text-white font-medium text-xl  text-center mb-3">Servers</h1>
        <h3 className="text-center text-white font-bold text-xl">
          {status ? status.guilds : '...'}
        </h3></div></div>
      </div>
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="#3b82f6" fill-opacity="1" d="M0,128L20,133.3C40,139,80,149,120,176C160,203,200,245,240,272C280,299,320,309,360,261.3C400,213,440,107,480,80C520,53,560,107,600,106.7C640,107,680,53,720,80C760,107,800,213,840,240C880,267,920,213,960,197.3C1000,181,1040,203,1080,218.7C1120,235,1160,245,1200,224C1240,203,1280,149,1320,128C1360,107,1400,117,1420,122.7L1440,128L1440,320L1420,320C1400,320,1360,320,1320,320C1280,320,1240,320,1200,320C1160,320,1120,320,1080,320C1040,320,1000,320,960,320C920,320,880,320,840,320C800,320,760,320,720,320C680,320,640,320,600,320C560,320,520,320,480,320C440,320,400,320,360,320C320,320,280,320,240,320C200,320,160,320,120,320C80,320,40,320,20,320L0,320Z"></path></svg></div>
    </div>
  );
}