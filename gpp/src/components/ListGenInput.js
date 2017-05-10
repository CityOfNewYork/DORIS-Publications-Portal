import React, {Component} from 'react';
import {Form, Icon, List, Segment, Button} from 'semantic-ui-react';

class ListGenInput extends Component {
  state = {
    items: [],
    value: ''
  };

  onAdd = () => {
    if (this.state.value.replace(/^\s+|\s+$/g, '')) {
      this.setState({
        items: [this.state.value, ...this.state.items],
        value: ''
      });
    }
  };

  onRemove = (index) => (e) => {
    e.preventDefault();
    this.setState({
      items: [...this.state.items.slice(0, index), ...this.state.items.slice(index + 1)]
    })
  };

  handleChange = (e, {value}) => {
    this.setState({
      value: value
    })
  };


  render() {
    const items = this.state.items.length > 0 &&
      <Segment>
        <List divided>
          {this.state.items.map((item, index) => (
            <List.Item key={index}>
              <List.Content verticalAlign="middle">
                <Button
                  circular
                  size="mini"
                  icon="remove"
                  onClick={this.onRemove(index)}
                /> {item}
              </List.Content>
            </List.Item>
          ))}
        </List>
      </Segment>;

    return (
      <Form.Field>
        <Form.Input
          {...this.props}
          icon={<Icon name="add" inverted circular link onClick={this.onAdd}/>}
          onChange={this.handleChange}
          value={this.state.value}
          onKeyDown={(e) => {
            if (e.key === 'Enter'){
              e.preventDefault();
              this.onAdd();
            }
          }}
        />
        {items}
      </Form.Field>
    )
  }
}

export default ListGenInput;
