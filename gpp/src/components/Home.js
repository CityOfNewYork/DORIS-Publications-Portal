import React, {Component} from 'react';
import {connect} from 'react-redux';
import {Menu, Segment, Container} from 'semantic-ui-react';
import {mapStateToProps, mapDispatchToProps} from '../utils/reduxMappers'
import Submit from './Submit'
import Search from './Search'
import Register from './Register'


class Home extends Component {

  static ITEM_SEARCH = "search";
  static ITEM_SUBMIT = "submit";
  static ITEM_REGISTER = "register";
  static ITEM_MANAGE_PROFILE = "manageProfile";
  static ITEM_ADMIN = "admin";
  static ITEM_DOCUMENTS = "documents";

  state = {
    activeItem: this.props.approved ? Home.ITEM_SUBMIT : Home.ITEM_REGISTER
  };

  activeComponent = () => {
    switch (this.state.activeItem) {
      case Home.ITEM_REGISTER:
        return <Register
          registered={this.props.registered}
        />;
      case Home.ITEM_SUBMIT:
        return this.props.authenticatedFE && <Submit/>;
      case Home.ITEM_SEARCH:
        return <Search/>;
      case Home.ITEM_MANAGE_PROFILE:
        return <div>For changing user attributes not retrieved via SAML Assertion</div>;
      case Home.ITEM_ADMIN:
        return <div>For approving/denying registrants</div>;
      case Home.ITEM_DOCUMENTS:
        return <div>For viewing <strong>submitted</strong> and <strong>published</strong> documents</div>;
      default:
        return <div>You should not be able to see this...</div>;
    }
  };

  /**
   * Ensure correct activeItem is set.
   */
  componentWillUpdate(nextProps, nextState) {
    if ([Home.ITEM_REGISTER, Home.ITEM_SUBMIT].includes(nextState.activeItem)) {
      const nextActiveItem = nextProps.approved ? Home.ITEM_SUBMIT : Home.ITEM_REGISTER;
      if (nextState.activeItem !== nextActiveItem) {
        this.setState({activeItem: nextActiveItem});
      }
    }
  }

  setActiveItem = (e, {name}) => {
    this.setState({activeItem: name});
  };

  render() {
    const {
      authenticatedFE,
      approved,
    } = this.props;

    const {activeItem} = this.state;

    return (
      <Container>
        { authenticatedFE ? (
          // logged in user...
          <div>
            { approved ? (
              <Menu attached="top" tabular>
                <Menu.Item
                  name={Home.ITEM_SUBMIT}
                  active={activeItem === Home.ITEM_SUBMIT}
                  onClick={this.setActiveItem}
                  icon="upload"
                />
                <Menu.Item
                  name={Home.ITEM_ADMIN}
                  active={activeItem === Home.ITEM_ADMIN}
                  onClick={this.setActiveItem}
                  icon="user outline"
                />
                <Menu.Item
                  name={Home.ITEM_DOCUMENTS}
                  active={activeItem === Home.ITEM_DOCUMENTS}
                  onClick={this.setActiveItem}
                  icon="file text outline"
                />
                <Menu.Item
                  name={Home.ITEM_MANAGE_PROFILE}
                  active={activeItem === Home.ITEM_MANAGE_PROFILE}
                  onClick={this.setActiveItem}
                  icon="setting"
                />
                <Menu.Item
                  name={Home.ITEM_SEARCH}
                  active={activeItem === Home.ITEM_SEARCH}
                  onClick={this.setActiveItem}
                  icon="search"
                />
              </Menu>
            ) : (
              <Menu attached="top" tabular>
                <Menu.Item
                  name={Home.ITEM_REGISTER}
                  active={activeItem === Home.ITEM_REGISTER}
                  onClick={this.setActiveItem}
                  icon="add user"
                />
                <Menu.Item
                  name={Home.ITEM_SEARCH}
                  active={activeItem === Home.ITEM_SEARCH}
                  onClick={this.setActiveItem}
                  icon="search"
                />
              </Menu>
            )}
            <Segment attached="bottom">
              {this.activeComponent()}
            </Segment>
          </div>
        ) : (
          // logged out / public user only uses Search
          <div>
            <h1>Search</h1>
            <Search/>
          </div>
        )}
      </Container>
    );
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Home);
