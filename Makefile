all:
	cp packages/django_security_db/dist/security_db-0.1.tar.gz app/web/custom_packages
	cp packages/django_security_db/dist/security_db-0.1.tar.gz app/equity_updater/custom_packages
	docker-compose -f app/docker-compose.yaml up --build

