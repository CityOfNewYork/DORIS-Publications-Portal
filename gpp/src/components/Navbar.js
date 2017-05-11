import React, {Component} from 'react';
import {connect} from 'react-redux';
import {Link} from 'react-router-dom';
import {mapStateToProps, mapDispatchToProps} from '../utils/reduxMappers'
import {Menu, Icon} from 'semantic-ui-react';
import {csrfFetch} from "../utils/fetch"


class Navbar extends Component {

  state = {
    authenticatedBE: false,
    activePath: ""  // FIXME: "active" on appropriate <Link> on Back/Forward
  };

  loginBE = () => {
    csrfFetch("/login");
    this.setState({authenticatedBE: true})
  };

  logoutBE = () => {
    csrfFetch("/logout");
    this.setState({authenticatedBE: false});
  };

  setActivePath = () => {
    this.setState({activePath: location.pathname})
  };

  activeClassIfPath = (path) => (
    location.pathname === path ? "active" : ""
  );

  render() {
    const {
      authenticatedFE, logoutFE, loginFE,
      registered, register, deregister,
      approved, approve, deny
    } = this.props;

    const {authenticatedBE} = this.state;

    return (
      <div>
        <Menu>
          <Link
            className={"icon header item " + this.activeClassIfPath("/")}
            to="/"
            onClick={this.setActivePath}
          >
            <Icon name="home"/>&nbsp;
          </Link>
          <Menu.Menu position="right">
            <Link
              className={"item " + this.activeClassIfPath("/faq")}
              to="/faq"
              onClick={this.setActivePath}
            >
              FAQ
            </Link>
            <Link
              className={"item " + this.activeClassIfPath("/about")}
              to="/about"
              onClick={this.setActivePath}
            >
              About
            </Link>
            <Link
              className={"item " + this.activeClassIfPath("/contact")}
              to="/contact"
              onClick={this.setActivePath}
            >
              Contact
            </Link>
          </Menu.Menu>
        </Menu>
        {/* Following menu is for testing purposes only. */}
        <Menu vertical inverted compact fixed="bottom">
          <Menu.Item header>TOGGLES</Menu.Item>
          <Menu.Menu>
            <Menu.Item
              name={ (authenticatedFE ? "Logout" : "Login") + "Frontend" }
              onClick={ authenticatedFE ? logoutFE : loginFE }
            />
            <Menu.Item
              name={ (authenticatedBE ? "Logout" : "Login") + "Backend" }
              onClick={ authenticatedBE ? this.logoutBE : this.loginBE }
            />
            <Menu.Item
              name={ (registered ? "Deregister" : "Register" )}
              onClick={ registered ? deregister : register }
            />
            <Menu.Item
              name={ (approved ? "Deny" : "Approve")}
              onClick={ approved ? deny : approve }
            />
          </Menu.Menu>
        </Menu>
      </div>
    );
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Navbar);
