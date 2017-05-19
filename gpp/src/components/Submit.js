import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {Message, Form, Button} from 'semantic-ui-react';
import moment from 'moment';
import {ErrorLabel, withValidation} from './custom';
import FileUpload from './FileUpload';
import DateInput from './DateInput';
import ListGenInput from './ListGenInput';
import YearInput from './YearInput';
import TooltippedLabel from './TooltippedLabel';


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
          label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="File(s)" />}
        />
        <Form.Field>
          <FileUpload
            ref={(fileUpload) => {
              this.fileUpload = fileUpload
            }}
            required
            submitted={this.state.submitted}
            uploadDirName="some_ID"
          /> {/* TODO: uploadDirName = current user's guid? */}
        </Form.Field>

        {/* Title */}
        <Form.Field>
          <Form.Input
            label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="Title" />}
            placeholder="Look at me, I'm a Title."
            name="title"
            { ...stateError.hasOwnProperty("title") ? {error: true} : {}}
            onChange={handleFieldChange}
            required
          />
          { stateError.hasOwnProperty("title") && <ErrorLabel content={ stateError.title }/> }
        </Form.Field>

        {/* Sub-Title */}
        <Form.Field>
          <Form.Input
            label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="Sub-Title" />}
            placeholder="I am inferior."
            name="subtitle"
            { ...stateError.hasOwnProperty("subtitle") ? {error: true} : {}}
            onChange={handleFieldChange}
          />
          { stateError.hasOwnProperty("subtitle") && <ErrorLabel content={ stateError.title }/> }
        </Form.Field>

        {/* Agency */}
        <Form.Dropdown
          required
          label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="Agency" />}
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

        {/* Additional Creators */ }
        <ListGenInput
          label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="Additional Creators" />}
          ref={(creatorList) => {
            this.creatorList = creatorList
          }}
        />

        <Form.Group>
          {/* Type */}
          <Form.Field width="6">
            <Form.Select
              label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="Type" />}
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

          {/* TODO: limit to 3? */}
          <Form.Field width="10">
            <Form.Dropdown
              required
              label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="Subject(s)" />}
              name="subjects"
              fluid
              multiple
              search
              selection
              options={[
                {key: 'f', text: 'Foo', value: 'foo'},
                {key: 'b', text: 'Bar', value: 'bar'}
              ]} />
          </Form.Field>

        </Form.Group>

        <Form.Group>
        {/* Date Published */}
          <Form.Field width="4">
            <DateInput
              label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="Date Published" />}
              name="datePublished"
              maxDate={moment().startOf('day')}
            />
          </Form.Field>

          {/* Year */}
          <Form.Field width="12">
            <YearInput/>
          </Form.Field>
        </Form.Group>

        {/* Description */}
        <Form.Field>
          <Form.TextArea
            label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="Description" />}
            placeholder="Look at me, I'm a Description. LOOK AT ME."
            name="description"
            { ...stateError.hasOwnProperty("description") ? {error: true} : {}}
            onChange={handleFieldChange}
            required
          />
          { stateError.hasOwnProperty("description") && <ErrorLabel content={ stateError.description }/> }
        </Form.Field>

        <Button.Group widths="2">
          <Button color="blue" icon="send" content="Submit"/>
          <Button.Or/>
          <Button color="green" icon="save" content="Save"/>
        </Button.Group>

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
