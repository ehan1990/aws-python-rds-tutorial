
dev-setup:
	pip3 install -r requirements.txt

health:
	@curl localhost:8080/healthcheck

list-stocks:
	@curl -s localhost:8080/stocks | jq

# TICKER=AAPL NAME=Apple make add-stock
add-stock:
	@curl -X POST -d '{"ticker": "${TICKER}", "name": "${NAME}"}' localhost:8080/stocks

run:
	@python3 app.py

# export your envs
# e.g. export DB_USER=foo DB_PW=bar
db-init:
	$(if ${DB_USER},,$(error DB_USER is not defined))
	$(if ${DB_PW},,$(error DB_PW is not defined))
	@mysql -u${DB_USER} -p${DB_PW} < sql/init.sql

# export your envs
# e.g. export DB_USER=foo DB_PW=bar HOST=db.us-west-2.rds.amazonaws.com
db-init-remote:
	$(if ${DB_USER},,$(error DB_USER is not defined))
	$(if ${DB_PW},,$(error DB_PW is not defined))
	@mysql -u${DB_USER} -p${DB_PW} -h ${HOST} -P 3306 < sql/init.sql

db-login-cmd:
	@echo "mysql -u${DB_USER} -p${DB_PW}"
