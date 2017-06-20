/**
 * Custom and utility components that can be used alongside semantic-ui-react components
 */
import React from 'react';
import {Label} from 'semantic-ui-react';
import {PropTypes} from 'prop-types';
import {csrfFetch} from '../utils/fetch';
import {omit} from '../utils/object';
import {validate_property} from '../utils/jsonschema';


/**
 * Use this to display error messages directly below a form field.
 *
 * Example:
 *    <Form.Field>
 *      <Form.Input ... />
 *      { isThereAnError && <ErrorLabel content=( theError }/>
 *    </Form.Field>
 */
const ErrorLabel = ({content, style}) => (
  <Label style={style}
         className="prompt"
         pointing
         color="red"
         content={Array.isArray(content) ? content.join(" ") : content}/>
);

ErrorLabel.propTypes = {
  content: PropTypes.oneOfType([
    PropTypes.string.isRequired,
    PropTypes.arrayOf(PropTypes.string).isRequired
  ])
};

/**
 * A higher-order component (HOC) that provides basic validation functionality
 * and helper functions. Form data that can be captured from basic fields and
 * errors from the server response are stored in state.
 *
 * @param method Request method
 * @param action Request endpoint
 * @param FormComponent Form component to wrap
 */
function withValidation(method, action, FormComponent) {
  return class extends React.Component {
    state = {
      data: {},
      error: {},
      successMessage: '',
      loading: false,
    };

    removeError = (inputName) => {
      if (this.state.error.hasOwnProperty(inputName)) {
        this.setState({error: omit(this.state.error, inputName)});
      }
    };

    handleFieldChange = (e, {name, value}) => {
      this.setState({
        data: {
          ...this.state.data,
          [name]: typeof value === "string" ? value.replace(/^\s+|\s+$/g, '') : value
        }
      });
      this.removeError(name);
    };

    validateProperty = (schema) => (e) => {
      const {value} = e.target;
      this.validatePropertySynthetic(schema)(e, {
        name: e.target.name,
        value: /^\d+$/.test(value) ? parseInt(value, 10) : value
      })
    };

    validatePropertySynthetic = (schema) => (e, {name, value}) => {
      const errors = validate_property({[name]: value}, schema, name);
      if (errors.length > 0) {
        this.setState({
          error: {...this.state.error, [name]: errors}
        })
      }
    };

    submitFormData = (extraData = {}) => {
      // set loading to true to show form loading spinner
      this.setState({loading: true});

      // TODO: check formData for typos and display warning message

      const ERR_MSG = "We cannot process your submission at this time.";

      let formData = {};
      const {data} = this.state;
      for (let prop in data) {
        if (data[prop]) {
          formData[prop] = data[prop]
        }
      }

      csrfFetch(action, {
        method: method,
        body: JSON.stringify({...formData, ...extraData}),
      }).then((response) => {
        // stop loading
        this.setState({loading: false});
        // get response json data
        return response.json()
      }).then((json) => {
        // interpret valid JSend response here
        switch (json.status) {
          case "success":
            this.setState({error: {}, successMessage: json.data.success_message.text});
            break;
          case "fail":
            this.setState({error: json.data});
            break;
          case "error":
            this.setState({error: json.message});
            break;
          default:
            // considered an error as well
            this.setState({
              error: json.hasOwnProperty("message") ? json.message : ERR_MSG
            });
        }
      }).catch((err) => {
        // Issue was an unhandled 500, show generic error message.
        this.setState({
          error: ERR_MSG
        });
      });
    };

    render() {
      return <FormComponent
        stateError={ this.state.error }
        stateLoading={ this.state.loading }
        submitFormData={ this.submitFormData }
        handleFieldChange={ this.handleFieldChange }
        removeError={ this.removeError }
        validateProperty={ this.validateProperty }
        validatePropertySynthetic={ this.validatePropertySynthetic }
        successMessage={ this.state.successMessage }
      />
    }
  }
}

export {ErrorLabel, withValidation};
