mrsvnsync
=========
Multiple Repositories svnsync
		
Usage
=========
<h5>Install the httplib2 package</h5>
<pre><code>pip install httplib2</code></pre>
<h5>Open mrsvnsync.ini , and set the parameter</h5>
<p>
	Set the destination path to store the mirror repositories:
</p>
<pre><code>SVNBackupDir =  C:/SvnBackup</code></pre>
<p>If you run mrsvnsync locally on the SVN server , you should set the SVNPathParentPath , for example :</p>
<pre><code>SVNPathParentPath =  C:/Repositories</code></pre>
<p>If you run mrsvnsync on the another server , and you access the SVN server by HTTP or HTTPS protocol , you should set the SVNAccessUrl , for example:</p>
<pre><code>SVNAccessUrl = https://192.168.1.1/svn/</code></pre>
<p>
If your SVN server  requires authentication , you may specify the username and password:
</p>
<pre><code>UserName = username
Password = passowrd
</code></pre>
<h5>Run mrsvnsync , and you can run it by crontab or Schedule Task</h5>
<pre><code>python mrsvnsync.py</code></pre>


Notes
=========
While you access your SVN Server by HTTPS protocol , you may receive an error message like this:
<pre><code>
Traceback (most recent call last):
  File "usinghttplib2.py", line 28, in module
    response, content = http.request(url, "GET", headers=headers)
  File "/usr/local/python3/lib/python3.2/site-packages/httplib2/__init__.py", line 1059, in request
    self.disable_ssl_certificate_validation)
  File "/usr/local/python3/lib/python3.2/site-packages/httplib2/__init__.py", line 775, in __init__
    check_hostname=True)
  File "/usr/local/python3/lib/python3.2/http/client.py", line 1086, in __init__
    raise ValueError("check_hostname needs a SSL context with "
ValueError: check_hostname needs a SSL context with either CERT_OPTIONAL or CERT_REQUIRED
</code></pre>

You can download the patch for httplib2 via
<https://code.google.com/p/httplib2/issues/detail?id=173>

Dependencies
=========
httplib2 (pip install httplib2)
