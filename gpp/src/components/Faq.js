import React from 'react';
import {Container} from 'semantic-ui-react';


const Faq = () => (
  <Container>
    <h1>FAQ</h1>
    <ul>
      <li><a href="#1">What is the New York City Municipal Library Government Documents Portal?</a></li>
      <li><a href="#2">What is the Municipal Library?</a></li>
      <li><a href="#3">What is the New York City Department of Records and Information Services?</a></li>
      <li><a href="#4">How do I search the Government Documents Portal?</a></li>
    </ul>
    <h3 id="1">What is the New York City Municipal Library Government Documents Portal?</h3>
    <p>
      The Government Documents Portal is a permanent searchable digital repository for all of New York City’s recent
      agency publications, maintained by the Municipal Library at the New York City Department of Records and
      Information Services. The <a href="http://library.amlegal.com/nxt/gateway.dll/New%20York/charter/newyorkcitycharter/chapter49officersandemployees?f=templates$fn=default.htm$3.0$vid=amlegal:newyork_ny$anc=JD_1133" target="_blank">
      New York City Charter, Section 1133</a>, requires agencies to submit copies of any publication to us for permanent
      access and storage. This is part of the New York City government’s ongoing effort to be open and accessible for
      all citizens.
    </p>
    <h3 id="2">What is the Municipal Library?</h3>
    <p>
      The Municipal Library is one of the divisions of the New York City Department of Records and Information Services,
      located at 31 Chambers Street near City Hall (closest to the 4/5/6 trains Brooklyn Bridge – City Hall stop, and
      the N/R trains City Hall stop and the J/Z train Chambers Street stop). We are open to the public. Our hours are:
      <p>
        Monday – Wednesday 9:00 am to 4:30 pm
      </p>
      <p>
        Thursday 9:00 am to 7:00 pm
      </p>
      <p>
        Friday 9:00 am to 4:30 pm
      </p>
      You can contact us at 212-788-8950 or at <a href="mailto:munilib@records.nyc.gov">munilib@records.nyc.gov</a>.
    </p>
    <h3 id="3">What is the New York City Department of Records and Information Services?</h3>
    <p>
      Established in 1977, the <a href="http://nyc.gov/records" target="_blank">Department of Records and Information Services </a>
      preserves and provides public access to a vast and incomparable collection of historical and contemporary records
      and information about New York City government through the <a
      href="http://www.nyc.gov/html/records/html/archives/archives.shtml" target="_blank">Municipal Archives</a> which
      contains internal New York City records, including Mayoral papers), the <a
      href="http://www.nyc.gov/html/records/html/library/chlibrary.shtml" target="_blank">Municipal Library</a> which contains all of
      New York City agencies’ published materials) and the Records Management Division. The Records Management Division
      operates records storage facilities in two locations with a combined capacity of 700,000 cubic feet, and provides
      records management services to fifty City agencies, ten courts, and the five district attorneys’ offices. Records
      services include scheduling, off-site storage and retrieval, and overall guidance on management of records in all
      media. The Grants Administration Unit assists mayoral agencies with records management by advising on obtaining
      and managing grants from the New York State Archives’ Local Government Records Management Improvement Fund.
    </p>
    <h3 id="4">How do I search the Government Documents Portal?</h3>
    <p>
      You can search for recent New York City government publications in electronic, PDF form. Our search page allows
      keyword searches, and also an advanced search option that lets you search
      <ul>
        <li>By Agency Name</li>
        <li>By Subject</li>
        <li>By Title</li>
        <li>By Report Type (such as Executive Order, City Council testimony, Annual Report)</li>
        <li>By Date</li>
      </ul>
      Once you have search results, you can sort them by relevance, by date (either by searching a specific date or by
      using the slider to narrow to a range of dates), and alphabetically.
    </p>
    <br/>
    <br/>
  </Container>
);

export default Faq;