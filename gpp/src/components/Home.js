import React, {Component} from 'react';
import {connect} from 'react-redux';
import {Menu, Container, Grid} from 'semantic-ui-react';
import {ROUTE, MENU_ITEM} from "../constants/index";
import {mapStateToProps, mapDispatchToProps} from '../utils/reduxMappers'
import Submit from './Submit'
import Search from './Search'
import Register from './Register'


class Home extends Component {

  static ITEM_TO_ROUTE = {
    [MENU_ITEM.search]: ROUTE.search,
    [MENU_ITEM.submit]: ROUTE.submit,
    [MENU_ITEM.register]: ROUTE.register,
    [MENU_ITEM.dashboard]: ROUTE.dashboard,
    [MENU_ITEM.publications]: ROUTE.publications,
    [MENU_ITEM.profile]: ROUTE.profile,
    [MENU_ITEM.registrants]: ROUTE.registrants,
    [MENU_ITEM.submissions]: ROUTE.submissions
  };

  state = {
    activeItem: this.props.activeItem || (this.props.approved ? MENU_ITEM.submit : MENU_ITEM.register)
  };

  activeComponent = () => {
    switch (this.state.activeItem) {
      case MENU_ITEM.register:
        return <Register
          registered={this.props.registered}
        />;
      case MENU_ITEM.submit:
        return this.props.authenticatedFE && <Submit/>;
      case MENU_ITEM.search:
        return <Search/>;
      case MENU_ITEM.dashboard:
        return <div>Overview of submissions, TODO: links to other tabs</div>;
      case MENU_ITEM.publications:
        return <div>View published documents submitted through this portal</div>;
      case MENU_ITEM.profile:
        return <div>Change user attributes not retrieved via SAML Assertion</div>;
      case MENU_ITEM.registrants:
        return <div>Approve or deny registrants</div>;
      case MENU_ITEM.submissions:
        return <div>Review, approve, and request changes for submitted documents.</div>;
      default:
        return <div>Nothing to see here, move along...</div>;
    }
  };

  /**
   * Ensure correct activeItem is set before updating.
   */
  componentWillUpdate(nextProps, nextState) {
    // TODO: dashboard for library and super(?)
    if ([MENU_ITEM.register, MENU_ITEM.submit].includes(nextState.activeItem)) {
      const nextActiveItem = nextProps.approved ? MENU_ITEM.submit : MENU_ITEM.register;
      if (nextState.activeItem !== nextActiveItem) {
        this.setState({activeItem: nextActiveItem});
      }
    }
    else {
      if (!nextProps.approved) {
        this.setState({activeItem: MENU_ITEM.register})
      }
    }
  }

  /**
   * Set state.activeTtem and update route.
   */
  setActiveItem = (e, {name}) => {
    this.setState({activeItem: name});
    this.props.history.push(Home.ITEM_TO_ROUTE[name]);
  };

  render() {
    const {
      authenticatedFE,
      approved,
    } = this.props;

    const MenuItem = ({item, icon}) => (
      <Menu.Item
        name={item}
        active={this.state.activeItem === item}
        onClick={this.setActiveItem}
        icon={icon}
      />
    );

    return (
      <Container>
        { authenticatedFE ? (
          // logged in user...
          <Grid>
            <Grid.Column width={3}>
              { approved ? (
                <Menu fluid vertical tabular>
                  <MenuItem item={MENU_ITEM.submit} icon="upload"/>
                  <MenuItem item={MENU_ITEM.dashboard} icon="dashboard"/>
                  <MenuItem item={MENU_ITEM.publications} icon="file text outline"/>
                  <MenuItem item={MENU_ITEM.registrants} icon="user outline"/>
                  <MenuItem item={MENU_ITEM.submissions} icon="file text"/>
                  <MenuItem item={MENU_ITEM.profile} icon="setting"/>
                  <MenuItem item={MENU_ITEM.search} icon="search"/>
                </Menu>
              ) : (
                <Menu fluid vertical tabular>
                  <MenuItem item={MENU_ITEM.register} icon="add user"/>
                  <MenuItem item={MENU_ITEM.search} icon="search"/>
                </Menu>
              )}
            </Grid.Column>
            <Grid.Column width={13}>
              {this.activeComponent()}
            </Grid.Column>
          </Grid>
        ) : (
          // logged out / public user only uses Search
          <Search/>
        )}
      </Container>
    );
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Home);
