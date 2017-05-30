import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {MaskedInput} from 'react-text-mask';
import {Form} from 'semantic-ui-react';
import DatePicker from 'react-datepicker';
import moment from 'moment';
import 'react-datepicker/dist/react-datepicker.css';
import './DateInput.css';

class Input extends Component {  // Must be a class; DatePicker gives its customInput prop a ref
  render() {
    const {error, onClick, onChange, value, label, name} = this.props;
    return (
      <Form.Input
        error={error}
        // required
        label={label}
        name={name}
        children={
          <MaskedInput
            mask={[/\d/, /\d/, '/', /\d/, /\d/, '/', /\d/, /\d/, /\d/, /\d/]}
            placeholder="MM/DD/YYYY"
            // required
            pattern="(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.]\d\d\d\d"
            onClick={onClick}
            value={value}
            onChange={onChange}
          />
        }
      />
    )
  }
}


class DateInput extends Component {
  static propTypes = {
    label: PropTypes.oneOfType([
      PropTypes.string.isRequired,
      PropTypes.element.isRequired
    ]),
    name: PropTypes.string.isRequired,
    maxDate: PropTypes.object,
    error: PropTypes.bool.isRequired,
    onChange: PropTypes.func.isRequired
  };

  state = {
    date: undefined,
    moment: this.props.maxDate || null,
    dateError: false
  };

  handleChange = (date) => {
    this.props.onChange();
    this.setState({
      date: date,
      dateError: false
    });
  };

  static isValidDate(month, day, year) {
    const date = new Date(year, month - 1, day);
    // eslint-disable-next-line
    return date && date.getMonth() + 1 == month;  // this is a perfectly reasonable use of type coercion
  }

  handleChangeRaw = (e) => {
    this.props.onChange();
    const value = e.target.value,
      // .match returns null if value is not in the format: DD/DD/DDDD
      dateMatch = (value).match(/^(\d{2})\/(\d{2})\/(\d{4})$/),
      parsedDate = Date.parse(value);
    const invalidFormat = dateMatch === null || !DateInput.isValidDate(...value.split("/"));
    this.setState({
      // .diff will return negative values if the parsedDate is greater than today
      dateError: (
        invalidFormat || (this.state.moment && this.state.moment.diff(parsedDate, 'days') < 0)
      )
    });
    // update the date value if the format is valid, even though the date itself might be wrong
    if (!invalidFormat) {
      this.setState({
        date: moment(value, "MM/DD/YYYY")
      })
    }
  };

  render() {
    const {date, moment, dateError} = this.state;
    const {label, name, error} = this.props;
    return <DatePicker
      maxDate={moment}
      selected={date}
      customInput={
        <Input
          onChange={this.handleChange}
          error={dateError || error}
          label={label}
          name={name}
        />
      }
      onChange={this.handleChange}
      onChangeRaw={this.handleChangeRaw}
    />;
  }
}

export default DateInput;
