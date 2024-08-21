# SignON Locust Testing
The SignON Locust Testing repository is part of [SignON](https://signon-project.eu/) an EU H2020 research and innovation funded project.
The SignON Locust Testing is a tool with the aim of testing throuput and scalability for the entire SignON Platform.

### Usage
In order to start the SignON Locust Testing, is required to have the SignON platform up and running, it's possibl;e to start it using the [SignON Framework Docker Compose repository](https://github.com/signon-project-wp2/signon-extractor).
Once the SignON platform is deployed it's possible to start the testing using `docker compose -f docker-compose-LOCUST.yml up`, and then by going to http://localhost:8080 run the specified locust test.
Once the test is complete, it's possible to analyse the results by running the difference code cells in the `results.ipynb` file.

## Authors
This project was developed by [FINCONS GROUP AG](https://www.finconsgroup.com/) within the Horizon 2020 European project SignON under grant agreement no. [101017255](https://doi.org/10.3030/101017255).  
For any further information, please send an email to [signon-dev@finconsgroup.com](mailto:signon-dev@finconsgroup.com).

## License
This project is released under the [Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0.html).
