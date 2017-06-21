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
    uploadDirName: PropTypes.string.isRequired,
    index: PropTypes.number.isRequired,
    isLast: PropTypes.bool.isRequired,
    onRemove: PropTypes.func.isRequired,
    onShiftDown: PropTypes.func.isRequired,
    onShiftUp: PropTypes.func.isRequired,
    onFileTitleChange: PropTypes.func.isRequired,
    submitted: PropTypes.bool.isRequired
  };

  state = {
    percent: 0,
    error: "",
    uploading: true,
    title: '',
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
    try {
      let jsonResponse = JSON.parse(this.xhr.responseText);
      if (this.xhr.status !== 200 || jsonResponse.status === "fail") {
        errorMsg = jsonResponse.data || jsonResponse.message
      }
    }
    catch (err) {
      errorMsg = "Failed to upload file due to an unhandled server error."
    }
    this.setState({
      percent: 100,
      error: errorMsg,
      uploading: false
    })
  };

  /**
   * FileRow has been mounted, so start uploading this.props.file.
   */
  componentDidMount() {
    // TODO: frontend validation (number?, size?, total size?, mimetype, user authenticated, etc.)
    const {file, uploadDirName} = this.props;
    let data = new FormData();
    data.append("file", file);
    this.xhr.upload.addEventListener("progress", this.uploadProgress);
    this.xhr.upload.addEventListener("error", this.uploadFailed);
    this.xhr.open("POST", "/api/v1.0/upload/" + uploadDirName);
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
    const {file, uploadDirName} = this.props;
    if (this.xhr.readyState !== XMLHttpRequest.DONE) {
      this.xhr.abort();
    }
    else {
      if (!this.state.error) {
        csrfFetch(
          `api/v1.0/upload/${uploadDirName}/${file.name}`,
          {method: "delete"}
        );
      }
    }
  }

  onTitleChange = (index) => (e, {value}) => {
    this.setState({
      title: value.replace(/^\s+|\s+$/g, '')
    });
    this.props.onFileTitleChange(index, value)
  };

  render() {
    const {file, index, isLast, onRemove, onShiftDown, onShiftUp, submitted} = this.props;

    return (
      <Grid.Row>
        <Grid.Column width={1}>
          { index + 1 }
        </Grid.Column>
        { index === 0 && isLast ? null :
          <Grid.Column width={1}>
            { index !== 0 && <Icon name="caret up" size="large" link onClick={() => onShiftDown(index)}/> }
            { !isLast && <Icon name="caret down" size="large" link onClick={() => onShiftUp(index)}/> }
          </Grid.Column>
        }
        <Grid.Column width={index === 0 && isLast ? 6 : 5}>
          <Form.Input
            placeholder={file.name}
            onChange={this.onTitleChange(index)}
            error={submitted && this.state.title.length < 3}
          />
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

  static propTypes = {
    required: PropTypes.bool,
    submitted: PropTypes.bool,
    uploadDirName: PropTypes.string.isRequired,
    errors: PropTypes.array
  };

  static defaultProps = {
    required: false,
    submitted: false,
    errors: []
  };

  state = {
    files: [],
    warningMessages: [],
    warningMessageIsVisible: true,
    fileHasError: false
  };

  /**
   * Add files to the state.files array if there is anything to add
   * and if the files have not already been added (check by file name),
   * and if the files are PDFs.
   */
  addFile = (e) => {
    const files = e.target.files;
    let filesToAdd = [],
      messages = [];
    for (let i = 0; i < files.length; i++) {
      let file = files[i];
      if (file.type !== "application/pdf") {
        messages.push(
          <div>
            <strong>{file.name}</strong> is not a PDF file. Please choose a different file.
          </div>
        )
      }
      else if (this.state.files.filter((e) => e.name === file.name).length > 0) {
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
      warningMessages: messages,
      warningMessageIsVisible: true
    })
  };

  fileTitleChange = (index, value) => {
    let file = this.state.files[index];
    file.title = value;
    this.setState({
      files: [
        ...this.state.files.slice(0, index),
        file,
        ...this.state.files.slice(index + 1, this.state.files.length)
      ]
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

  /**
   * Move file down 1 index in the state.files array
   */
  shiftFileDown = (index) => {
    this._shiftFile(index, false)
  };

  /**
   * Move file up 1 index in the state.files array
   */
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
   * Check all refs to FileRows for errors.
   */
  fileHasError = () => {
    for (let [_, ref] of Object.entries(this.refs)) {
      if (ref.state.error) {
        return true;
      }
    }
    return false;
  };

  /**
   * Call fileHasError and update state now that refs are available.
   */
  componentDidUpdate() {
    if (this.fileHasError()) {
      if (!this.state.fileHasError) {
        this.setState({
          fileHasError: true
        })
      }
    }
    else {
      if (this.state.fileHasError) {
        this.setState({
          fileHasError: false
        })
      }
    }
  }

  render() {
    const {files, warningMessages, warningMessageIsVisible, fileHasError} = this.state;
    const {required, submitted, uploadDirName, errors} = this.props;

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
        onFileTitleChange={this.fileTitleChange}
        ref={"file" + index}
        uploadDirName={uploadDirName}
        submitted={submitted}
      />
    );

    const errorMessageListItems = errors.map((message, index) =>
      <Message.Item key={index} content={<strong>{message}</strong>}/>
    );

    const warningMessageListItems = warningMessages.map((message, index) =>
      <Message.Item key={index} content={message}/>
    );

    return (
      <div>
        <Segment style={ hasError ? {background: "#FFF6F6", borderColor: "#E0B4B4"} : {}}>
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
          {
            errors.length > 0 && files.length > 0 &&
            <Message error>
              <Message.List>{errorMessageListItems}</Message.List>
            </Message>
          }
          {
            warningMessages.length > 0 && warningMessageIsVisible &&
            <Message
              onDismiss={() => this.setState({warningMessageIsVisible: false})}
              warning
            >
              <Message.List>{warningMessageListItems}</Message.List>
            </Message>
          }
        </Segment>
        {
          hasError &&
          <ErrorLabel
            content={fileHasError ? "You must remove any failed uploads." : "You must add at least 1 file."}
            style={{marginTop: 0}}
          />
        }
      </div>
    )
  }
}

export default FileUpload;