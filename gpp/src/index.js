import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter, Route} from 'react-router-dom';
import Home from './components/Home';
import {Provider} from 'react-redux';
import store from './store/index'
import Nyc4dHeader from './components/Nyc4dHeader'
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

ReactDOM.render(
  <Provider store={store}>
    <BrowserRouter>
      <div>
        <App/>
        <Route exact path="/" component={Home}/>
        <Route path="/faq" component={Faq}/>
        <Route path="/about" component={About}/>
        <Route path="/contact" component={Contact}/>
      </div>
    </BrowserRouter>
  </Provider>,
  document.getElementById('root')
);
