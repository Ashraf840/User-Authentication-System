export interface UserProfile {
    exp: number;
    iat: number;
    jti: string;
    token_type: string;
    user_id: number;
    email?: string;
    full_name?: string;
}
