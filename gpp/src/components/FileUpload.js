import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {Progress, Grid, Segment, Message, Icon, Form} from 'semantic-ui-react';
import {readCookie} from '../utils/cookie';
import {csrfFetch} from '../utils/fetch';
import {ErrorLabel} from './custom';


class FileRow extends Component {

  static propTypes = {
    file: PropTypes.shape({
      size: PropTypes.number.isRequired,
      name: PropTypes.string.isRequired,
    }),
    index: PropTypes.number.isRequired,
    isLast: PropTypes.bool.isRequired,
    onRemove: PropTypes.func.isRequired,
    onShiftDown: PropTypes.func.isRequired,
    onShiftUp: PropTypes.func.isRequired
  };

  state = {
    percent: 0,
    error: "",
    uploading: true,
  };

  // Fetch API does not support upload progress yet.
  xhr = new XMLHttpRequest();

  /**
   * Update this.state.percent to match upload progress.
   */
  uploadProgress = (e) => {
    if (e.lengthComputable) {
      this.setState({
        percent: (e.loaded / e.total) * 100
      });
    }
  };

  /**
   * Set this.state.error message.
   * The server is probably not responding.
   */
  uploadFailed = () => {
    this.setState({
      percent: 100,
      error: "Failed to upload file. Please remove and try again.",
      uploading: false
    })
  };

  /**
   * Check completed XHR response for errors.
   */
  parseResponse = () => {
    let errorMsg = "";
    if (this.xhr.status !== 200) {
      try {
        errorMsg = JSON.parse(this.xhr.responseText);
      }
      catch (err) {
        errorMsg = {
          message: "Failed to upload file due to an unhandled server error. Please remove and try again."
        }
      }
    }
    this.setState({
      percent: 100,
      error: errorMsg.message || errorMsg.data,
      uploading: false
    })
  };

  /**
   * FileRow has been mounted, so start uploading this.props.file.
   */
  componentDidMount() {
    // TODO: frontend validation (number?, size?, total size?, mimetype, user authenticated, etc.)
    let data = new FormData();
    data.append("file", this.props.file);
    this.xhr.upload.addEventListener("progress", this.uploadProgress);
    this.xhr.upload.addEventListener("error", this.uploadFailed);
    this.xhr.open("POST", "/api/v1.0/upload");
    this.xhr.setRequestHeader("X-CSRFToken", readCookie("csrf_token"));
    this.xhr.onload = this.parseResponse;
    this.xhr.send(data);
  }

  /**
   * FileRow is about to un-mount, so cancel the upload if the
   * request has not completed. Otherwise, DELETE the uploaded file.
   * If the upload has failed, do nothing.
   */
  componentWillUnmount() {
    if (this.xhr.readyState !== XMLHttpRequest.DONE) {
      this.xhr.abort();
    }
    else {
      if (!this.state.error) {
        csrfFetch(
          "api/v1.0/upload/" + this.props.file.name,
          {method: "delete"}
        );
      }
    }
  }

  render() {
    const {file, index, isLast, onRemove, onShiftDown, onShiftUp} = this.props;

    return (
      <Grid.Row>
        <Grid.Column width={1}>
          { index + 1 }
        </Grid.Column>
        <Grid.Column width={1}>
          { index !== 0 && <Icon name="caret up" size="large" link onClick={() => onShiftDown(index)}/> }
          { !isLast && <Icon name="caret down" size="large" link onClick={() => onShiftUp(index)}/> }
        </Grid.Column>
        <Grid.Column width={5}>
          <Form.Input placeholder={file.name}/>
        </Grid.Column>
        <Grid.Column width={3} style={{wordWrap: "break-word"}}>
          { file.name }
        </Grid.Column>
        <Grid.Column width={5}>
          <Progress
            percent={this.state.percent}
            size="tiny"
            {
              ...this.state.percent >= 100 ?
                this.state.error ? {error: true} : {success: true} :
                {active: true}
            }
          >
            { this.state.error }
          </Progress>
        </Grid.Column>
        <Grid.Column width={1}>
          <Icon name="remove" color="red" link onClick={() => onRemove(index)}/>
        </Grid.Column>
      </Grid.Row>
    )
  }
}


class FileUpload extends Component {

  static defaultProps = {
    required: false,
    submitted: false,
  };

  state = {
    files: [],
    messages: [],
  };

  /**
   * Add files to the state.files array if there is anything to add
   * and if the files have not already been added (check by file name).
   */
  addFile = (e) => {
    const files = e.target.files;
    let filesToAdd = [],
      messages = [];
    for (let i = 0; i < files.length; i++) {
      let file = files[i];
      if (this.state.files.filter((e) => e.name === file.name).length > 0) {
        messages.push(
          <div>
            <strong>{file.name}</strong> has already been added. Please choose a different file.
          </div>
        );
      }
      else {
        filesToAdd.push(file);
      }
    }
    this.setState({
      files: [...this.state.files, ...filesToAdd],
      messages: messages,
    })
  };

  /**
   * Remove a file from the state.files array with the supplied index.
   */
  removeFile = (index) => {
    if (this.state.files.length > 0) {
      this.setState({
        files: [...this.state.files.slice(0, index), ...this.state.files.slice(index + 1)]
      });
    }
  };

  shiftFileDown = (index) => {
    this._shiftFile(index, false)
  };

  shiftFileUp = (index) => {
    this._shiftFile(index)
  };

  _shiftFile = (index, up = true) => {
    const before = index + (up ? 1 : 0);
    this.setState({
      files: [
        ...this.state.files.slice(0, before - 1),
        ...this.state.files.slice(before, before + 1),
        ...this.state.files.slice(before - 1, before),
        ...this.state.files.slice(before + 1)
      ]
    })
  };

  /**
   * Cancel event if the latest file component is in
   * an error state or is in the process of uploading.
   */
  checkLatestFile = (e) => {  // TODO: remove
    if (this.refs.latestFile) {
      let msg = "";
      if (this.refs.latestFile.state.error) {
        msg = "You must remove the failed upload before you can add another file.";
      }
      else if (this.refs.latestFile.state.uploading) {
        msg = "You cannot add another file while while an upload is in progress.";
      }
      if (msg) {
        e.preventDefault();
      }
      this.setState({
        message: msg
      });
    }
  };

  fileHasError = () => {
    for (let [_, ref] of Object.entries(this.refs)) {
      if (ref.state.error) {
        return true;
      }
    }
  };

  render() {
    const {files, messages} = this.state;
    const {required, submitted} = this.props;
    const fileHasError = this.fileHasError();
    const hasError = required && submitted && (files.length === 0 || fileHasError);
    const fileRows = files.map((file, index) =>
      <FileRow
        key={file.name}
        file={file}
        index={index}
        isLast={index === files.length - 1}
        onRemove={this.removeFile}
        onShiftDown={this.shiftFileDown}
        onShiftUp={this.shiftFileUp}
        ref={`file${index}`}
      />
    );
    const messageListItems = messages.map((message, index) =>
      <Message.Item key={index} content={message}/>
    );

    return (
      <div>
        <Segment attached="top" style={ hasError ? {background: "#FFF6F6", borderColor: "#E0B4B4"} : {}}>
          <p>
            Please add files and arrange them in the order you would like them to appear for this publication.
          </p>
          <Grid divided="vertically">
            { fileRows }
          </Grid>
          <Grid>
            <Grid.Column>
              {/* NOTE: Using semantic-ui-react's Button in a Form will trigger submit! */}
              <label htmlFor="file">
                <div className="ui button fluid">
                  Add Files (PDFs only)
                </div>
              </label>
              <input
                multiple
                onChange={this.addFile}
                type="file"
                id="file"
                name="file"
                style={{display: "none"}}
                value=""
              />
            </Grid.Column>
          </Grid>
          { hasError &&
            <ErrorLabel
              content={fileHasError ? "You must remove any failed uploads" : "You must add at least 1 file."}
            />
          }
        </Segment>
        {
          messages.length > 0 &&
          <Message info attached="bottom">
            <Message.List>{messageListItems}</Message.List>
          </Message>
        }
      </div>
    )
  }
}

export default FileUpload;