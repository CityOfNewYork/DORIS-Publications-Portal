import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {Message, Form} from 'semantic-ui-react';
import {ErrorLabel, withValidation} from './custom';
import FileUpload from './FileUpload';
import Date from './Datepicker';
import ListGenInput from './ListGenInput';


class SubmitForm extends Component {
  static propTypes = {
    stateError: PropTypes.oneOfType([
      PropTypes.object.isRequired,
      PropTypes.string.isRequired,
    ]),
    stateLoading: PropTypes.bool.isRequired,
    handleFieldChange: PropTypes.func.isRequired,
    submitFormData: PropTypes.func.isRequired,
  };

  state = {
    submitted: false,
  };

  handleSubmit = (e) => {
    e.preventDefault();

    this.setState({
      submitted: true
    });

    this.props.submitFormData({
      filenames: this.fileUpload.state.files.map((file) => {
        return file.name;
      }),
      creators: this.creatorList.state.items
    });
  };

  render() {
    const {stateError, stateLoading, handleFieldChange} = this.props;

    return (
      <Form
        onSubmit={this.handleSubmit}
        // only set error attribute if there is an error *message*
        { ...typeof stateError === "string" && {error: true} }
        { ...stateLoading && {loading: true} }
      >
        <h2>Document Submission</h2>
        {/* Files */}
        <Form.Field
          required
          label="File(s)"
        />
        <Form.Field>
          <FileUpload
            ref={(fileUpload) => {this.fileUpload = fileUpload}}
            required
            submitted={this.state.submitted}
          /> {/* TODO: deal with server error? */}
        </Form.Field>
        <ListGenInput
          label="Additional Creators"
          ref={(creatorList) => {this.creatorList = creatorList}}
        />
        <Form.Group widths="equal">
          {/* Title */}
          <Form.Field>
            <Form.Input
              label="Title"
              placeholder="Look at me, I'm a Title."
              name="title"
              { ...stateError.hasOwnProperty("title") ? {error: true} : {}}
              onChange={handleFieldChange}
              maxLength="10"
              required
            />
            { stateError.hasOwnProperty("title") && <ErrorLabel content={ stateError.title }/> }
          </Form.Field>
          <Form.Field>
            <Form.Select
              label="Type"
              name="type"
              options={[
                {key: 'f', text: 'Foo', value: 'foo'},
                {key: 'b', text: 'Bar', value: 'bar'}
              ]}
              { ...stateError.hasOwnProperty("type") ? {error: true} : {}}
              onChange={handleFieldChange}
              required
            />
            { stateError.hasOwnProperty("type") && <ErrorLabel content={ stateError.type }/> }
          </Form.Field>
        </Form.Group>

        <Form.Field>
          {/* Description */}
          <Form.TextArea
            label="Description"
            placeholder="Look at me, I'm a Description. LOOK AT ME."
            name="description"
            { ...stateError.hasOwnProperty("description") ? {error: true} : {}}
            onChange={handleFieldChange}
            required
          />
          { stateError.hasOwnProperty("description") && <ErrorLabel content={ stateError.description }/> }
        </Form.Field>

        <Form.Button fluid>Submit</Form.Button>

        <Message
          error
          header="There was an error with your submission"
          content={ typeof stateError === "string" ? stateError : "" }
        />
      </Form>
    )
  }
}

export default withValidation(
  "post",
  "api/v1.0/publication",
  SubmitForm
);
