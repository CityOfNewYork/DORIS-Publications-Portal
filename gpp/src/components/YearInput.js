import React, {Component} from 'react';
import {Form, Label, Grid} from 'semantic-ui-react';
import moment from 'moment';
import TooltippedLabel from './TooltippedLabel';
import DateInput from './DateInput';
import './DateInput.css';


class YearInput extends Component {
  static YEAR_TYPE_CAL = 'calendar';
  static YEAR_TYPE_FIS = 'fiscal';
  static YEAR_TYPE_OTH = 'other';

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

    const yearTypePicker = (
      <Grid.Column verticalAlign="bottom" width="4">
        <Form.Select
          compact
          // defaultValue={YearInput.YEAR_TYPE_CAL}  // will cause issues due to remounting below
          options={options}
          onChange={this.onDropdownChange}
          value={this.state.yearType}
        />
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
          />
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
                  name="startDate"
                  maxDate={moment().startOf('day')}
                />
              </Grid.Column>
              <Grid.Column width="6">
                <DateInput
                  label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="Associated End Date"/>}
                  name="endDate"
                />
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
