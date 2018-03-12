# myflaskapp
First Flask Application with SQlite3 Database

Initial Commit on 3/12/18:  End of Video 2 on Traversy Media - Python Flask From Scratch Video.
 - Opted to use SQlite3 instead of MySQL database.  There is still an issue with using the default Timestamp from the database since Python makes you represent every database field with a ?.  To overcome this issue, the datetime.datetime.now() function is being used to create a timestamp for this value.
 - When developing the project for an SAP Part nubmer workflow.  MySQL will be utilized.  Python will need to be loaded on the server.
