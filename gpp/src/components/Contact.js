import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {Container} from 'semantic-ui-react';


class Contact extends Component {
  static propTypes = {
    authenticatedFE : PropTypes.bool.isRequired,
  };

  render() {
    const {authenticatedFE} = this.props;

    return (
      <Container>
        <h1>Contact Us</h1>
        {/* Agency Contact */}
        { authenticatedFE ? (
          <div>
            <p>
              Contact us <a href="mailto:munilib@records.nyc.gov">here</a> or call us at 212-788-8950.
            </p>
          </div>
        ) : (
          <div>
            <p>(Contact Form)</p>
          </div>
        )
        }
      </Container>
    )
  }
}

export default Contact;
