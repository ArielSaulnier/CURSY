import axios from "axios";
import React, { useEffect, useState } from "react";
import { Loading } from "../components/Loading";
import Nav from "../components/Navbar";
import config from "../config.json";
import { Guild, User } from "../types";

export const GuildsPage: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [guilds, setGuilds] = useState<Guild[] | null>(null);

  useEffect(() => {
    const access_token = localStorage.getItem("access_token");

    if (!access_token) {
      window.location.href = "/login";
    }

    const makeRequests = async () => {
      if (access_token) {
        const guildRES = await axios.get(`${config.API_URL}/guilds`, {
          headers: {
            access_token: access_token,
          },
        });
        setGuilds(guildRES.data.guilds);

        const userRes = await axios.get(`${config.API_URL}/users/me`, {
          headers: {
            access_token: access_token,
          },
        });
        setUser(userRes.data);

        setLoading(false);
      } else {
      }
    };
    makeRequests();
  }, []);

  console.log(guilds);

  if (loading) {
    return <Loading />;
  }

  if (user) {
    return (
      <div>
        <Nav/>
        <div className="container mx-auto">
          <div className="flex items-center h-full justify-center">
            <div className="h-3/4">
              <h1 className="text-white text-4xl mb16 text-center mb-24">
                Guilds
              </h1>
              <div className="grid grid-cols-4 gap-10 ">
                {guilds?.map((guild: Guild) => {
                  return (
                    <div className="transition duration-500 transform hover:scale-110 rounded-t-lg rounded-b-lg bg-purple-700 hover:bg-purple-600 justify-center mb-24">
                      <div className="flex item-center justify-center -mt-16">
                        <img
                          src={guild.icon_url}
                          alt=""
                          className="rounded-full "
                          width="150"
                        />
                      </div>
                      <div className=" rounded-md scrollbar-none overflow-x-auto p-6 text-sm leading-snug text-white justify-center flex item-center font-bold word-break">
                        {guild.name}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
            <div className="absolute top-1 text-white  right-1">
              <div className="flex items-center gap-2">
              <h1 className="text-white ">
              {user?.discriminator}#<span className="font-semibold text-lg">{user?.username}</span>
                </h1>
                <img
                  src={user?.avatar_url}
                  alt=""
                  width="50"
                  className="rounded-full "
                />
                
              </div>
            </div>
            
          </div>
        </div>
        <div className="bottom-0 left-0">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320">
                <path
                  fill="#6D28D9"
                  fill-opacity="1"
                  d="M0,192L48,208C96,224,192,256,288,250.7C384,245,480,203,576,181.3C672,160,768,160,864,181.3C960,203,1056,245,1152,240C1248,235,1344,181,1392,154.7L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
                ></path>
              </svg>
            </div>
      </div>
      
    );
  }

  return <div></div>;
};
