import React, {Component, PropTypes} from 'react'
import {Progress, Grid, Segment, Message} from 'semantic-ui-react'
import {readCookie} from '../utils/cookie'
import {csrfFetch} from '../utils/fetch'
import {FormFieldPrompt} from './custom'


class FileRow extends Component {

  static propTypes = {
    file: PropTypes.shape({
      size: PropTypes.number.isRequired,
      name: PropTypes.string.isRequired
    }),
    index: PropTypes.number.isRequired
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
      error: "Failed to upload file. Please Remove and try again.",
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
        errorMsg = JSON.parse(this.xhr.responseText).message;
      }
      catch (err) {
        errorMsg = "Failed to upload file due to an unhandled server error. Please Remove and try again."
      }
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
          { method: "delete" }
        );
      }
    }
  }

  render() {
    const {file, index} = this.props;

    return (
      <Grid.Row>
        <Grid.Column width={1}>
          { index + 1 }
        </Grid.Column>
        <Grid.Column style={{wordWrap: "break-word"}} width={4}>
          { file.name }
        </Grid.Column>
        <Grid.Column width={11}>
          <Progress
            percent={this.state.percent}
            {
              ...this.state.percent >= 100 ?
                this.state.error ? {error: true} : {success: true} :
                {active: true}
            }
          >
            { this.state.error }
          </Progress>
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
    message: "",
  };

  /**
   * Add a file to the state.files array if there is anything to add
   * and if the file has not already been added (check by file name).
   */
  addFile = (e) => {
    if (e.target.files.length > 0) {
      let file = e.target.files[0];
      if (this.state.files.filter((e) => {
        return e.name === file.name;
      }).length > 0) {
        this.setState({
          message: `"${file.name}" has already been added. Please choose a different file.`
        })
      }
      else {
        this.setState({
          files: [...this.state.files, file],
          message: ""
        });
      }
    }
  };

  /**
   * Remove a file from the state.files array if there is
   * anything to remove.
   */
  removeFile = () => {
    if (this.state.files.length > 0) {
      this.setState({
        files: this.state.files.slice(0, -1),
        message: ""
      });
    }
  };

  /**
   * Cancel event if the latest file component is in
   * an error state or is in the process of uploading.
   */
  checkLatestFile = (e) => {
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

  render() {
    const {files, message} = this.state;
    const {required, submitted} = this.props;
    const hasError = required && submitted && files.length === 0;
    const fileList = files.map((file, index) =>
      <FileRow key={file.name} file={file} index={index} ref="latestFile"/>
    );

    return (
      <Segment style={ hasError ? { background: "#FFF6F6", borderColor: "#E0B4B4"}: {}}>
        <p>
          Please add files in the order you would like them to appear for this publication.
        </p>
        <Grid divided>
          { fileList }
        </Grid>
        <Grid columns={2}>
          <Grid.Column>
            {/* NOTE: Using semantic-ui-react's Button in a Form will trigger submit! */}
            <label htmlFor="file">
              <div className="ui button fluid" onClick={this.checkLatestFile}>
                Add
              </div>
            </label>
            <input
              onChange={this.addFile}
              type="file"
              id="file"
              name="file"
              style={{display: "none"}}
              value=""
            />
          </Grid.Column>
          <Grid.Column>
            <div
              onClick={ this.removeFile }
              className={"ui button fluid negative" + ( files.length === 0 ? " disabled" : "") }
            >
              Remove
            </div>
          </Grid.Column>
        </Grid>
        { message && <Message content={ message }/> }
        { hasError && <FormFieldPrompt content="You must add at least 1 file." /> }
      </Segment>
    )
  }
}

export default FileUpload;