													#{nol-ij}

<PROJECT DESCRIPTION>
## Mission Statement
Secure and team centered information sharing made easy. 

Security 	- Control user permissions to those who need it. 
	Authentication - Domain and invite based access to teams and folios. 
	Shares information with relevent users. 

Ease of Use - User interfacce is simple, and gets the job done. 
	- User friendly, made with every possible user in mind! 

## Features

* TODO

## Project Agenda: 

View the following google docs to understand project status and updates as they are being implemented. 

Once {nol-ij} stands at a level where it can support our documentation, it will be moved there. 


https://docs.google.com/document/d/19G0_CfLpAAa_jSBKRaoj1lL2kn6vnpZE0iQV3zjQoc8/edit#


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
