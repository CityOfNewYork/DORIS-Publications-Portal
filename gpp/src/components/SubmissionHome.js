import React, {Component} from 'react';
import {Link} from 'react-router-dom';

class SubmissionHome extends Component {
  render() {
    return (
      <div>
        <h1>NYC Submissions Portal</h1>
        <p>
          Welcome to the Submissions Portal for the Municipal Library at the New York City Department of Records and
          Information Services. The Submissions Portal is a convenient, secure online system for New York City agencies
          to electronically submit their publication to the Government Documents Portal of the Municipal Library.
        </p>
        <h3>Getting Started</h3>
        <ul>
          <li>Complete the information (metadata) in the automated <Link to="/submit">form</Link>.</li>
          <li>
            Upload your document following the instructions (either before or after filling out the required
            information). It must be in PDF format. You will receive confirmation that you have successfully uploaded
            the document.
          </li>
          <li>
            You can choose to save your submission for further work or submit once the information is complete and
            the upload is successful.
          </li>
          <li>
            The Municipal Library staff checks that everything is in order, and contacts you if there is any problem.
            Once the submission is trouble-free, staff loads the publication to the Government Documents Portal,
            where it is accessible and preserved.
          </li>
        </ul>
      </div>
    )
  }
}

export default SubmissionHome
