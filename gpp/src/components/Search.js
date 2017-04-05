import React, {Component} from 'react'
import {Select, Form} from 'semantic-ui-react'

class Search extends Component {

  state = {
    showAdvanced: true,
  };

  render() {
    return (
      <div>
        <p>
          Vestibulum id ligula porta felis euismod semper. Praesent commodo cursus magna, vel scelerisque nisl
          consectetur et. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa
          justo sit amet risus. Maecenas sed diam eget risus varius blandit sit amet non magna. Cum sociis natoque
          penatibus et magnis dis parturient montes, nascetur ridiculus mus.
        </p>
        <Form>
          <Form.Input
            icon="search"
            iconPosition="left"
            placeholder="cool dynamic placeholder (if value empty)"
            action={
              <Select
                compact
                options={[
                  {key: "metadata", text: "Metadata", value: "metadata"},
                  {key: "document", text: "Documents", value: "document"}
                ]}
                defaultValue="metadata"
              />
            }
          />
        </Form>
      </div>
    )
  }
}

export default Search;
