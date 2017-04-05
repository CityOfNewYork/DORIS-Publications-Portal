import {createStore} from 'redux'
import {persistStore, autoRehydrate} from 'redux-persist'
import {auth} from '../reducers/auth'


const store = createStore(
  auth,
  undefined,
  autoRehydrate()
);

persistStore(store);

export default store;
