import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {Form, Label, Grid} from 'semantic-ui-react';
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
    })
  };

  state = {
    yearType: YearInput.YEAR_TYPE_CAL,
    value: ''
  };

  onDropdownChange = (e, {value}) => {
    this.setState({
      yearType: value
    })
  };

  onInputChange = (e, {value}) => {
    if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
      this.setState({
        value: value
      })
    }
  };

  render() {
    const options = [
      {key: "cal", text: "Calendar", value: YearInput.YEAR_TYPE_CAL},
      {key: "fis", text: "NYC Fiscal", value: YearInput.YEAR_TYPE_FIS},
      {key: "oth", text: "Other", value: YearInput.YEAR_TYPE_OTH}
    ];

    const {yearType, value} = this.state;
    const {stateError} = this.props;

    const yearTypePicker = (
      <Grid.Column verticalAlign="bottom" width="4">
        <Form.Select
          compact
          // defaultValue={YearInput.YEAR_TYPE_CAL}  // will cause issues due to remounting below
          options={options}
          name="year_type"
          onChange={this.onDropdownChange}
          value={this.state.yearType}
          error={stateError.hasOwnProperty("year_type")}
        />
        { stateError.hasOwnProperty("year_type") && <ErrorLabel content={ stateError.year_type }/> }
      </Grid.Column>
    );

    const yearPicker = (
      <Grid>
        <Grid.Column width="12">
          <Form.Input
            label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="Associated Year"/>}
            name='year'
            maxLength='4'
            value={value}
            onChange={this.onInputChange}
            error={stateError.hasOwnProperty("year")}
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
            <Grid>
              <Grid.Column width="6">
                <DateInput
                  label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="Associated Start Date"/>}
                  name="start_date"
                  maxDate={moment().startOf('day')}
                  error={stateError.hasOwnProperty("start_date")}
                />
                { stateError.hasOwnProperty("start_date") && <ErrorLabel content={ stateError.start_date }/> }
              </Grid.Column>
              <Grid.Column width="6">
                <DateInput
                  label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="Associated End Date"/>}
                  name="end_date"
                  error={stateError.hasOwnProperty("end_date")}
                />
                { stateError.hasOwnProperty("end_date") && <ErrorLabel content={ stateError.end_date }/> }
              </Grid.Column>
              {yearTypePicker}
            </Grid>
          </div>
        );
      case YearInput.YEAR_TYPE_FIS:
        return (
          <div>
            {yearPicker}
            {value.length === 4 &&
            <Label pointing>
              July 1, {value} – June 30, {parseInt(value, 10) + 1}
            </Label>
            }
          </div>
        );
      default:
        return (
          <div>
            {yearPicker}
            {value.length === 4 &&
            <Label pointing>
              January 1, {value} – December 31, {parseInt(value, 10)}
            </Label>
            }
          </div>
        );
    }
  }
}

export default YearInput;
