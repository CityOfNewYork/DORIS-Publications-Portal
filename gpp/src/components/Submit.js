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
import schema from '../utils/schemas/document'


class SubmitForm extends Component {
  static propTypes = {
    stateError: PropTypes.oneOfType([
      PropTypes.object.isRequired,
      PropTypes.string.isRequired,
    ]),
    successMessage: PropTypes.string.isRequired,
    stateLoading: PropTypes.bool.isRequired,
    handleFieldChange: PropTypes.func.isRequired,
    submitFormData: PropTypes.func.isRequired,
    removeError: PropTypes.func.isRequired,
    validateProperty: PropTypes.func.isRequired,
    validatePropertySynthetic: PropTypes.func.isRequired
  };

  state = {
    submitted: false,
    reportTypeChoices: [],
    subjects: [],
    subjectsChoices: [],
    language: "english",
    languageChoices: [],
    descriptionCharCount: 0,
  };

  fetchChoices = (endpoint, stateKey) => {
    fetch(endpoint).then((response) => (
      response.json()
    )).then((json) => {
      this.setState({
        [stateKey]: json.data.map((item) => ({
          key: item.value,
          text: item.text,
          value: item.value
        }))
      })
    }).catch(() => {
      this.setState({
        [stateKey]: [{
          key: 'none',
          text: 'None - Check Server',
          value: 'none'
        }]
      })
    })
  };

  componentWillMount() {
    this.fetchChoices('/api/v1.0/subjects', 'subjectsChoices');
    this.fetchChoices('/api/v1.0/report_types', 'reportTypeChoices');
    this.fetchChoices('/api/v1.0/languages', 'languageChoices')
  }

  handleSubmit = (e) => {
    e.preventDefault();

    this.setState({
      submitted: true
    });

    /**
     * Convert Moment object from dateRef into formatted string if present.
     */
    const formatDate = (dateRef) => (
      dateRef && dateRef.state.date ? dateRef.state.date.format('MM/DD/YYYY') : ''
    );

    const {startDate, endDate} = this.year;
    let formData = {
      files: this.fileUpload.state.files.map((file) => {
        return {
          "title": file.title,
          "name": file.name
        };
      }),
      creators: this.creatorList.state.items,
      date_published: formatDate(this.datePublished),
      year_type: this.year.state.yearType
    };

    const optionalData = {
      year: parseInt(this.year.state.year, 10),
      start_date: formatDate(startDate),
      end_date: formatDate(endDate)
    };

    for (let prop in optionalData) {
      if (optionalData[prop]) {
        formData[prop] = optionalData[prop]
      }
    }

    this.props.submitFormData(formData);
  };

  onDescriptionChange = (e, {name, value}) => {
    this.setState({
      descriptionCharCount: value.length
    });
    this.props.handleFieldChange(e, {name: name, value: value})
  };

  onSubjectsChange = (e, {name, value}) => {
    if (value.length <= 3) {
      this.setState({
        subjects: value
      });
      this.props.handleFieldChange(e, {name: name, value: value})
    }
  };

  // TODO: utilize this across other fields and functions (onSubjectsChange)? might need this in order to validate json schema
  onLanguageChange = (e, {name, value}) => {
    this.setState({
      [name]: value
    });
    this.props.handleFieldChange(e, {name: name, value: value})
  };

  render() {
    const {stateError, successMessage, stateLoading, handleFieldChange, removeError, validateProperty, validatePropertySynthetic} = this.props;
    const {submitted, subjects, language, descriptionCharCount, subjectsChoices, reportTypeChoices, languageChoices} = this.state;
    return (
      <Form
        onSubmit={this.handleSubmit}
        // only set error attribute if there is an error *message*
        { ...stateLoading && {loading: true} }
        error
        warning
        success
      >
        {successMessage &&
        <Message success>
          {successMessage}
        </Message>
        }
        <h2>Document Submission</h2>

        {/* Files */}
        <Form.Field
          required
          label={
            <TooltippedLabel
              tooltipContent="Please provide all files associated with the document you are submitting."
              labelContent="File(s)"
            />
          }
        />
        <Form.Field>
          <FileUpload
            ref={(fileUpload) => {
              this.fileUpload = fileUpload
            }}
            required
            submitted={submitted}
            uploadDirName="some_ID"
            errors={stateError.hasOwnProperty("files") ? stateError.files : []}
          /> {/* TODO: uploadDirName = current user's guid? */}
        </Form.Field>

        {/* Title */}
        <Form.Group>
          <Form.Field width="16">
            <Form.Input
              label={
                <TooltippedLabel
                  tooltipContent="On the front page, the first page or in the Executive Summary (if any) of
                  the document, what is it called? 150 characters or fewer."
                  labelContent="Title"
                />
              }
              placeholder="Audit Report on the Department of Flying Monkeys"
              name="title"
              error={stateError.hasOwnProperty("title")}
              onChange={handleFieldChange}
              onBlur={validateProperty(schema)}
              required
              maxLength="150"
            />
            { stateError.hasOwnProperty("title") && <ErrorLabel content={ stateError.title }/> }
          </Form.Field>
        </Form.Group>

        {/* Sub-Title */}
        <Form.Group>
          <Form.Field width="16">
            <Form.Input
              label={
                <TooltippedLabel
                  tooltipContent="The remainder of the document's title, if any. 150 characters or fewer."
                  labelContent="Sub-Title"/>
              }
              placeholder="Follow-up Audit Report"
              name="subtitle"
              error={stateError.hasOwnProperty("subtitle")}
              onChange={handleFieldChange}
              onBlur={validateProperty(schema)}
              maxLength="150"
            />
            { stateError.hasOwnProperty("subtitle") && <ErrorLabel content={ stateError.title }/> }
          </Form.Field>
        </Form.Group>

        {/* Agency */}
        <Form.Group>
          <Form.Field width="16">
            <Form.Dropdown
              required
              label={
                <TooltippedLabel
                  tooltipContent="What agency is the primary creator of this document?"
                  labelContent="Agency"
                />
              }
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
              selectOnBlur={false}
              onBlur={validatePropertySynthetic(schema)}
              onChange={handleFieldChange}
              error={stateError.hasOwnProperty("agency")}
              placeholder="Select an Agency"
            />
            { stateError.hasOwnProperty("agency") && <ErrorLabel content={ stateError.agency }/> }
          </Form.Field>
        </Form.Group>

        {/* Additional Creators */ }
        <ListGenInput
          label={
            <TooltippedLabel
              tooltipContent="What other agencies, consultants, or authors, if any, contributed to the
              creation of this document? To add authors, click the plus sign or press [enter] after
              you have filled out the field."
              labelContent="Additional Creators"/>
          }
          ref={(creatorList) => {
            this.creatorList = creatorList
          }}
        />

        <Form.Group>
          {/* Report Type */}
          <Form.Field width="6">
            <Form.Select
              label={
                <TooltippedLabel
                  tooltipContent="Start typing in the box (which will autofill) or use dropdown for a list
                  of the most common kinds of reports and pick the one closest to what you are submitting."
                  labelContent="Report Type"
                />
              }
              name="report_type"
              options={reportTypeChoices}
              error={stateError.hasOwnProperty("report_type")}
              onBlur={validatePropertySynthetic(schema)}
              onChange={handleFieldChange}
              selectOnBlur={false}
              placeholder="Select a Document Type"
              search
              required
            />
            { stateError.hasOwnProperty("report_type") && <ErrorLabel content={ stateError.report_type }/> }
          </Form.Field>

          {/* Subjects */}
          <Form.Field width="6">
            <Form.Dropdown
              required
              label={
                <TooltippedLabel
                  tooltipContent="Select what subjects you feel are the most relevant subjects covered in this report.
                  Pick up to three. Start typing in the box (which will autofill), or use dropdown to pick subjects."
                  labelContent="Subject(s)"
                />
              }
              name="subjects"
              fluid
              multiple
              search
              selection
              value={subjects}
              onChange={this.onSubjectsChange}
              onBlur={validatePropertySynthetic(schema)}
              placeholder="Select up to 3 Subjects"
              options={subjectsChoices}
              error={stateError.hasOwnProperty("subjects")}
            />
            { stateError.hasOwnProperty("subjects") && <ErrorLabel content={ stateError.subjects }/> }
          </Form.Field>

          {/* Language */}
          <Form.Field width="4">
            <Form.Dropdown
              required
              label={
                <TooltippedLabel
                  tooltipContent="If the publication is written in a language other than English, pick the language
                  from the dropdown list. English is the default choice."
                  labelContent="Language"
                />
              }
              fluid
              selection
              name="language"
              value={language}
              onBlur={validatePropertySynthetic(schema)}
              onChange={this.onLanguageChange}
              options={languageChoices}
              error={stateError.hasOwnProperty("language")}
            />
            { stateError.hasOwnProperty("language") && <ErrorLabel content={ stateError.language }/> }
          </Form.Field>
        </Form.Group>

        <Form.Group>
          {/* Date Published */}
          <Form.Field width="16">
            <DateInput
              label={
                <TooltippedLabel
                  tooltipContent="This document's date of publication by the agency."
                  labelContent="Date Published"
                />
              }
              name="date_published"
              maxDate={moment().startOf('day')}
              error={stateError.hasOwnProperty("date_published")}
              ref={(datePublished) => this.datePublished = datePublished}
              onChange={() => removeError("date_published")}
              onBlur={validateProperty(schema)}
            />
            { stateError.hasOwnProperty("date_published") && <ErrorLabel content={ stateError.date_published }/> }
          </Form.Field>
        </Form.Group>

        <Form.Group>
          {/* Year */}
          <Form.Field width="16">
            <YearInput
              stateError={stateError}
              ref={(year) => this.year = year}
              removeError={removeError}
              onBlur={validateProperty(schema)}
            />
          </Form.Field>
        </Form.Group>

        {/* Description */}
        <Form.Group>
          <Form.Field width="16">
            <Form.TextArea
              label={
                <label>
                  <TooltippedLabel
                    tooltipContent="A brief (100 - 200 characters) explanation of the contents of this document."
                    labelContent="Description"
                  />
                  <span
                    style={{color: descriptionCharCount < 100 ? "red" : "green", float: "right", fontWeight: "normal"}}>
                    {descriptionCharCount}
                  </span>
                </label>
              }
              name="description"
              error={stateError.hasOwnProperty("description")}
              onChange={this.onDescriptionChange}
              onBlur={validateProperty(schema)}
              required
              maxLength="200"
              rows="3"
            />
            { stateError.hasOwnProperty("description") && <ErrorLabel content={ stateError.description }/> }
          </Form.Field>
        </Form.Group>

        <Button.Group widths="2">
          <Button color="blue" icon="send" content="Submit"/>
          <Button.Or/>
          <Button color="green" icon="save" content="Save"/>
        </Button.Group>

        { typeof stateError === "string" &&
        <Message
          error
          header="There was an error with your submission"
          content={ typeof stateError === "string" ? stateError : "" }
        />
        }
      </Form>
    )
  }
}

export default withValidation(
  "post",
  "api/v1.0/document",
  SubmitForm
);
