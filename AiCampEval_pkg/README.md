Hello World

Create a function called test_model(X_test) which takes X_test as input, and returns a list of string predictions.
X_test is a list of numpy arrays. Each numpy array is an image.
In the script with the function test_model, import the test function as such:

from AiCampEval import eval

and use the function by calling:

eval(test_model, 'submission_1', 'team123')
<!-- eval(test_model, 'http://www.url123', 'submission_1', 'team123') -->

where arguments are:
test_model : function written by you that takes numpy images input and returns prediction string
<!-- 'http://www.url123' : the url to get the test set from, to be released at submission time -->
'submission_1' : the submission session, to be released at submission time
'team123' : team secret. your team's secret id, please do not share this.