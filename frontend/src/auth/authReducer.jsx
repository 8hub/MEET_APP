export const initialState = {
  isAuthenticated: false,
  user: null,
  accessToken: null,
  refreshToken: null,
};

export const authReducer = (state, action) => {
  switch (action.type) {
      case 'LOGIN':
          return {
              ...state,
              isAuthenticated: true,
              user: action.payload.user,
              accessToken: action.payload.accessToken,
              refreshToken: action.payload.refreshToken,
          };
      case 'LOGOUT':
          return {
              ...state,
              isAuthenticated: false,
              user: null,
              accessToken: null,
              refreshToken: null,
          };
      default:
          return state;
  }
};
