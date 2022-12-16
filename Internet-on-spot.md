# How to setup spot to use internet via proxy over ssh
This is a quick guide on how to setup a host computer and spot to get internet on spot via a proxy server running on the host computer.

**NOTE: You will need atleast 2 network adapters on the host computer. 1 to connect to spot, 1 to connect to the internet.** 

1. Start by downloading a proxy server on the host computer that will ssh onto spot
    * Squid is a good proxy server, available on both Windows and Linux
    * The rest of the examples in this writeup will assume you are using squid, however you can use another proxy server but configuration may vary
2. In the squid configuration file, by default `/etc/squid/squid.conf` or `C:\Squid\etc\squid\squid.conf`, note the following.
    1. The port that squid listens on. This port will be over the host computers `localhost:` interface. By default it is port `3128` but can be found/changed by the configuration setting `http_port <port>`.
    2. Comment out `http_access deny all` by putting a pound sign infront, `# http_access deny all`, and add the setting `http_access allow all`
3. Run the proxy server, you can check that it is running by navigating to `localhost:<port>` and checking that the proxy is displaying something.
4. After connectings to spots local wifi network, when you now ssh onto spot, add the following arguement. `ssh -R <port to be used on spot>:localhost:<port on host computer>`
    * EX: `ssh -R 3129:localhost:3128 spot@192.168.80.3`
5. Once ssh'ed onto spot, set the following environemnt variables. `http_proxy` and `https_proxy`. They both need to be set to `localhost:<port to be used on spot>`
    * EX: 
        * `export http_proxy=localhost:3129`
        * `export https_proxy=localhost:3129`
6. Check that internet is present by running `wget google.com` and making sure that it downloads `index.html`

**MORE NOTES**
* Root uses a difference environment session that the normal user. This means that if you use `sudo apt install ...` it will not work. This is because sudo will temporarily elevate you to root, clearing the `http_proxy/https_proxy` variables. You can get around this by properly setting apt proxy settings or by running `sudo su` to enter a root session, and then re-setting the environment variables and running `apt install ...` again after.
* Vscode and other ssh tools may mess up the ssh configuration or add more on top causing this method to not work. We found the best results by doing everything manually in a terminal to install our required packages, then using vscodes remote server to develop seperately, returning to the terminal to install anymore dependencies that we may need.