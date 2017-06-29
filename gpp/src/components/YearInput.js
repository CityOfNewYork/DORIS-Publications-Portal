import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {Form, Label, Grid, Segment} from 'semantic-ui-react';
import moment from 'moment';
import TooltippedLabel from './TooltippedLabel';
import {ErrorLabel} from './custom';
import DateInput from './DateInput';
import './DateInput.css';


class YearInput extends Component {
  static YEAR_TYPE_CAL = 'calendar';
  static YEAR_TYPE_FIS = 'fiscal';
  static YEAR_TYPE_OTH = 'other';

  static props = {
    stateError: PropTypes.shape({
      year: PropTypes.string,
      start_date: PropTypes.string,
      end_date: PropTypes.string,
      year_type: PropTypes.string
    }),
    removeError: PropTypes.func.isRequired,
    onBlur: PropTypes.func.isRequired
  };

  state = {
    yearType: YearInput.YEAR_TYPE_CAL,
    year: '',
  };

  onDropdownChange = (e, {value}) => {
    this.setState({
      yearType: value,
      year: ''
    })
  };

  onYearChange = (e, {value}) => {
    this.props.removeError("year");
    if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
      this.setState({
        year: value
      })
    }
  };

  render() {
    const options = [
      {key: "cal", text: "Calendar", value: YearInput.YEAR_TYPE_CAL},
      {key: "fis", text: "NYC Fiscal", value: YearInput.YEAR_TYPE_FIS},
      {key: "oth", text: "Other", value: YearInput.YEAR_TYPE_OTH}
    ];

    const {yearType, year} = this.state;
    const {stateError, removeError, onBlur} = this.props;

    const yearTypePicker = (
      <Grid.Column width="4">
        <Form.Select
          compact
          // defaultValue={YearInput.YEAR_TYPE_CAL}  // will cause issues due to remounting below
          options={options}
          name="year_type"
          onChange={this.onDropdownChange}
          value={yearType}
          error={stateError.hasOwnProperty("year_type")}
          style={{marginTop: 29}}
        />
        { stateError.hasOwnProperty("year_type") && <ErrorLabel content={ stateError.year_type }/> }
      </Grid.Column>
    );

    const yearPicker = (
      <Grid>
        <Grid.Column width="12">
          <Form.Input
            label={
              <TooltippedLabel
                tooltipContent='The year covered by this publication. If multiple years are covered,
                pick "Other" in the dropdown to the right.'
                labelContent="Associated Year"
              />
            }
            name='year'
            maxLength='4'
            required
            value={year}
            onChange={this.onYearChange}
            error={stateError.hasOwnProperty("year")}
            onBlur={onBlur}
          />
          { stateError.hasOwnProperty("year") && <ErrorLabel content={ stateError.year }/> }
        </Grid.Column>
        {yearTypePicker}
      </Grid>
    );

    switch (yearType) {
      case YearInput.YEAR_TYPE_OTH:
        return (
          <div>
            <Segment>
              <Grid>
                <Grid.Column width="6">
                  <DateInput
                    label={
                      <TooltippedLabel
                        tooltipContent="The start date covered by this document."
                        labelContent="Associated Start Date"
                      />
                    }
                    name="start_date"
                    ref={(startDate) => this.startDate = startDate}
                    maxDate={moment().startOf('day')}
                    error={stateError.hasOwnProperty("start_date")}
                    onChange={() => removeError("start_date")}
                    onBlur={onBlur}
                  />
                  { stateError.hasOwnProperty("start_date") && <ErrorLabel content={ stateError.start_date }/> }
                </Grid.Column>
                <Grid.Column width="6">
                  <DateInput
                    label={
                      <TooltippedLabel
                        tooltipContent="The end date covered by this document."
                        labelContent="Associated End Date"/>
                    }
                    name="end_date"
                    ref={(endDate) => this.endDate = endDate}
                    error={stateError.hasOwnProperty("end_date")}
                    onChange={() => removeError("end_date")}
                    onBlur={onBlur}
                  />
                  { stateError.hasOwnProperty("end_date") && <ErrorLabel content={ stateError.end_date }/> }
                </Grid.Column>
                {yearTypePicker}
              </Grid>
            </Segment>
          </div>
        );
      case YearInput.YEAR_TYPE_FIS:
        return (
          <div>
            <Segment>
              {yearPicker}
              {
                year.length === 4 && !stateError.hasOwnProperty("year") &&
                <Label pointing>
                  July 1, {year} – June 30, {parseInt(year, 10) + 1}
                </Label>
              }
            </Segment>
          </div>
        );
      default:
        return (
          <div>
            <Segment>
              {yearPicker}
              {year.length === 4 && !stateError.hasOwnProperty("year") &&
              <Label pointing>
                January 1, {year} – December 31, {parseInt(year, 10)}
              </Label>
              }
            </Segment>
          </div>
        );
    }
  }
}

export default YearInput;
