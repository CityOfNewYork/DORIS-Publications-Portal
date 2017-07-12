import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {Link} from 'react-router-dom';
import {Form, Table, Segment, Message} from 'semantic-ui-react';
import {MaskedInput} from 'react-text-mask';


class Register extends Component {

  static propTypes = {
    registered: PropTypes.bool.isRequired,  // TODO: fetch instead of prop
  };

  state = {
    denied: false
  };

  toggleStatus = () => {
    this.setState({denied: !this.state.denied})
  };

  render() {
    const {registered} = this.props;
    const {denied} = this.state;

    return (
      <div>
        { registered ? (
          <div>
            <h1>Registration Status:
              <span
                style={{color: (denied ? 'red' : '#21ba45')}}
                onClick={this.toggleStatus}
              >
                 &nbsp;{denied ? "DENIED" : "PENDING"}
              </span>
            </h1>
            <p>
              It looks like you have already applied for authorization to submit documents to this portal.
              <br/>
              {denied ?
                <span>
                  Your application was denied. If you have any questions pertaining to this denial, please
                  <a href="mailto:fake@email.com"> email us</a>.
                </span>
                :
                "Your application is in the process of being reviewed by your agency's designated point of contact."}
            </p>
            <p>Please check the information below.</p>
            <Message warning>
              <p>We have emailed your agency's point of contact: <strong>Jane Doe ( jdoe@mail.com )</strong>.</p>
              <p>
                If this is not your agency's point of contact, please <a href="mailto:fake@email.com">email </a>
                or call us at <a href="tel:+2127888590">212-788-8590</a> immediately.
              </p>
            </Message>
            <Table celled striped>
              <Table.Header>
                <Table.Row>
                  <Table.HeaderCell colSpan="3">John Smith</Table.HeaderCell>
                </Table.Row>
              </Table.Header>
              <Table.Body>
                {/* Agency */}
                <Table.Row>
                  <Table.Cell>
                    Agency
                  </Table.Cell>
                  <Table.Cell>
                    DORIS - Department of Records and Information Services
                  </Table.Cell>
                </Table.Row>
                {/* Email */}
                <Table.Row>
                  <Table.Cell>
                    Email
                  </Table.Cell>
                  <Table.Cell>
                    jsmith@email.com
                  </Table.Cell>
                </Table.Row>
                {/* Phone */}
                <Table.Row>
                  <Table.Cell >
                    Phone
                  </Table.Cell>
                  <Table.Cell>
                    (123) 456-7890
                  </Table.Cell>
                </Table.Row>
                {/* Submission Date */}
                <Table.Row>
                  <Table.Cell>
                    Submission Date
                  </Table.Cell>
                  <Table.Cell>
                    Tuesday April 11, 2017
                  </Table.Cell>
                </Table.Row>
              </Table.Body>
            </Table>
            <h5>
              { denied ? "You can still " : "While waiting for approval, you are free to " }
              <Link to="/search">search</Link> for publications.
            </h5>
          </div>
        ) : (
          <div>
            <h1>Portal Registration</h1>
            <p>
              Welcome to the New York City Government Publications Portal. Each New York City agency should have at
              least one staff member authorized by their agency to submit documents to the Portal in compliance with <a href="http://library.amlegal.com/nxt/gateway.dll/New%20York/charter/newyorkcitycharter/chapter49officersandemployees?f=templates$fn=default.htm$3.0$vid=amlegal:newyork_ny$anc=JD_1133" target="_blank">
                New York City Charter, Title 49, Section 1133</a> requirements.
            </p>
            <p>
              Please fill out the form to register here as an authorized user for your agency. Most fields have been
              pre-populated with information from your user account. Please add your <strong>agency</strong> and
              <strong> telephone number</strong>.
            </p>
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
                  label="I acknowledge that I am the designated agency contact for submission of records to the
                  Municipal Library. If there is any change (such as my reassignment to other duties or some other
                  agency), I will notify my supervisor that a new agency contact for the Municipal Library needs to be
                  appointed and registered."
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