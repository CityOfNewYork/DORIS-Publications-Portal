import {
  LOGIN_USER,
  LOGOUT_USER,
  REGISTER_USER,
  DEREGISTER_USER,
  APPROVE_USER,
  DENY_USER
} from "../constants/index"


const defaultState = {
  authenticated: false,
  registered: false,
  approved: false
};


export function auth(state = defaultState, action) {
  switch (action.type) {
    case LOGIN_USER:
      return {...state, authenticated: true};
    case LOGOUT_USER:
      return {...state, authenticated: false};
    case REGISTER_USER:
      return {...state, registered: true};
    case DEREGISTER_USER:
      return {...state, registered: false};
    case APPROVE_USER:
      return {...state, approved: true };
    case DENY_USER:
      return {...state, approved: false};
    default:
      return state;
  }
}