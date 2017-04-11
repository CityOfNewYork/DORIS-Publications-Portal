import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter, Route} from 'react-router-dom';
import {ROUTE, MENU_ITEM} from "./constants/index"
import Home from './components/Home';
import {Provider} from 'react-redux';
import store from './store/index'
import Nyc4dHeader from './components/Nyc4dHeader/Nyc4dHeader'
import Navbar from './components/Navbar'
import Faq from './components/Faq'
import About from './components/About'
import Contact from './components/Contact'
import './index.css';

const App = () => (
  <div>
    <Nyc4dHeader/>
    <Navbar/>
  </div>
);

const Search = (props) => (
  <Home activeItem={MENU_ITEM.search} {...props}/>
);

const Register = (props) => (
  // TODO: redirect(?) to home if already registered
  <Home activeItem={MENU_ITEM.register} {...props}/>
);

const Submit = (props) => (
  <Home activeItem={MENU_ITEM.submit} {...props}/>
);

const Dashboard = (props) => (
  <Home activeItem={MENU_ITEM.dashboard} {...props}/>
);

const Publications = (props) => (
  <Home activeItem={MENU_ITEM.publications} {...props}/>
);

const Profile = (props) => (
  <Home activeItem={MENU_ITEM.profile} {...props}/>
);

const Registrants = (props) => (
  <Home activeItem={MENU_ITEM.registrants} {...props}/>
);

const Submissions = (props) => (
  <Home activeItem={MENU_ITEM.submissions} {...props}/>
);


ReactDOM.render(
  <Provider store={store}>
    <BrowserRouter>
      <div>
        <App/>
        <Route exact path={ROUTE.index} component={Home}/>
        <Route path={ROUTE.search} component={Search}/>
        <Route path={ROUTE.register} component={Register}/>
        <Route path={ROUTE.submit} component={Submit}/>
        <Route path={ROUTE.dashboard} component={Dashboard}/>
        <Route path={ROUTE.publications} component={Publications}/>
        <Route path={ROUTE.profile} component={Profile}/>
        <Route path={ROUTE.registrants} component={Registrants}/>
        <Route path={ROUTE.submissions} component={Submissions}/>
        <Route path={ROUTE.faq} component={Faq}/>
        <Route path={ROUTE.about} component={About}/>
        <Route path={ROUTE.contact} component={Contact}/>
      </div>
    </BrowserRouter>
  </Provider>,
  document.getElementById('root')
);
