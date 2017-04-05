/**
 * Custom components that can be used alongside semantic-ui-react components
 */
import React from 'react'
import {csrfFetch} from '../utils/fetch'
import {omit} from '../utils/object'


/**
 * Use this to display error, warning, etc. messages directly below a form field.
 *
 * Example:
 *    <Form.Field>
 *      <Form.Input ... />
 *      { isThereAnError && <FormFieldPrompt content=( theError }/>
 *    </Form.Field>
 */
const FormFieldPrompt = ({content}) => (
  <div className="ui basic red pointing prompt label">
    { content }
  </div>
);

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
          [name]: value
        }});
      this.removeError(name);
    };

    submitFormData = (extraData = {}) => {
      // set loading to true to show form loading spinner
      this.setState({loading: true});

      // TODO: check formData for typos and display warning message

      const ERR_MSG = "We cannot process your submission at this time.";

      csrfFetch(action, {
        method: method,
        body: JSON.stringify({...this.state.data, ...extraData}),
      }).then((response) => {
        // stop loading
        this.setState({loading: false});
        // get response json data
        return response.json()
      }).then((json) => {
        // interpret valid JSend response here
        switch (json.status) {
          case "success":
            this.setState({error: {}});
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
      />
    }
  }
}

export {FormFieldPrompt, withValidation};
