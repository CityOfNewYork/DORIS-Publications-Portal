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
          label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="File(s)"/>}
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
        <Form.Group>
          <Form.Field width="16">
            <Form.Input
              label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="Title"/>}
              placeholder="Look at me, I'm a Title."
              name="title"
              error={stateError.hasOwnProperty("title")}
              onChange={handleFieldChange}
              required
            />
            { stateError.hasOwnProperty("title") && <ErrorLabel content={ stateError.title }/> }
          </Form.Field>
        </Form.Group>

        {/* Sub-Title */}
        <Form.Group>
          <Form.Field width="16">
            <Form.Input
              label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="Sub-Title"/>}
              placeholder="I am inferior."
              name="subtitle"
              error={stateError.hasOwnProperty("subtitle")}
              onChange={handleFieldChange}
            />
            { stateError.hasOwnProperty("subtitle") && <ErrorLabel content={ stateError.title }/> }
          </Form.Field>
        </Form.Group>

        {/* Agency */}
        <Form.Group>
          <Form.Field width="16">
            <Form.Dropdown
              required
              label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="Agency"/>}
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
              error={stateError.hasOwnProperty("agency")}
              placeholder="Select Your Agency"
            />
            { stateError.hasOwnProperty("agency") && <ErrorLabel content={ stateError.agency }/> }
          </Form.Field>
        </Form.Group>

        {/* Additional Creators */ }
        <ListGenInput
          label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="Additional Creators"/>}
          ref={(creatorList) => {
            this.creatorList = creatorList
          }}
        />

        <Form.Group>
          {/* Type */}
          <Form.Field width="6">
            <Form.Select
              label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="Type"/>}
              name="type"
              options={[
                {key: 'f', text: 'Foo', value: 'foo'},
                {key: 'b', text: 'Bar', value: 'bar'}
              ]}
              error={stateError.hasOwnProperty("type")}
              onChange={handleFieldChange}
              search
              required
            />
            { stateError.hasOwnProperty("type") && <ErrorLabel content={ stateError.type }/> }
          </Form.Field>

          {/* Subjects TODO: limit to 3? */}
          <Form.Field width="10">
            <Form.Dropdown
              required
              label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="Subject(s)"/>}
              name="subjects"
              fluid
              multiple
              search
              selection
              options={[
                {key: 'f', text: 'Foo', value: 'foo'},
                {key: 'b', text: 'Bar', value: 'bar'}
              ]}
              error={stateError.hasOwnProperty("subjects")}
            />
            { stateError.hasOwnProperty("subjects") && <ErrorLabel content={ stateError.subjects }/> }
          </Form.Field>

        </Form.Group>

        <Form.Group>
          {/* Date Published */}
          <Form.Field width="4">
            <DateInput
              label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="Date Published"/>}
              name="date_published"
              maxDate={moment().startOf('day')}
              error={stateError.hasOwnProperty("date_published")}
            />
            { stateError.hasOwnProperty("date_published") && <ErrorLabel content={ stateError.date_published }/> }
          </Form.Field>

          {/* Year */}
          <Form.Field width="12">
            <YearInput stateError={stateError}/>
          </Form.Field>
        </Form.Group>

        {/* Description */}
        <Form.Group>
          <Form.Field width="16">
            <Form.TextArea
              label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="Description"/>}
              placeholder="Look at me, I'm a Description. LOOK AT ME."
              name="description"
              error={stateError.hasOwnProperty("description")}
              onChange={handleFieldChange}
              required
            />
            { stateError.hasOwnProperty("description") && <ErrorLabel content={ stateError.description }/> }
          </Form.Field>
        </Form.Group>

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
  "api/v1.0/document",
  SubmitForm
);
