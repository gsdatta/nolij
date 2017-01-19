# nolij

## Goals
Secure and team centered information sharing made easy. 

Security 	- Control user permissions to those who need it. 
	Authentication - Domain and invite based access to teams and folios. 
	Shares information with relevent users. 

Ease of Use - User interfacce is simple, and gets the job done. 
	- User friendly, made with every possible user in mind! 

## Install for development
The dependencies are `postgres` and `virtualenv`.
```bash
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

Create a database in your postgres install called `nolij`. If there is a user, update as such in
`config.py` - for example, the url would become `postgres://user:password@localhost:5432/nolij`.

To run the server, from the root directory of this project, execute `python -m nolij dev`.


## Contributing
Anyone can help make this project better - read [CONTRIBUTING](CONTRIBUTING.md) to get started!


## License
Proprietary. See the [LICENSE](LICENSE) file for more details.
