export interface User {
    id: string;
    username: string;
    discriminator: number;
    avatar_url: string;
}

export interface Status{
    guilds: number;
    ping: number;
}