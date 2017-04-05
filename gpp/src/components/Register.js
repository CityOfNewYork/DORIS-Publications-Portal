import React, {Component, PropTypes} from 'react';

class Register extends Component {

  static propTypes = {
    registered: PropTypes.bool.isRequired,  // TODO: fetch instead of prop
  };

  render() {
    const {registered} = this.props;

    return (
      <div>
        { registered ? (
          <div>
            <h1>Registration Status: <span>Pending</span></h1>
            <p>Other relevant information...</p>
          </div>
        ) : (
          <div>
            <h1>Portal Registration</h1>
            <p>Please fill out the following form to register for access to our submissions portal.</p>
            <p>(Form will go here)</p>
          </div>
        )}
      </div>
    );
  }
}

export default Register;