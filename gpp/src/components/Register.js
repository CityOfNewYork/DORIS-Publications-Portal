import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {Link} from 'react-router-dom';
import {Form, Segment} from 'semantic-ui-react';
import {MaskedInput} from 'react-text-mask';


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
            <p>While waiting for approval, you are free to <Link to="/search">search</Link> for publications.</p>
          </div>
        ) : (
          <div>
            <h1>Portal Registration</h1>
            <p>Please fill out the following form to apply for access to our submissions portal.</p>
            <Form>
              <Form.Dropdown
                required
                label="Agency"
                name="agency"
                search
                selection
                options={[
                  {
                    key: "doris",
                    value: "doris",
                    text: "DORIS - Department of Records & Information Services"
                  },
                  {
                    key: "doitt",
                    value: "doitt",
                    text: "DOITT - Department of Information Technology & Telecommunications"
                  },
                ]}
                placeholder="Select Your Agency"
              />
              <Form.Group widths="equal">
                {/* First Name */}
                <Form.Input
                  readOnly
                  label="First Name"
                  value="Joe (fetched from user record)"
                />
                {/* Last Name */}
                <Form.Input
                  readOnly
                  label="Last Name"
                  value="Smith (fetched from user record)"
                />
              </Form.Group>
              <Form.Group widths="equal">
                {/* Phone */}
                <Form.Input
                  required
                  label="Phone"
                  name="phone"
                  children={
                    <MaskedInput
                      mask={['(', /[1-9]/, /\d/, /\d/, ')', ' ', /\d/, /\d/, /\d/, '-', /\d/, /\d/, /\d/, /\d/]}
                      placeholder="(123) 456-7890"
                      required
                      pattern="^[\(]\d{3}[\)][ ]\d{3}[\-]\d{4}$"
                    />
                  }
                />
                {/* Email */}
                <Form.Input
                  readOnly
                  label="Email"
                  value="jsmith@email.com (fetched from user record)"
                />
              </Form.Group>
              <Segment>
                {/* Registration Terms */}
                <Form.Checkbox
                  label="I acknowledge that I am the designated agency contact for submission of records to the ML.
                  If there is any change (such as my reassignment to other duties or some other agency), I will notify
                  my supervisor that a new agency contact for the ML needs to be appointed and registered."
                />
              </Segment>
              <Form.Button fluid>Submit</Form.Button>
            </Form>
          </div>
        )}
      </div>
    );
  }
}

export default Register;