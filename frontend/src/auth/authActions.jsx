import axios from 'axios';
import { 
    API_USER_LOGIN,
    API_USER_LOGOUT, 
    API_USER_REFRESH 
} from '../constants';

export const login = async (dispatch, username, password) => {
    try {
        const response = await axios.post(API_USER_LOGIN, { username, password });
        if (response.data.access && response.data.refresh && response.data.user) {
            // store tokens in local storage
            localStorage.setItem('accessToken', response.data.access);
            localStorage.setItem('refreshToken', response.data.refresh);
            // set the axios auth header
            axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
            dispatch({
                type: 'LOGIN',
                payload: {
                    accessToken: response.data.access,
                    refreshToken: response.data.refresh,
                    user: response.data.user,
                },
            });
        }
    } catch (error) {
        console.error('Login failed:', error);
        // handle login error
    }
};

export const logout = async (dispatch) => {
  try {
    const refreshToken = localStorage.getItem('refreshToken');
    if(!refreshToken){
        console.error('No refresh token found');
        return;
    }
    const response = await axios.post(API_USER_LOGOUT, {
        refresh: refreshToken,
    });
    if (response.status === 204) {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');

        axios.defaults.headers.common['Authorization'] = '';

        dispatch({
            type: 'LOGOUT'
        });
    }
  } catch (error) {
      console.error('Logout failed:', error);
      // handle logout error
  }
};


export const refreshAccessToken = async (dispatch) => {
    try {
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) {
            console.error('No refresh token found');
            localStorage.removeItem('accessToken');
            dispatch({
                type: 'LOGOUT'
            });
            return;
        }
        const response = await axios.post(API_USER_REFRESH, { 
            refresh: refreshToken
        });

        if (response.data.access) {
            localStorage.setItem('accessToken', response.data.access);
            axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
            dispatch({
                type: 'REFRESH',
                payload: {
                    accessToken: response.data.access,
                    refreshToken: refreshToken,
                    user: response.data.user,
                },
            });
            return;
        }
        if (response.data.error) {
            console.error('Refresh failed:', response.data.error);
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            dispatch({
                type: 'LOGOUT'
            });
        }
    } catch (error) {
        console.error('Refresh failed:', error);
        dispatch({
            type: 'LOGOUT'
        });
        // handle refresh error
    }
}