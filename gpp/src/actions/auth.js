import {
  LOGIN_USER,
  LOGOUT_USER,
  REGISTER_USER,
  DEREGISTER_USER,
  APPROVE_USER,
  DENY_USER
} from '../constants/index'


export function loginUser() {
  return {
    type: LOGIN_USER
  };
}

export function logoutUser() {
  return {
    type: LOGOUT_USER
  };
}

export function registerUser() {
  return {
    type: REGISTER_USER
  };
}

export function deregisterUser() {
  return {
    type: DEREGISTER_USER
  };
}

export function approveUser() {
  return {
    type: APPROVE_USER
  };
}

export function denyUser() {
  return {
    type: DENY_USER
  };
}
